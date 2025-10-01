import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def main(URL):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                ' Chrome/58.0.3029.110 Safari/537.3'
}

    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    teams_details = []
    
    tables = soup.find_all('table')
    target_table = tables[1].find("tbody")
    teams = target_table.find_all('tr')
    def get_team_info(team):
        details = team.find_all('td')
        return {
            "Rank": details[0].get_text(strip=True),
            "Club": details[1].find("img")["alt"] if details[1].find("img") else details[1].get_text(strip=True),
            "Matches": details[3].get_text(strip=True),
            "W": details[4].get_text(strip=True),
            "D": details[5].get_text(strip=True),
            "L": details[6].get_text(strip=True),
            "Goals": details[7].get_text(strip=True), 
            "+/-": details[8].get_text(strip=True),
            "Pts": details[9].get_text(strip=True),
        }
    
    
    for team in teams:
        team_info = get_team_info(team)
        teams_details.append(team_info)
    df = pd.DataFrame(teams_details)
    df.to_csv(f"final/l_{season}.csv", index=False, encoding="utf-8-sig")
    print("Done")
        
for season in range(2021,2026):    
    URL = f"https://www.transfermarkt.com/premier-league/jahrestabelle/wettbewerb/GB1/saison_id/{season}"
    main(URL)
