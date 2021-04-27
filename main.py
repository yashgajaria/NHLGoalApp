# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests

# TODO: Input from user about team and player
# Variable Initialization
# teamInput = "MTL"
# playerInput = "Tyler Toffoli"
# id = 0
# playerId = 0
odds= {}

# specify the url
quote_page = 'https://sportsbook.draftkings.com/leagues/hockey/2022?category=player-props&subcategory=game'

# query the website and return the html to the variable ‘page’
page = urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
name_box = soup.find('div', attrs={'class': 'scorer-7'})

# loop through all games, identify players in the games and the odds to score 
for games in soup.findAll('div', attrs={'class': 'sportsbook-event-accordion__children-wrapper'}):
    players = games.find('div', attrs={'class': 'scorer-7'})
    for player in players:
        allOdds= (player.text.strip().split('+'))
        # if (allOdds[0]==playerInput):
        #     output['odds']=allOdds[3]
        #Populate dictionary with player name and odds
        try:
            odds[allOdds[0]]=allOdds[3]
        except:
            print("error on loading Odds")

#######################################################################
#OLD, retreieving player data from team 
# Get TEAM ID
# URL = "https://statsapi.web.nhl.com/api/v1/teams"

# resp = requests.get(url= URL)
# resp= json.loads(resp.text)
# for team in resp["teams"]:
#     if (team['abbreviation']==teamInput):
#         id = team['id']

# # Get Player ID 
# URL= "https://statsapi.web.nhl.com/api/v1/teams/{}?expand=team.roster".format(id)
# resp = requests.get(url= URL)
# resp= json.loads(resp.text)
# for player in resp['teams'][0]["roster"]["roster"]:
#     if (player['person']['fullName']==playerInput):
#         playerId = player['person']['id']

# # Get Player Stats 
# URL = "https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=statsSingleSeason&season=20202021".format(playerId)
# resp = requests.get(url= URL)
# resp= json.loads(resp.text)
# playerStats= (resp['stats'][0]['splits'][0]['stat'])

# #Format player stats for output
# output['goals']= playerStats['goals']
# output['gp']= playerStats['games']
# output['shooting%']= playerStats['shotPct']

# print(output)

#Collect data from Tim Hortons 
URL = "https://ec2-54-158-170-220.compute-1.amazonaws.com/api/v1/players"
buckets={}

resp = requests.post(url= "https://cors.bridged.cc/http://ec2-54-158-170-220.compute-1.amazonaws.com/api/v1/players", headers={"X-Requested-With": "XMLHttpRequest"})
timmiesSets= json.loads(resp.text)
for sets in timmiesSets['sets']:
    print("SET NUMBER", sets["id"])
    for players in sets['players']:
        ##Load player data/stats
        try:
            URL= "https://api.nhle.com/stats/rest/en/skater/summary?cayenneExp=gameTypeId=2%20and%20seasonId%3E=20202021%20and%20skaterFullName%20likeIgnoreCase%20%22%25" + players['firstName'] + "%20" + players['lastName'] + "%25%22"
            response = requests.get(url =URL, headers={"X-Requested-With": "XMLHttpRequest"})
            playersData= json.loads(response.text)
            playersData=playersData['data'][0]
            name= players['firstName'] + ' ' + players['lastName']

            buckets[name]= {
                "Set": sets['id'],
                "Position": players["position"],
                "Goals": str(playersData["goals"]),
                "GP": str(playersData['gamesPlayed']),
                "S%": str(playersData['shootingPct']),
                "Odds": odds[name]
            }
        # print (playersData)
        # print (players['firstName'] +" " + players["lastName"] + " " + players["position"] + " Goals " + str(playersData["goals"]) + " GP: " + str(playersData["gamesPlayed"]) + " S% " + str(playersData['shootingPct']) + " TOI: " + str(playersData["timeOnIcePerGame"]))
        except:
            print(players['firstName'] + " " + players["lastName"] + " STATS NOT AVAILABLE RIGHT NOW")
print(buckets)