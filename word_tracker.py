import json
import os

TRACKER_FILE = "used_words.json"

def load_used_words() -> dict:
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_used_words(used_words: dict) -> None:
    with open(TRACKER_FILE, "w") as f:
        json.dump(used_words, f, indent=2)

def mark_word_as_used(category: str, word: str) -> None:
    used_words = load_used_words()
    if category not in used_words:
        used_words[category] = []
    if word not in used_words[category]:
        used_words[category].append(word)
    save_used_words(used_words)

def get_unused_words(category: str, all_words: list) -> list:
    used_words = load_used_words()
    used = used_words.get(category, [])
    unused = [w for w in all_words if w not in used]

    if not unused:
        print(f"All words in '{category}' have been used! Starting fresh — consider adding new words to the list!")
        # Reset this category
        used_words[category] = []
        save_used_words(used_words)
        return all_words

    return unused