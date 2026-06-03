import random

import requests
from words import PAIRED_CATEGORIES, API_CATEGORIES
from word_tracker import get_unused_words, mark_word_as_used

def get_hint(word: str) -> str | None:
    """
    https://www.datamuse.com/api/
    Check the documentation. This function takes the word
    and returns a hint related to that word.
    """
    url = f"https://api.datamuse.com/words?rel_trg={word}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return random.choice(data)["word"] if data else None
    except requests.RequestException:
        print("Network error, couldn't fetch hint word")
        return None
    
def get_word_from_category(category: str) -> tuple[str, str] | None:
    if category in PAIRED_CATEGORIES:
        all_words = list(PAIRED_CATEGORIES[category].keys())
        unused = get_unused_words(category, all_words)
        word = random.choice(unused)
        hint = PAIRED_CATEGORIES[category][word]
        mark_word_as_used(category, word)
        return word, hint

    elif category in API_CATEGORIES:
        all_words = API_CATEGORIES[category]
        unused = get_unused_words(category, all_words)
        word = random.choice(unused)
        hint = get_hint(word)
        mark_word_as_used(category, word)
        return (word, hint) if hint else None

    return None
        