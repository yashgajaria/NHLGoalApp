# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests

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
        # try:
        #     print(allOdds[0], allOdds[3])
        # except:
        #     print("error")


# name = name_box.text.strip() # strip() is used to remove starting and trailing
# print (name)

# url = requests.get(quote_page)
# tags = BeautifulSoup(page, 'html.parser')
# for tag in tags.findAll('div', attrs={'class': 'scorer-7'}):
#     # new_tag = tag.find('div', attrs={'class': 'scorer-7'})
#     print(tag)

## Given a team and player return stats
teamInput = "TOR"
playerInput = "Jason Spezza"
id = 0
playerId = 0

# Get TEAM ID
URL = "https://statsapi.web.nhl.com/api/v1/teams"

resp = requests.get(url= URL)
resp= json.loads(resp.text)
for team in resp["teams"]:
    if (team['abbreviation']==teamInput):
        id = team['id']
# print(resp.text)

# Get Player ID 
URL= "https://statsapi.web.nhl.com/api/v1/teams/{}?expand=team.roster".format(id)
resp = requests.get(url= URL)
resp= json.loads(resp.text)
for player in resp['teams'][0]["roster"]["roster"]:
    if (player['person']['fullName']==playerInput):
        playerId = player['person']['id']

# Get Player Stats 
URL = "https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=statsSingleSeason&season=20202021".format(playerId)
resp = requests.get(url= URL)
resp= json.loads(resp.text)
print(resp['stats'][0]['splits'][0]['stat'])
print (playerId)


