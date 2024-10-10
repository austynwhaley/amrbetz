import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import TEAM_STATS_URL, PLAYER_STATS_URL

def get_team_stats(team_url):
    response = requests.get(team_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    stats = {}
    stats['total_yards'] = soup.find('div', {'id': 'total_yards'}).text
    stats['passing_yards'] = soup.find('div', {'id': 'passing_yards'}).text
    stats['rushing_yards'] = soup.find('div', {'id': 'rushing_yards'}).text
    return stats

def get_player_stats(player_url):
    response = requests.get(player_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    players_stats = []
    table = soup.find('table', {'class': 'player-stats-table'})
    for row in table.find_all('tr')[1:]:
        player = row.find_all('td')
        players_stats.append({
            'name': player[0].text,
            'position': player[1].text,
            'passing_yards': player[2].text,
            'rushing_yards': player[3].text,
            'receiving_yards': player[4].text,
        })
    return players_stats

def compare_team_stats(team_a_stats, team_b_stats):
    df = pd.DataFrame([team_a_stats, team_b_stats], index=['Team A', 'Team B'])
    df['Yards Difference'] = df['total_yards'].diff().iloc[-1]
    print(df)

# URLs from config.py
team_a_stats = get_team_stats(TEAM_STATS_URL['team_a'])
team_b_stats = get_team_stats(TEAM_STATS_URL['team_b'])

compare_team_stats(team_a_stats, team_b_stats)
