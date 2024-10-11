import requests
from bs4 import BeautifulSoup
from config import TEAM_STATS_URL
from matchups import *

def get_team_stats(team):
    url = TEAM_STATS_URL.get(team.lower())
    game_week = 5
    if not url:
        print(f"No URL found for {team}")
        return

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sections = soup.find_all('h3', class_='nfl-o-teamstats__title')

    team_stats = {}

    for section in sections:
        title = section.text.strip()

        if title not in ["Passing", "Rushing", "Receiving"]:
            continue

        table = section.find_next('table')
        if not table:
            continue 

        stats = []
        table_rows = table.find_all('tr', {'aria-hidden': 'false'})

        for index, row in enumerate(table_rows):
            player_name = row.find('span', {'class': 'nfl-o-roster__player-name'}).text.strip()

            player_stats = {}
            if title == "Passing":
                pass_attempts = row.find_all('td')[1].text.strip()
                passing_yards = row.find_all('td')[3].text.strip()
                touchdowns = row.find_all('td')[6].text.strip()
                interceptions = row.find_all('td')[8].text.strip()

                pass_attempts = int(pass_attempts) if pass_attempts.isdigit() else 0
                passing_yards = int(passing_yards) if passing_yards.isdigit() else 0
                touchdowns = int(touchdowns) if touchdowns.isdigit() else 0
                interceptions = int(interceptions) if interceptions.isdigit() else 0

                pass_attempts_per_week = pass_attempts / game_week
                passing_yards_per_week = passing_yards / game_week
                touchdowns_per_week = touchdowns / game_week
                interceptions_per_week = interceptions / game_week

                player_stats = {
                    "Player Name": player_name,
                    "Passing Attempts/Week": pass_attempts_per_week,
                    "Passing Yards/Week": passing_yards_per_week,
                    "Touchdowns/Week": touchdowns_per_week,
                    "Interceptions/Week": interceptions_per_week
                }

            elif title == "Rushing":
                rush_attempts = row.find_all('td')[1].text.strip()
                rushing_yards = row.find_all('td')[2].text.strip()
                touchdowns = row.find_all('td')[5].text.strip()

                rush_attempts = int(rush_attempts) if rush_attempts.isdigit() else 0
                rushing_yards = int(rushing_yards) if rushing_yards.isdigit() else 0
                touchdowns = int(touchdowns) if touchdowns.isdigit() else 0

                rush_attempts_per_week = rush_attempts / game_week
                rushing_yards_per_week = rushing_yards / game_week
                touchdowns_per_week = touchdowns / game_week

                player_stats = {
                    "Player Name": player_name,
                    "Rushing Attempts/Week": rush_attempts_per_week,
                    "Rushing Yards/Week": rushing_yards_per_week,
                    "Touchdowns/Week": touchdowns_per_week
                }

            elif title == "Receiving":
                receptions = row.find_all('td')[1].text.strip()
                receiving_yards = row.find_all('td')[2].text.strip()
                touchdowns = row.find_all('td')[5].text.strip()

                receptions = int(receptions) if receptions.isdigit() else 0
                receiving_yards = int(receiving_yards) if receiving_yards.isdigit() else 0
                touchdowns = int(touchdowns) if touchdowns.isdigit() else 0

                receptions_per_week = receptions / game_week
                receiving_yards_per_week = receiving_yards / game_week
                touchdowns_per_week = touchdowns / game_week

                player_stats = {
                    "Player Name": player_name,
                    "Receptions/Week": receptions_per_week,
                    "Receiving Yards/Week": receiving_yards_per_week,
                    "Touchdowns/Week": touchdowns_per_week
                }

            stats.append(player_stats)
        team_stats[title] = stats

    return team_stats

for team1, team2 in w6_matchups:
    print(f"\nStats for {team1} vs. {team2}:")

    team1_stats = get_team_stats(team1)
    team2_stats = get_team_stats(team2)

    print(f"\n{team1} Stats:")
    for category, players in team1_stats.items():
        print(f"\n{category}:")
        for player in players:
            print(player)

    print(f"\n{team2} Stats:")
    for category, players in team2_stats.items():
        print(f"\n{category}:")
        for player in players:
            print(player)
