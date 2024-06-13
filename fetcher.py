import os
import requests
import re

from bs4 import BeautifulSoup

# Directory to save raw song content
os.makedirs("song_pages", exist_ok=True)


# Function to fetch a page
def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.content


# Function to parse the main page and extract song links
def parse_main_page(content):
    soup = BeautifulSoup(content, "html.parser")
    song_links = []
    list_items = soup.find_all("li")
    for item in list_items:
        link = item.find("a", href=True)
        if link:
            url = "https://zemirotdatabase.org/" + link["href"]
            if re.match(r"https://zemirotdatabase\.org/view_song\.php\?id=\d+", url):
                song_links.append(url)
    return song_links


# Function to save content to a file
def save_content_to_file(content, filename):
    with open(filename, "wb") as file:
        file.write(content)


# Base URL for the song index
base_url = "https://zemirotdatabase.org/song_index.php"

# Fetch the main page
main_page_content = fetch_page(base_url)

# Parse the main page to extract song links
song_links = parse_main_page(main_page_content)

for sl in song_links:
    print(sl)

# Iterate over each song link and fetch the content
for song_url in song_links:
    song_id = song_url.split("=")[-1]
    song_page_content = fetch_page(song_url)
    # Save the content to a file named after the song ID
    save_content_to_file(song_page_content, f"song_pages/song_{song_id}.html")
    print(f"Saved content for song ID {song_id}")

print("All song pages have been saved.")
