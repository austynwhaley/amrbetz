import requests
import tweepy
from bs4 import BeautifulSoup
from utils.config import TEAM_STATS_URL
from utils.matchups import *
from utils.helpers import *
from keys import *
import time

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def get_team_stats(team):
    url = TEAM_STATS_URL.get(team.lower())

    current_week = get_current_game_week()
    if current_week is None:
        print(f"No active game week found for today's date.")
        return {}
    game_week = current_week - 1
    if not url:
        print(f"No URL found for {team}")
        return {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sections = soup.find_all('h3', class_='nfl-o-teamstats__title')

    team_stats = {}

    for section in sections:
        title = section.text.strip()

        if title not in ["Receiving", "Rushing", "Passing"]:
            continue

        table = section.find_next('table')
        if not table:
            continue 

        stats = []
        table_rows = table.find_all('tr', {'aria-hidden': 'false'})

        for row in table_rows:
            player_name = row.find('span', {'class': 'nfl-o-roster__player-name'}).text.strip()

            player_stats = {}
            if title == "Receiving":
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
                    "Rec": round(receptions_per_week, 1),
                    "Yds": round(receiving_yards_per_week, 1),
                    "TD": round(touchdowns_per_week, 1)
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
                    "Att": round(rush_attempts_per_week, 1),
                    "Yds": round(rushing_yards_per_week, 1),
                    "TD": round(touchdowns_per_week, 1)
                }

            elif title == "Passing":
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
                    "Att": round(pass_attempts_per_week, 1),
                    "Yds": round(passing_yards_per_week, 1),
                    "TD": round(touchdowns_per_week, 1),
                    "Int": round(interceptions_per_week, 1)
                }

            stats.append(player_stats)
        team_stats[title] = stats

    return team_stats

current_week, current_matchups = get_current_week_matchups()

if current_week:
    print(f"\nProcessing matchups for Week {current_week}:\n")
    client.create_tweet(text="ALL DONE, UR WELCOME - AMR")
    for team1, team2 in current_matchups:
        team1_stats = get_team_stats(team1)
        team2_stats = get_team_stats(team2)

        # Sending tweets for each team
        for team, stats in [(team1, team1_stats), (team2, team2_stats)]:
            tweet_text = f"{team.upper()} STATS\n"

            # Grouped tweets for each category
            for category, players in stats.items():
                category_output = f"{category}:\n"
                for player in players:
                    category_output += f"- {player['Player Name']}: "
                    category_output += ", ".join([f"{key}: {value}" for key, value in player.items() if key != "Player Name"]) + "\n"
                
                tweet_text += category_output + "\n"

            # Print the final tweet text for each team
            print('tweet', tweet_text.strip())
            # Uncomment below line to send the tweet
            time.sleep(5) 
            client.create_tweet(text=tweet_text.strip())
            time.sleep(5) 
else:
    print("No matchups found for the current date.")

client.create_tweet(text="ALL DONE, UR WELCOME - AMR")
