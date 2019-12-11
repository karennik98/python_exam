import requests

def bet(year, round, userBets):
    r = requests.get('https://ergast.com/api/f1/'+str(year)+'/'+str(round)+'/driverStandings.json').json()
    d = {}
    for k in r['MRData']['StandingsTable']['StandingsLists']:
        for k1 in k['DriverStandings']:
            d[k1['Driver']['driverId']] = k1['position']
    tot = 0
    win_tot = 0
    for user in userBets:
        for bet in user:
            tot += int(bet[2])
            if bet[0] in d and d[bet[0]] == bet[1]:
                win_tot += int(bet[2])    
    
    largest = -float("inf")
    for user in userBets:
        user_tot = 0
        user_win_tot = 0
        for bet in user:
            user_tot += int(bet[2])
            if bet[0] in d and d[bet[0]] == bet[1]:
                user_win_tot += int(bet[2])*tot//win_tot
        winnings = user_win_tot - user_tot
        if winnings > largest:
            largest = winnings
    return largest