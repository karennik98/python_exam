# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1


class NewsStory(object):
    def __init__(self, _guid, _title, _description, _link, _pubdate):
        self.guid = _guid
        self.title = _title
        self.description = _description
        self.link = _link
        self.pubdate = _pubdate.replace(tzinfo=pytz.timezone("EST"))

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

# ======================
# Triggers
# ======================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS


# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().split()

    def is_phrase_in(self, text):
        clear_text = str()
        for i in range(len(text)):
            if text[i] not in string.punctuation and not (text[i] == ' ' and text[i - 1] == ' '):
                clear_text += text[i].lower()
            else:
                clear_text += ' '
        clear_text = clear_text.split()
        try:
            start = clear_text.index(self.phrase[0])
        except ValueError:
            return False
        for i in range(len(self.phrase)):
            try:
                if self.phrase[i] == clear_text[start]:
                    start += 1
                    continue
                else:
                    return False
            except IndexError:
                return False
        return True


# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().split()

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.


class TimeTrigger(Trigger):
    def __init__(self, pubtime):
        format = '%d %b %Y %H:%M:%S'
        pubtime = datetime.strptime(pubtime, format)
        pubtime = pubtime.replace(tzinfo=pytz.timezone("EST"))
        self.pubtime = pubtime

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, string_time):
        self.time = datetime.strptime(string_time, "%d %b %Y %X").replace(tzinfo=pytz.timezone("EST"))

    def evaluate(self, story):
        return story.get_pubdate() < self.time


class AfterTrigger(TimeTrigger):
    def __init__(self, string_time):
        self.time = datetime.strptime(string_time, "%d %b %Y %X").replace(tzinfo=pytz.timezone("EST"))

    def evaluate(self, story):
        return story.get_pubdate() > self.time

# COMPOSITE TRIGGERS


# Problem 7
class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        self.trigger = other_trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8
class AndTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        self.first = first_trigger
        self.second = second_trigger

    def evaluate(self, story):
        return self.first.evaluate(story) and self.second.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        self.first = first_trigger
        self.second = second_trigger

    def evaluate(self, story):
        return self.first.evaluate(story) or self.second.evaluate(story)

# ======================
# Filtering
# ======================


# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    trig_stories = []
    for story in stories:
        for trig in triggerlist:
            if trig.evaluate(story):
                trig_stories.append(story)
                break
    return trig_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trig_dict = {}
    trig_list = []
    for i in range(len(lines)):
        trig = lines[i].split(',')
        if trig[1] == 'TITLE':
            trig_dict[trig[0]] = TitleTrigger(trig[2])
        elif trig[1] == 'DESCRIPTION':
            trig_dict[trig[0]] = DescriptionTrigger(trig[2])
        elif trig[1] == 'AFTER':
            trig_dict[trig[0]] = AfterTrigger(trig[2])
        elif trig[1] == 'BEFORE':
            trig_dict[trig[0]] = BeforeTrigger(trig[2])
        elif trig[1] == 'NOT':
            trig_dict[trig[0]] = NotTrigger(trig[2])
        elif trig[1] == 'AND':
            trig_dict[trig[0]] = AndTrigger(trig_dict[trig[2]], trig_dict[trig[3]])
        elif trig[0] == 'ADD':
            for x in range(1, len(trig)):
                trig_list.append(trig_dict[trig[x]])
    return trig_list
            

SLEEPTIME = 120 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
