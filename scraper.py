import requests
import tweepy
from bs4 import BeautifulSoup
from utils.config import TEAM_STATS_URL
from utils.matchups import *
from utils.helpers import *
from utils.keys import *
import time
import random
from requests.exceptions import RequestException

# Initialize Twitter client with rate limit handling
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret, wait_on_rate_limit=True)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


CACHE_TIMEOUT = 60 * 60 

cache = load_cache()

def is_cache_valid(team, current_time):
    if team in cache:
        cached_time = cache[team].get('time')
        if current_time - cached_time < CACHE_TIMEOUT:
            return True
    return False

def get_team_stats(team):
    current_time = time.time()

    if is_cache_valid(team, current_time):
        print(f"Using cached stats for {team}")
        return cache[team]['stats']

    url = TEAM_STATS_URL.get(team.lower())
    current_week = get_current_game_week()
    if current_week is None:
        print(f"No active game week found for today's date.")
        return {}
    game_week = current_week - 1
    if not url:
        print(f"No URL found for {team}")
        return {}

    try:
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
    except RequestException as e:
        print(f"Failed to fetch stats for {team}: {e}")
        return {}

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
                receptions = int_or_zero(row.find_all('td')[1].text.strip())
                receiving_yards = int_or_zero(row.find_all('td')[2].text.strip())
                touchdowns = int_or_zero(row.find_all('td')[5].text.strip())

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
                rush_attempts = int_or_zero(row.find_all('td')[1].text.strip())
                rushing_yards = int_or_zero(row.find_all('td')[2].text.strip())
                touchdowns = int_or_zero(row.find_all('td')[5].text.strip())

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
                pass_attempts = int_or_zero(row.find_all('td')[1].text.strip())
                passing_yards = int_or_zero(row.find_all('td')[3].text.strip())
                touchdowns = int_or_zero(row.find_all('td')[6].text.strip())
                interceptions = int_or_zero(row.find_all('td')[8].text.strip())

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

    # save stats to cache
    cache[team] = {
        'stats': team_stats,
        'time': current_time
    }
    save_cache(cache)

    return team_stats

def int_or_zero(value):
    """Helper function to safely convert strings to integers, returns 0 if not valid."""
    return int(value) if value.isdigit() else 0

current_week, current_matchups = get_current_week_matchups()

# tweet builder
if current_week:
    print(f"\nProcessing matchups for Week {current_week}:\n")
    for team1, team2 in current_matchups:
        team1_stats = get_team_stats(team1)
        team2_stats = get_team_stats(team2)

        # sending tweets for each team
        for team, stats in [(team1, team1_stats), (team2, team2_stats)]:
            tweet_text = f"\n{team.upper()} WEEKLY AVERAGE STATS\n"

            for category, players in stats.items():
                category_output = f"{category}:\n"
                for player in players:
                    category_output += f"- {player['Player Name']}: "
                    category_output += ", ".join([f"{key}: {value}" for key, value in player.items() if key != "Player Name"]) + "\n"

                tweet_text += category_output + "\n"

            print(tweet_text.strip())

            # randomized sleep to avoid rate limiting
            # time.sleep(random.uniform(4.5, 6.5))
            # try:
            #     client.create_tweet(text=tweet_text.strip())
            # except tweepy.TweepError as e:
            #     print(f"Failed to send tweet: {e}")
            
            time.sleep(random.uniform(4.5, 6.5))
else:
    print("No matchups found for the current date.")

# client.create_tweet(text="ALL DONE, UR WELCOME - AMR")
