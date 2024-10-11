import requests
from bs4 import BeautifulSoup
from config import TEAM_STATS_URL
from matchups import *

# Function to fetch and display stats for each team
def get_team_stats(team):
    url = TEAM_STATS_URL.get(team.lower())
    if not url:
        print(f"No URL found for {team}")
        return

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all sections (h3 tags) and corresponding tables
    sections = soup.find_all('h3', class_='nfl-o-teamstats__title')

    team_stats = {}

    # Loop through each section and process only the relevant ones (Passing, Rushing, Receiving)
    for section in sections:
        title = section.text.strip()

        # Skip sections that are not Passing, Rushing, or Receiving
        if title not in ["Passing", "Rushing", "Receiving"]:
            continue

        # Find the table immediately following the section
        table = section.find_next('table')
        if not table:
            continue  # If no table is found, skip to next section

        stats = []
        # Extract table rows (players)
        table_rows = table.find_all('tr', {'aria-hidden': 'false'})

        # Process each player based on their role in the section
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

                pass_attempts_per_week = pass_attempts / 5
                passing_yards_per_week = passing_yards / 5
                touchdowns_per_week = touchdowns / 5
                interceptions_per_week = interceptions / 5

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

                rush_attempts_per_week = rush_attempts / 5
                rushing_yards_per_week = rushing_yards / 5
                touchdowns_per_week = touchdowns / 5

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

                receptions_per_week = receptions / 5
                receiving_yards_per_week = receiving_yards / 5
                touchdowns_per_week = touchdowns / 5

                player_stats = {
                    "Player Name": player_name,
                    "Receptions/Week": receptions_per_week,
                    "Receiving Yards/Week": receiving_yards_per_week,
                    "Touchdowns/Week": touchdowns_per_week
                }

            stats.append(player_stats)
        team_stats[title] = stats

    return team_stats

# Iterate through matchups and display stats for both teams
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
