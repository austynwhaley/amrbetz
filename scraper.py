import requests
from bs4 import BeautifulSoup
from config import TEAM_STATS_URL

# Fetch the page content
response = requests.get(TEAM_STATS_URL['team_a'])
soup = BeautifulSoup(response.text, 'html.parser')

table_rows = soup.find_all('tr', {'aria-hidden': 'false'})

first_10_players = table_rows[:10]

quarter_back = first_10_players[:1] 
running_backs = first_10_players[1:4]
recievers = first_10_players[4:10]
week = 5

print("Passing:")
for index, row in enumerate(quarter_back):
    player_name = row.find('span', {'class': 'nfl-o-roster__player-name'}).text.strip()
    pass_attempts = row.find_all('td')[1].text.strip()
    passing_yards = row.find_all('td')[3].text.strip()
    touchdowns = row.find_all('td')[6].text.strip()
    interceptions = row.find_all('td')[8].text.strip()

    # Convert stats to integers
    pass_attempts = int(pass_attempts) if pass_attempts.isdigit() else 0
    passing_yards = int(passing_yards) if passing_yards.isdigit() else 0
    touchdowns = int(touchdowns) if touchdowns.isdigit() else 0
    interceptions = int(interceptions) if interceptions.isdigit() else 0

    # Divide each stat by the week number
    pass_attempts_per_week = pass_attempts / week
    passing_yards_per_week = passing_yards / week
    touchdowns_per_week = touchdowns / week
    interceptions_per_week = interceptions / week

    print(f"\nPlayer {index + 1}: {player_name}, \nAverage Passing Attempts: {pass_attempts_per_week}, \nAverage Passing Yards: {passing_yards_per_week}, \nAverage Touchdowns: {touchdowns_per_week}, \nAverage Interceptions: {interceptions_per_week}")

print("\nRushing:")
for index, row in enumerate(running_backs):
    player_name = row.find('span', {'class': 'nfl-o-roster__player-name'}).text.strip()
    rush_attempts = row.find_all('td')[1].text.strip()
    rushing_yards = row.find_all('td')[2].text.strip()
    touchdowns = row.find_all('td')[3].text.strip()

    rush_attempts = int(rush_attempts) if rush_attempts.isdigit() else 0
    rushing_yards = int(rushing_yards) if rushing_yards.isdigit() else 0
    touchdowns = int(touchdowns) if touchdowns.isdigit() else 0

    rush_attempts_per_week = rush_attempts / week
    rushing_yards_per_week = rushing_yards / week
    touchdowns_per_week = touchdowns / week

    print(f"\nPlayer {index + 1}: {player_name}, \nAverage Rushing Attempts: {rush_attempts_per_week}, \nAverage Rushing Yards: {rushing_yards_per_week}, \nAverage Touchdowns: {touchdowns_per_week}")

print("\nReceiving:")
for index, row in enumerate(recievers):
    player_name = row.find('span', {'class': 'nfl-o-roster__player-name'}).text.strip()
    receptions = row.find_all('td')[1].text.strip()
    receiving_yards = row.find_all('td')[2].text.strip()
    touchdowns = row.find_all('td')[5].text.strip()

    receptions = int(receptions) if receptions.isdigit() else 0
    receiving_yards = int(receiving_yards) if receiving_yards.isdigit() else 0
    touchdowns = int(touchdowns) if touchdowns.isdigit() else 0


    receptions_per_week = receptions / week
    receiving_yards_per_week = receiving_yards / week
    touchdowns_per_week = touchdowns / week

    print(f"\nPlayer {index + 1}: {player_name}, \nAverage Receptions: {receptions_per_week}, \nAverage Reciving Yards: {receiving_yards_per_week}, \nAverage Touchdowns: {touchdowns_per_week}")