# utils/helpers.py

def clean_stat(stat):
    """Helper function to clean stats (e.g., remove commas, convert to int)."""
    return int(stat.replace(',', ''))

def calculate_diff(stat_a, stat_b):
    """Helper to calculate the difference between two stats."""
    return stat_a - stat_b
