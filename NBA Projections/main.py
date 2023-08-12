from nba_api.stats.endpoints import leaguegamefinder
from random import random

games = leaguegamefinder.LeagueGameFinder(season_nullable='2022-23', league_id_nullable='00', season_type_nullable='Regular Season')

elos = {}
wins = {}
western = set()
eastern = set()

western.update(['DEN', 'MEM', 'SAC', 'PHX', 'LAC', 'GSW', 'LAL', 'MIN', 'NOP', 'OKC', 'DAL', 'UTA', 'POR', 'HOU', 'SAS'])
eastern.update(['MIL', 'BOS', 'PHI', 'CLE', 'NYK', 'BKN', 'MIA', 'ATL', 'TOR', 'CHI', 'IND', 'WAS', 'ORL', 'CHA', 'DET'])

for game_index, game in games.get_data_frames()[0].iterrows():
    teams = (game['MATCHUP'])
    if '@' in teams:
        away, home = teams.split(' @ ')
        if away not in elos:
            wins[away] = 0
            elos[away] = 1500
        if home not in elos:
            wins[home] = 0
            elos[home] = 1500
        awayExpected = (1/(1 + 10**((elos[home] - elos[away] + 100)/400)))
        homeExpected = (1/(1 + 10**((elos[away] - elos[home] - 100)/400)))
        if game['WL'] == 'W':
            wins[away] += 1
            awayVal = 1
            homeVal = 0
        else:
            wins[home] += 1
            awayVal = 0
            homeVal = 1
        
        elos[away] = elos[away] + 20 * (awayVal - awayExpected)
        elos[home] = elos[home] + 20 * (homeVal - homeExpected)


wins = sorted(wins.items(), key=lambda x:-x[1])

eastBracket = []
westBracket = []
eastPlayInOne = []
eastPlayInTwo = []
westPlayInOne = []
westPlayInTwo = []
i = 0
j = 0

for team, record in wins:
    if team in eastern:
        if i < 10 and i > 7:
            eastPlayInTwo.append(team)
        elif i < 8 and i > 5:
            eastPlayInOne.append(team)
        elif i < 6:
            eastBracket.append(team)
        i += 1
    
    else:
        if j < 10 and j > 7:
            westPlayInTwo.append(team)
        elif j < 8 and j > 5:
            westPlayInOne.append(team)
        elif j < 6:
            westBracket.append(team)
        j += 1

# print(f'East Bracket:{eastBracket}')
# print(f'East Play In One:{eastPlayInOne}')
# print(f'East Play In Two:{eastPlayInTwo}')
# print(f'West Bracket:{westBracket}')
# print(f'West Play In One:{westPlayInOne}')
# print(f'West Play In Two:{westPlayInTwo}')

def get_win_expectation(home_elo, away_elo):
    return (1/(1 + 10**((away_elo - home_elo - 100)/400)))

playoff_entries = {}
secondround_entries = {}
thirdround_entries = {}
fourthround_entries = {}
finalist_entries = {}

def playIn(BracketForecast, playInOne, playInTwo):
    if get_win_expectation(elos[playInOne[0]], elos[playInOne[1]]) > random():
        BracketForecast.append(playInOne[0])
        playInOneLoser = playInOne[1]
    else:
        BracketForecast.append(playInOne[1])
        playInOneLoser = playInOne[0]

    playInTwoWinner = playInTwo[0] if get_win_expectation(elos[playInTwo[0]], elos[playInTwo[1]]) > random() else playInTwo[1]

    BracketForecast.append(playInOneLoser if get_win_expectation(elos[playInOneLoser], elos[playInTwoWinner]) > random() else playInTwoWinner)

    for team in BracketForecast:
        if not team in playoff_entries:
            playoff_entries[team] = 0
        playoff_entries[team] += 1

def playOff(mainBracket, fourthRound):
    secondRound = []
    
    oneSeed = 0
    eightSeed = 0 
    i = 1
    
    while oneSeed < 4 and eightSeed < 4:
        if i == 1 or i == 2 or i == 5 or i == 7:
            if get_win_expectation(elos[mainBracket[0]], elos[mainBracket[7]]) > random():
                oneSeed += 1
            else:
                eightSeed += 1
        else:
            if get_win_expectation(elos[mainBracket[7]], elos[mainBracket[0]]) > random():
                eightSeed += 1
            else:
                oneSeed += 1
        i += 1
    if oneSeed == 4:
        secondRound.append(mainBracket[0])
    else:
        secondRound.append(mainBracket[7])
    
    fourSeed = 0
    fiveSeed = 0
    i = 1
    while fourSeed < 4 and fiveSeed < 4:
        if i == 1 or i == 2 or i == 5 or i == 7:
            if get_win_expectation(elos[mainBracket[3]], elos[mainBracket[4]]) > random():
                fourSeed += 1
            else:
                fiveSeed += 1
        else:
            if get_win_expectation(elos[mainBracket[4]], elos[mainBracket[3]]) > random():
                fiveSeed += 1
            else:
                fourSeed += 1
        i += 1
    if fourSeed == 4:
        secondRound.append(mainBracket[3])
    else:
        secondRound.append(mainBracket[4])
    
    threeSeed = 0
    sixSeed = 0
    i = 1
    while threeSeed < 4 and sixSeed < 4:
        if i == 1 or i == 2 or i == 5 or i == 7:
            if get_win_expectation(elos[mainBracket[2]], elos[mainBracket[5]]) > random():
                threeSeed += 1
            else:
                sixSeed += 1
        else:
            if get_win_expectation(elos[mainBracket[5]], elos[mainBracket[2]]) > random():
                sixSeed += 1
            else:
                threeSeed += 1
        i += 1
    if threeSeed == 4:
        secondRound.append(mainBracket[2])
    else:
        secondRound.append(mainBracket[5])
    
    twoSeed = 0
    sevenSeed = 0
    i = 1
    while twoSeed < 4 and sevenSeed < 4:
        if i == 1 or i == 2 or i == 5 or i == 7:
            if get_win_expectation(elos[mainBracket[1]], elos[mainBracket[6]]) > random():
                twoSeed += 1
            else:
                sevenSeed += 1
        else:
            if get_win_expectation(elos[mainBracket[6]], elos[mainBracket[1]]) > random():
                sevenSeed += 1
            else:
                twoSeed += 1
        i += 1
    if twoSeed == 4:
        secondRound.append(mainBracket[1])
    else:
        secondRound.append(mainBracket[6])
    
    for team in secondRound:
        if not team in secondround_entries:
            secondround_entries[team] = 0
        secondround_entries[team] += 1
    
    # ---Next Round---
    
    thirdRound = []
    
    oneSeed = 0
    twoSeed = 0
    i = 1
    while oneSeed < 4 and twoSeed < 4:
        if i == 1 or i == 2 or i == 5 or i == 7:
            if get_win_expectation(elos[secondRound[0]], elos[secondRound[1]]) > random():
                oneSeed += 1
            else:
                twoSeed += 1
        else:
            if get_win_expectation(elos[secondRound[1]], elos[secondRound[0]]) > random():
                twoSeed += 1
            else:
                oneSeed += 1
        i += 1
    if oneSeed == 4:
        thirdRound.append(secondRound[0])
    else:
        thirdRound.append(secondRound[1])
    
    threeSeed = 0
    fourSeed = 0
    i = 1
    while threeSeed < 4 and fourSeed < 4:
        if i == 1 or i == 2 or i == 5 or i == 7:
            if get_win_expectation(elos[secondRound[2]], elos[secondRound[3]]) > random():
                threeSeed += 1
            else:
                fourSeed += 1
        else:
            if get_win_expectation(elos[secondRound[3]], elos[secondRound[2]]) > random():
                fourSeed += 1
            else:
                threeSeed += 1
        i += 1
    if threeSeed == 4:
        thirdRound.append(secondRound[2])
    else:
        thirdRound.append(secondRound[3])
    
    for team in thirdRound:
        if not team in thirdround_entries:
            thirdround_entries[team] = 0
        thirdround_entries[team] += 1
    
    #---Next Round---
    
    oneSeed = 0
    twoSeed = 0
    i = 1
    while oneSeed < 4 and twoSeed < 4:
        if i == 1 or i == 2 or i == 5 or i == 7:
            if get_win_expectation(elos[thirdRound[0]], elos[thirdRound[1]]) > random():
                oneSeed += 1
            else:
                twoSeed += 1
        else:
            if get_win_expectation(elos[thirdRound[1]], elos[thirdRound[0]]) > random():
                twoSeed += 1
            else:
                oneSeed += 1
        i += 1
    if oneSeed == 4:
        fourthRound.append(thirdRound[0])
    else:
        fourthRound.append(thirdRound[1])
    
    for team in fourthRound:
        if not team in fourthround_entries:
            fourthround_entries[team] = 0
        fourthround_entries[team] += 1
    
def simulator(playoff_odds, secondround_odds, thirdround_odds, fourthround_odds, finalist_odds):
    for i in range(10000):
        fourthRoundEast = []
        fourthRoundWest = []
        fifthRound = []
    
        eastForecast = eastBracket.copy()
        playIn(eastForecast, eastPlayInOne, eastPlayInTwo)
        east = eastForecast.copy()
        playOff(eastForecast, fourthRoundEast)
    
        westForecast = westBracket.copy()
        playIn(westForecast, westPlayInOne, westPlayInTwo)
        west = westForecast.copy()
        playOff(westForecast, fourthRoundWest)
        
        fourthRound = [fourthRoundEast[0], fourthRoundWest[0]]
    
        firstTeamPos = east.index(fourthRound[0])
        secondTeamPos = west.index(fourthRound[1])
    
        if firstTeamPos < secondTeamPos:
            home_team = fourthRound[0]
            away_team = fourthRound[1]
        elif firstTeamPos > secondTeamPos:
            home_team = fourthRound[1]
            away_team = fourthRound[0]
        elif random() > 0.5:
            home_team = fourthRound[0]
            away_team = fourthRound[1]
        else:
            home_team = fourthRound[1]
            away_team = fourthRound[0]
    
        homeGames = 0
        awayGames = 0
    
        while homeGames < 4 and awayGames < 4:
            if i == 1 or i == 2 or i == 5 or i == 7:
                if get_win_expectation(elos[home_team], elos[away_team]) > random():
                    homeGames += 1
                else:
                    awayGames += 1
            else:
                if get_win_expectation(elos[away_team], elos[home_team]) > random():
                    awayGames += 1
                else:
                    homeGames += 1
            i += 1
    
        if homeGames == 4:
            fifthRound.append(home_team)
        else:
            fifthRound.append(away_team)
    
        for team in fifthRound:
            if not team in finalist_entries:
                finalist_entries[team] = 0
            finalist_entries[team] += 1
        
    for team in playoff_entries:
        playoff_odds[team] = playoff_entries[team] / 10000

    for team in secondround_entries:
        secondround_odds[team] = secondround_entries[team] / 10000

    for team in thirdround_entries:
        thirdround_odds[team] = thirdround_entries[team] / 10000
        
    for team in fourthround_entries:
        fourthround_odds[team] = fourthround_entries[team] / 10000

    for team in finalist_entries:
        finalist_odds[team] = finalist_entries[team] / 10000

