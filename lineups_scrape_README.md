# RotoWire MLB Lineups Scraper

A Python script that scrapes MLB daily lineups data from RotoWire, including player information, weather conditions, and game details.

## Features

- Scrapes daily MLB lineups from RotoWire
- Captures comprehensive game information including:
  - Team lineups (home and away)
  - Player details (name, position, batting order, batting hand)
  - Starting pitcher information (name, record, ERA, throwing hand)
  - Weather conditions (temperature, wind speed, rain probability)
  - Lineup status (confirmed/expected)
- Saves data to a CSV file with timestamp

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - beautifulsoup4
  - pandas

## Installation

1. Clone this repository or download the script
2. Install required packages:
```bash
pip install requests beautifulsoup4 pandas
```

## Usage

Run the script directly:
```bash
python lineups_scrape.py
```

The script will:
1. Fetch the latest MLB lineups from RotoWire
2. Process and parse the data
3. Save the results to a CSV file named `mlb_lineups_YYYYMMDD.csv`

## Output Format

The script generates a CSV file with the following columns:

- `team`: Team abbreviation
- `opposing_team`: Opposing team abbreviation
- `home_away`: Whether the team is home or away
- `batting_order`: Player's position in batting order
- `position`: Player's fielding position
- `player_name`: Player's full name
- `bats`: Player's batting hand (L/R/S)
- `opposing_pitcher`: Name of the opposing team's starting pitcher
- `opposing_pitcher_throws`: Opposing pitcher's throwing hand
- `opposing_pitcher_record`: Opposing pitcher's win-loss record
- `opposing_pitcher_era`: Opposing pitcher's ERA
- `lineup_status`: Whether the lineup is confirmed or expected
- `game_date`: Date of the game
- `weather_condition`: Current weather conditions
- `rain_probability`: Probability of rain (percentage)
- `temperature_f`: Temperature in Fahrenheit
- `wind_speed`: Wind speed in mph
- `load_ts`: Timestamp when the data was scraped

## Notes

- The script includes a 1-second delay between requests to avoid overwhelming the server
- Weather information is scraped from the game's weather section
- Lineup status indicates whether the lineup is confirmed or expected
- The script can be modified to use a saved HTML file for testing purposes

## Author

Created by Andy

## License

This project is open source and available under the MIT License. 