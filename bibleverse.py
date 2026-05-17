#!/usr/bin/env python3
"""
Bible Verse CLI- fetches and displays a random verse from the web or from a local database as specified by the user.
Usage: 

bibleverse.py <translation>

translation can be one of the following: WEB, KJV, AKJV, ASV, ACV
If no translation is specified, the web version is used.
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

# Main Program

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

def print_verse(book, chapter, verse, text):
    """Prints the verse to the console"""
    width = int(shutil.get_terminal_size().columns)
    text_width = len(text)
    if text_width < width:
        width = text_width + 2
    border = "=" * width
    print(f"\n{border}")
    print(f'"{text}"')
    print(f"- {book} {chapter}:{verse}")
    print(f'{border}\n')

def get_random_verse_from_db(translation):
    # Connect to your local SQLite database
    conn = sqlite3.connect(os.path.join(DATA_DIR, f"{translation}.db"))
    cursor = conn.cursor()
    
    # SQL query to grab exactly one random verse
    # (Note: table and column names will depend on the specific SQLite database)
    # This program uses databases provided by https://github.com/scrollmapper/sqlite-bible-database
    
    query = f"SELECT b.name AS book_name,v.chapter,v.verse,v.text FROM {translation}_verses v JOIN {translation}_books b ON v.book_id = b.id ORDER BY RANDOM() LIMIT 1;"
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            book, chapter, verse, text = result
            print_verse(book, chapter, verse, text)
            
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
        
        print_verse(book, chapter, verse, text)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching verse: {e}")
        print("Please try again later.  The server may be down.  ")
        print("Alternatively, you can use one of the local databases by specifying a translation.")    
        sys.exit(1)

if __name__ == "__main__":

    # get column width to center output
    width = int(shutil.get_terminal_size().columns)
    border = "=" * width
    # check to see if translation exists in data directory
    avail_versions = []
    for db_file in os.listdir(DATA_DIR):
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
 
            print(f"\nWARNING: Unknown translation: {sys.argv[1]}.\n")
            print(f"Valid translations are: {', '.join(avail_versions)}.  Defaulting to web lookup.\n")
            get_random_web_verse()
            sys.exit(0)
        
    else:
        print("\nWARNING: No translation specified.\n")
        print(f"Command syntax: {sys.argv[0]} [translation]")
        print(f"Please specify a translation.  Valid translations are: {', '.join(avail_versions)}")
        print(f"Example: {sys.argv[0]} KJV\n")
        sys.exit(0)    