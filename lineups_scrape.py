#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:21:51 2024

@author: andy
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

def parse_pitcher_stats(stats_str):
    """Parse pitcher stats string into record and ERA."""
    if not stats_str:
        return '', ''
    
    # Extract record (e.g., "4-2") and ERA (e.g., "2.92")
    record_match = re.search(r'(\d+-\d+)', stats_str)
    era_match = re.search(r'(\d+\.\d+)\s*ERA', stats_str)
    
    record = record_match.group(1) if record_match else ''
    era = era_match.group(1) if era_match else ''
    
    return record, era

def parse_weather_info(weather_div):
    """Parse weather information from the weather div."""
    if not weather_div:
        return '', '', '', ''
    
    # Get weather condition from the image alt text
    weather_icon = weather_div.find('img', class_='lineup__weather-icon')
    weather_condition = weather_icon.get('alt', '').replace('-', ' ').title() if weather_icon else ''
    
    # Get weather text which contains rain probability, temperature, and wind
    weather_text = weather_div.find('div', class_='lineup__weather-text')
    if weather_text:
        text = weather_text.text.strip()
        # Extract rain probability
        rain_match = re.search(r'(\d+)%', text)
        rain_prob = rain_match.group(1) if rain_match else '0'
        
        # Extract temperature
        temp_match = re.search(r'(\d+)°', text)
        temperature = temp_match.group(1) if temp_match else ''
        
        # Extract wind speed
        wind_match = re.search(r'Wind\s+(\d+)\s+mph', text)
        wind_speed = wind_match.group(1) if wind_match else ''
    else:
        rain_prob = ''
        temperature = ''
        wind_speed = ''
    
    return weather_condition, rain_prob, temperature, wind_speed

def get_daily_lineups(html=None):
    # URL for RotoWire MLB daily lineups
    url = "https://www.rotowire.com/baseball/daily-lineups.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        if html is None:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            html = response.text
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all games
        games = soup.find_all('div', class_='lineup')
        print(f"Found {len(games)} games.")
        all_lineups = []
        
        # Get current timestamp for load_ts
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for game in games:
            # Get team abbreviations
            abbrs = game.select('.lineup__abbr')
            if len(abbrs) != 2:
                continue  # skip if not a valid game block
            away_abbr = abbrs[0].text.strip()
            home_abbr = abbrs[1].text.strip()
            
            # Get starting pitchers
            away_pitcher = game.select_one('ul.lineup__list.is-visit li.lineup__player-highlight')
            home_pitcher = game.select_one('ul.lineup__list.is-home li.lineup__player-highlight')
            
            away_pitcher_name = away_pitcher.find('a').text.strip() if away_pitcher else ''
            away_pitcher_throws = away_pitcher.find('span', class_='lineup__throws').text.strip() if away_pitcher else ''
            away_pitcher_stats = away_pitcher.find('div', class_='lineup__player-highlight-stats').text.strip() if away_pitcher else ''
            away_pitcher_record, away_pitcher_era = parse_pitcher_stats(away_pitcher_stats)
            
            home_pitcher_name = home_pitcher.find('a').text.strip() if home_pitcher else ''
            home_pitcher_throws = home_pitcher.find('span', class_='lineup__throws').text.strip() if home_pitcher else ''
            home_pitcher_stats = home_pitcher.find('div', class_='lineup__player-highlight-stats').text.strip() if home_pitcher else ''
            home_pitcher_record, home_pitcher_era = parse_pitcher_stats(home_pitcher_stats)
            
            # Get lineup status
            away_status = game.select_one('ul.lineup__list.is-visit li.lineup__status')
            home_status = game.select_one('ul.lineup__list.is-home li.lineup__status')
            
            away_lineup_status = 'Confirmed' if away_status and 'is-confirmed' in away_status.get('class', []) else 'Expected'
            home_lineup_status = 'Confirmed' if home_status and 'is-confirmed' in home_status.get('class', []) else 'Expected'
            
            # Get weather information
            weather_div = game.select_one('div.lineup__weather')
            weather_condition, rain_prob, temperature, wind_speed = parse_weather_info(weather_div)
            
            # Get away players
            away_players = game.select('ul.lineup__list.is-visit li.lineup__player')
            for idx, player in enumerate(away_players, 1):
                pos = player.find('div', class_='lineup__pos')
                name = player.find('a')
                bats = player.find('span', class_='lineup__bats')
                all_lineups.append({
                    'team': away_abbr,
                    'opposing_team': home_abbr,
                    'home_away': 'away',
                    'batting_order': idx,
                    'position': pos.text.strip() if pos else '',
                    'player_name': name.text.strip() if name else '',
                    'bats': bats.text.strip() if bats else '',
                    'opposing_pitcher': home_pitcher_name,
                    'opposing_pitcher_throws': home_pitcher_throws,
                    'opposing_pitcher_record': home_pitcher_record,
                    'opposing_pitcher_era': home_pitcher_era,
                    'lineup_status': away_lineup_status,
                    'game_date': datetime.now().strftime('%Y-%m-%d'),
                    'weather_condition': weather_condition,
                    'rain_probability': rain_prob,
                    'temperature_f': temperature,
                    'wind_speed': wind_speed,
                    'load_ts': current_timestamp
                })
            
            # Get home players
            home_players = game.select('ul.lineup__list.is-home li.lineup__player')
            for idx, player in enumerate(home_players, 1):
                pos = player.find('div', class_='lineup__pos')
                name = player.find('a')
                bats = player.find('span', class_='lineup__bats')
                all_lineups.append({
                    'team': home_abbr,
                    'opposing_team': away_abbr,
                    'home_away': 'home',
                    'batting_order': idx,
                    'position': pos.text.strip() if pos else '',
                    'player_name': name.text.strip() if name else '',
                    'bats': bats.text.strip() if bats else '',
                    'opposing_pitcher': away_pitcher_name,
                    'opposing_pitcher_throws': away_pitcher_throws,
                    'opposing_pitcher_record': away_pitcher_record,
                    'opposing_pitcher_era': away_pitcher_era,
                    'lineup_status': home_lineup_status,
                    'game_date': datetime.now().strftime('%Y-%m-%d'),
                    'weather_condition': weather_condition,
                    'rain_probability': rain_prob,
                    'temperature_f': temperature,
                    'wind_speed': wind_speed,
                    'load_ts': current_timestamp
                })
        
        df = pd.DataFrame(all_lineups)
        if len(df) > 0:
            # Reorder columns to ensure load_ts is last
            cols = [col for col in df.columns if col != 'load_ts'] + ['load_ts']
            df = df[cols]
            
            filename = f"mlb_lineups_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filename, index=False)
            print(f"Lineup data saved to {filename}")
        else:
            print("No lineup data found!")
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # For testing, you can load the saved HTML file instead of making a request
    # with open('MLB Daily Lineups _ RotoWire.html', 'r', encoding='utf-8') as f:
    #     html = f.read()
    #     lineups_df = get_daily_lineups(html)
    #     print(lineups_df.head())
    # else:
    time.sleep(1)
    lineups_df = get_daily_lineups()
    if lineups_df is not None and not lineups_df.empty:
        print("\nFirst few rows of the lineup data:")
        print(lineups_df.head())
