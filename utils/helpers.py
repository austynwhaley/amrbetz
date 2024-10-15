from datetime import date
from utils.matchups import *
import os
import json

def get_current_week_matchups():
    today = date.today()
    for week, (start_date, end_date) in date_ranges_by_week.items():
        if start_date <= today <= end_date:
            return week, matchups_by_week[week][::-1]
    return None, [] 

def get_current_game_week():
    today = date.today()

    for week, (start_date, end_date) in date_ranges_by_week.items():
        if start_date <= today <= end_date:
            return week
    
    return None 

CACHE_FILE = 'team_stats_cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache_data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f)