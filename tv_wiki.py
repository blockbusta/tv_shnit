import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--show", type=str, help="The name of the TV show")
parser.add_argument("--season", type=int, help="The TV show season number")
args = parser.parse_args()

tv_show_name = args.show
season_number = args.season

def fetch_episodes(tv_show_name, season_number):
    # Replace spaces in the TV show name with underscores and convert to lowercase
    tv_show_name = tv_show_name.replace(" ", "_")

    # Construct the URL for the Wikipedia page for the season
    url = f"https://en.wikipedia.org/wiki/{tv_show_name}_(season_{season_number})"
    print(url)
    # Send a request to the URL and parse the HTML response
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find the table containing the list of episodes
    episode_table = soup.find('table', class_='wikiepisodetable')

    # if theres a single page for all episodes from all the show's seasons:
    if episode_table is None:
        url = "https://en.wikipedia.org/wiki/List_of_{tv_show_name}_episodes"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        episode_table = soup.findAll('table', class_='wikiepisodetable')
        print(soup)

    # Extract the episode names and numbers from the table
    episodes = []

    # episode table column id's:
    ep_number = 0
    ep_title = 1
    director = 2
    writer = 3
    original_air_date = 4
    prod_code = 5
    rating = 6

    for row in episode_table.find_all('tr')[1:]:
        if len(row.find_all('td')) <= 1:
            continue
        episode_number_cell = row.find_all('td')[ep_number]
        episode_number = episode_number_cell.text.strip()
        episode_name_cell = row.find_all('td')[ep_title]
        episode_name_link = episode_name_cell.find('href')
        if episode_name_link:
            episode_name = episode_name_link.text.strip()
        else:
            episode_name = episode_name_cell.text.strip()
        air_date_cell = row.find_all('td')[original_air_date]
        if "TBA" in air_date_cell.text.strip():
            continue
        air_date = air_date_cell.text.strip().split("(")[1].split(")")[0]
        if air_date[0:3] == "199" or air_date[0:3] == "200" or air_date[0:3] == "201" or air_date[0:3] == "202":
            air_date = air_date.split("-")
            air_date.reverse()
            print(air_date)
            air_date = "/".join(air_date)
        episodes.append({'episode_number': episode_number, 'episode_name': episode_name, 'air_date': air_date})

    return episodes

# Prompt the user to enter the TV show name and season number
if tv_show_name is None:
    tv_show_name = input("Enter the name of the TV show: ")

if season_number is None:
    season_number = input("Enter the season number: ")

# Fetch the list of episodes in the season from Wikipedia
episodes = fetch_episodes(tv_show_name, season_number)

# Iterate over the episodes and print out the information for each one
for episode in episodes:
    episode_number = episode['episode_number']
    episode_name = episode['episode_name']
    air_date = episode['air_date']
    output_string = tv_show_name + " S" + str(season_number).zfill(2) + "E" + str(episode_number).zfill(2) + " " + episode_name + " (" + air_date + ")"
    print(output_string)
    search_query = tv_show_name.replace(" ", "+") + "+S" + str(season_number).zfill(2) + "E" + str(episode_number).zfill(2) + "+1080p"
    search_api=f"https://rarbgtor.org/torrents.php?search={search_query}&order=seeders&by=DESC"
    print(search_api + "\n")
