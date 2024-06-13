from bs4 import BeautifulSoup
import os
import requests

# Directory to save parsed song content
os.makedirs("parsed_songs", exist_ok=True)


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def parse_song_page(content):
    soup = BeautifulSoup(content, "html.parser")

    # Extract the relevant texts
    transliteration_div = soup.find("div", id="transliteration")
    transliteration = (
        transliteration_div.get_text(separator="\n").strip()
        if transliteration_div
        else ""
    )

    hebrew_div = soup.find("div", id="hebrew")
    hebrew = hebrew_div.get_text(separator="\n").strip() if hebrew_div else ""

    translation_div = soup.find("div", id="translation")
    translation = (
        translation_div.get_text(separator="\n").strip() if translation_div else ""
    )

    return transliteration, hebrew, translation


def save_parsed_content(transliteration, hebrew, translation, song_id):
    with open(f"parsed_songs/song_{song_id}.txt", "w", encoding="utf-8") as file:
        file.write(
            f"Transliteration:\n{transliteration}\n\nHebrew:\n{hebrew}\n\nTranslation:\n{translation}\n"
        )


# parse each song stored in /song_pages
for song_file in os.listdir("song_pages"):
    if song_file.endswith(".html"):
        song_id = song_file.split("_")[-1].split(".")[0]
        print(f"Parsing song ID {song_id}")
        with open(f"song_pages/{song_file}", "rb") as file:
            song_content = file.read()
        transliteration, hebrew, translation = parse_song_page(song_content)
        save_parsed_content(transliteration, hebrew, translation, song_id)

print("All song pages have been parsed and saved.")
