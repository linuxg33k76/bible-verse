#!/usr/bin/env python3
"""
Bible Verse of the Day - fetches and displays a random verse
"""


import sys
import os
import subprocess
import shutil

try:
    import requests
except ImportError:
    print("The 'requests' library is not installed. Installing it automatically...", file=sys.stderr)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    except Exception as e:
        print(f"Failed to install 'requests': {e}", file=sys.stderr)
        print("Please install it manually by running: pip install requests", file=sys.stderr)
        sys.exit(1)
        
from requests import exceptions
try:
    import sqlite3
except ImportError:
    print("The 'sqlite3' library is not installed. Installing it automatically...", file=sys.stderr)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sqlite3"])
        import sqlite3
    except Exception as e:
        print(f"Failed to install 'sqlite3': {e}", file=sys.stderr)
        print("Please install it manually by running: pip install sqlite3", file=sys.stderr)
        sys.exit(1)

def get_random_verse_from_db(translation):
    # Connect to your local SQLite database
    conn = sqlite3.connect(f"data/{translation}.db")
    cursor = conn.cursor()
    
    # SQL query to grab exactly one random verse
    # (Note: table and column names will depend on the specific SQLite file you download)
    # query = "SELECT book_id, chapter, verse, text FROM kjv_verses ORDER BY RANDOM() LIMIT 1;"
    query = f"SELECT b.name AS book_name,v.chapter,v.verse,v.text FROM {translation}_verses v JOIN {translation}_books b ON v.book_id = b.id ORDER BY RANDOM() LIMIT 1;"
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            book, chapter, verse, text = result
            print(f'\n{border}')
            print(f'"{text}"')
            print(f"- {book} {chapter}:{verse}")
            print(f'{border}\n')
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def get_random_web_verse():
    # The /random endpoint automatically pulls a random verse
    # "web" stands for World English Bible, but you can use "kjv" or others
    url = "https://bible-api.com/data/web/random"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()
        
        # Parse the JSON response
        book = data['random_verse']['book']
        chapter = data['random_verse']['chapter']
        verse = data['random_verse']['verse']
        text = data['random_verse']['text'].strip()
        
        print("\n" + border)
        print(f'"{text}"')
        print(f"- {book} {chapter}:{verse}")
        print(border + "\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching verse: {e}")

        # Look up from internal database of verses

        get_random_verse_from_db()

if __name__ == "__main__":

    # get column width to center output
    width = int(shutil.get_terminal_size().columns)
    border = "=" * width
    # check to see if translation exists in data directory
    avail_versions = []
    for db_file in os.listdir("data"):
        if db_file.endswith(".db"):
            avail_versions.append(db_file.replace(".db", "").upper())

    # validate user arguments
    if len(sys.argv) > 1:
        if sys.argv[1].upper() in avail_versions and sys.argv[1].upper() != "WEB":
            translation = sys.argv[1].upper()
            get_random_verse_from_db(translation)
        elif sys.argv[1].upper() == "WEB":
            get_random_web_verse()
            sys.exit(0)
        else:
            print(f"\n{border}")
            print(f"\tWARNING: Unknown translation: {sys.argv[1]}.  Valid translations are: {', '.join(avail_versions)}.  Defaulting to web lookup...")
            get_random_web_verse()
            sys.exit(0)
        
    else:
        print(f"\n{border}")
        print(f"You did not specify a translation.  Command syntax: {sys.argv[0]} [translation]")
        print(f"Please specify a translation.  Valid translations are: {', '.join(avail_versions)}")
        print(f"Example: {sys.argv[0]} KJV")
        print(f'{border}\n')
        sys.exit(0)    