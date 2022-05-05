from time import time
import requests
import json
from datetime import date
from datetime import datetime

def FindGamesToday(GameList,date):
    return [game for game in GameList if date in game]

def ChessGames(username):

    currentDay = date.today()
    currentMonth = str(currentDay.month)
    currentYear = str(currentDay.year)
    currentDay = str(currentDay.day)
    if len(currentMonth) == 1: currentMonth = str(0) + str(currentMonth)
    if len(currentDay) == 1: currentDay = str(0) + str(currentDay)
    baseURL = "https://api.chess.com/pub/player/"
    nameURL = baseURL + username + "/"
    gamesURL = nameURL + "games/" + str(currentYear) + "/" + str(currentMonth)


    games = requests.get(gamesURL)
    gamesJson = games.json()

    json_string = json.dumps(gamesJson)
    rawGameList = json_string.split("...")
    dateString = r"[Date \""+currentYear+ "."+currentMonth+"." +currentDay+r"\"]"
    TodayGames = FindGamesToday(rawGameList,dateString)
    return len(TodayGames)


def ChessOnline(username):
    baseURL = "https://api.chess.com/pub/player/"
    userURL = baseURL + username + "/"
    response = requests.get(userURL)
    userJson = response.json()
    userString = json.dumps(userJson)
    startIndex = userString.index("\"last_online\":") + 15
    endIndex = userString.index("joined") - 3
    lastOnline = int(userString[startIndex:endIndex])
    currentTime = datetime.utcnow()

    timeLastOnline = datetime.utcfromtimestamp(lastOnline).strftime('%Y-%m-%d %H:%M')
    currentTime = currentTime.strftime('%Y-%m-%d %H:%M')

    print("Last Online: ",timeLastOnline)
    print("Current Time: ",currentTime)

    online = False

    return online

def GetRanking(username):
    baseURL = "https://api.chess.com/pub/player/"
    statsURL = baseURL + username + "/stats"
    response = requests.get(statsURL)
    statsJson = response.json()
    statsString = json.dumps(statsJson)

    startIndex = statsString.index("\"rating\":") + 10
    endIndex = statsString.index("date") - 3
    ranking = statsString[startIndex:endIndex]

    return ranking

