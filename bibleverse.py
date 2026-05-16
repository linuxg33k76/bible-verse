#!/usr/bin/env python3
"""
Bible Verse of the Day - fetches and displays a random verse
"""

import requests
import json
import random

API_URL = "https://labs.bible.com/api/v2/verses.choicelist/json?limit=1000"

def get_verses():
    """Fetch Bible verses from the API"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching verses: {e}")
        return None

def display_verse(verses):
    """Display a random verse"""
    if not verses:
        print("No verses available.")
        return

    verse = random.choice(verses)
    
    book = verse.get('book', {}).get('name', '')
    chapter = verse.get('chapter_number', '')
    verse_num = verse.get('verse_number', '')
    text = verse.get('verse_text', '')
    
    print("\n" + "="*60)
    print(f"📖 {book} {chapter}:{verse_num}")
    print("="*60)
    print(f"\n{text}")
    print("\n" + "="*60)

def main():
    """Main function"""
    print("Fetching Bible verse of the day...")
    verses = get_verses()
    display_verse(verses)

if __name__ == "__main__":
    main()