import random

import requests


def get_hint(word):
    """
    https://www.datamuse.com/api/
    Check the documentation. This function takes the word
    and returns a hint related to that word.
    """
    url = f"https://api.datamuse.com/words?rel_trg={word}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        return random.choice(data)["word"] if data else None
    return None
