import sys
import string
import argparse
import math

def read_file(filename):
    with open(filename) as f:
        return f.read()    
    pass


def file_into_lines(content):
    return content.translate(content)

def get_word_frequencies(filename):
    content = read_file(filename)
    words = file_into_lines(content).split()

    word_to_freq = {}
    for w in words:
        if w in word_to_freq:
            word_to_freq[w] += 1
        else:
            word_to_freq[w] = 1
    
    return word_to_freq

def inner_product(D1, D2):

    sum = 0.0
    for key in D1:
        if key in D2:
            sum += D1[key] * D2[key]
    return sum

def vector_angle(D1,D2):
    return math.acos(inner_product(D1,D2)/math.sqrt(inner_product(D1,D1)*inner_product(D2,D2)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--first', type=str, required=True)
    parser.add_argument('-s', '--second', type=str, required=True)

    parsed_args = parser.parse_args()
    first = parsed_args.first
    second = parsed_args.second

    first_word_freq = get_word_frequencies(first)
    second_word_freq = get_word_frequencies(second)

    similarity = vector_angle(first_word_freq, second_word_freq)
    print('Similariry {}'.format(similarity))

    pass
