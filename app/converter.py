import nltk
from nltk.corpus import words

nltk.download('words', quiet=True)

# Define WORD_LIST using the NLTK word corpus
WORD_LIST = set(w.lower() for w in words.words() if w.isalpha())

# Use WORD_LIST to initialize word_list
word_list = WORD_LIST

# -------------------------------
# Major System Digit → Phonetic Sound Map
# -------------------------------
MAJOR_SYSTEM_MAP = {
    '0': ['s', 'z'],
    '1': ['t', 'd'],
    '2': ['n'],
    '3': ['m'],
    '4': ['r'],
    '5': ['l'],
    '6': ['j', 'sh', 'ch'],
    '7': ['k', 'g'],
    '8': ['f', 'v'],
    '9': ['p', 'b'],
}

# Predefined words (1–100) used only as a last resort
PREDEFINED = {
    '1': 'tie', '2': 'noah', '3': 'ma', '4': 'ear', '5': 'lea',
    '6': 'shea', '7': 'key', '8': 'ivy', '9': 'pea', '10': 'tease',
    '11': 'tit', '12': 'tin', '13': 'time', '14': 'tire', '15': 'tile',
    '16': 'dish', '17': 'tick', '18': 'tiff', '19': 'tip', '20': 'nose',
    '21': 'net', '22': 'nun', '23': 'name', '24': 'near', '25': 'nail',
    '26': 'nosh', '27': 'neck', '28': 'navy', '29': 'nap', '30': 'moss',
    '31': 'mat', '32': 'man', '33': 'mama', '34': 'mare', '35': 'mail',
    '36': 'mash', '37': 'mac', '38': 'mauve', '39': 'map', '40': 'rose',
    '41': 'rat', '42': 'ran', '43': 'ram', '44': 'rare', '45': 'rail',
    '46': 'rash', '47': 'rack', '48': 'rave', '49': 'rap', '50': 'lose',
    '51': 'lat', '52': 'lan', '53': 'lamb', '54': 'lair', '55': 'lull',
    '56': 'lash', '57': 'lack', '58': 'lava', '59': 'lap', '60': 'chess',
    '61': 'chat', '62': 'chain', '63': 'chum', '64': 'chair', '65': 'chill',
    '66': 'choo-choo', '67': 'chick', '68': 'chaff', '69': 'chip', '70': 'case',
    '71': 'cat', '72': 'can', '73': 'cam', '74': 'care', '75': 'call',
    '76': 'cash', '77': 'cake', '78': 'cave', '79': 'cap', '80': 'fuss',
    '81': 'fat', '82': 'fan', '83': 'fam', '84': 'fare', '85': 'fall',
    '86': 'fish', '87': 'fake', '88': 'fife', '89': 'fap', '90': 'pass',
    '91': 'pat', '92': 'pan', '93': 'pam', '94': 'pare', '95': 'pal',
    '96': 'pash', '97': 'pack', '98': 'pave', '99': 'pap', '100': 'tease'
}

# -------------------------------
# Helper: Convert word to digits using Major System
# -------------------------------
def word_to_digits(word):
    import re
    phoneme_map = {
        's': '0', 'z': '0',
        't': '1', 'd': '1',
        'n': '2',
        'm': '3',
        'r': '4',
        'l': '5',
        'j': '6', 'sh': '6', 'ch': '6',
        'k': '7', 'g': '7',
        'f': '8', 'v': '8',
        'p': '9', 'b': '9'
    }
    cleaned = re.sub(r'[^a-z]', '', word.lower())
    digits = ""
    i = 0
    while i < len(cleaned):
        if cleaned[i:i+2] in phoneme_map:
            digits += phoneme_map[cleaned[i:i+2]]
            i += 2
        elif cleaned[i] in phoneme_map:
            digits += phoneme_map[cleaned[i]]
            i += 1
        else:
            i += 1
    print(f"Word: {word}, Digits: {digits}")  # Debugging
    return digits

def matches_number(word, number):
    return word_to_digits(word) == number

# -------------------------------
# Helper: Phonetic Chunk-Based Matching
# -------------------------------
def find_words_for_number(number):
    results = []

    def backtrack(idx, path):
        if idx == len(number):
            results.append(" ".join(path))
            return
        for end in range(len(number), idx, -1):
            chunk = number[idx:end]
            for w in word_list:
                if matches_number(w, chunk):
                    backtrack(end, path + [w])
                    break
            else:
                continue
            break

    backtrack(0, [])
    return results

# -------------------------------
# Fallback: Predefined Word Matching (1–100)
# -------------------------------
def fallback_chunks(num):
    i = 0
    words = []
    while i < len(num):
        for j in range(min(3, len(num) - i), 0, -1):
            part = num[i:i + j]  # Fixed the slicing syntax
            if part in PREDEFINED:
                words.append(PREDEFINED[part])
                i += j
                break
        else:
            # If no match is found, return "No word or phrase found"
            return "No word or phrase found for this number."
    return " ".join(words)

# -------------------------------
# Main Function: Convert Number to Word(s)
# -------------------------------
def convert_number(number_str):
    # Check for invalid input
    if not number_str.replace('.', '').isdigit():
        return {
            'original': number_str,
            'type': 'invalid',
            'result': "No word or phrase found for this number."
        }

    # Check if the entire number (including decimal) exists in predefined mappings
    if number_str in PREDEFINED:
        return {
            'original': number_str,
            'type': 'predefined',
            'result': PREDEFINED[number_str]
        }

    # Handle decimal numbers as a single entity
    if '.' in number_str:
        left, right = number_str.split('.')
        combined_number = f"{left}.{right}"
        if combined_number in PREDEFINED:
            return {
                'original': number_str,
                'type': 'predefined',
                'result': PREDEFINED[combined_number]
            }
        else:
            # Fallback to combining left and right parts
            left_result = convert_number(left)['result']
            right_result = convert_number(right)['result']
            combined_result = f"{left_result} point {right_result}"
            return {
                'original': number_str,
                'type': 'decimal',
                'result': combined_result
            }

    # Helper function for recursive chunking
    def chunk_number(idx):
        if idx == len(number_str):
            return [[]]  # Base case: return an empty list of chunks

        results = []
        for j in range(1, min(3, len(number_str) - idx) + 1):  # Try chunks of size 1, 2, 3
            chunk = number_str[idx:idx + j]
            if chunk in PREDEFINED:
                for rest in chunk_number(idx + j):
                    results.append([PREDEFINED[chunk]] + rest)
        return results

    # Generate all possible chunking combinations
    all_combinations = chunk_number(0)
    if not all_combinations:
        return {
            'original': number_str,
            'type': 'none',
            'result': "No word or phrase found for this number."
        }

    # Sort the combinations alphabetically for consistent ordering
    all_combinations = sorted(all_combinations, key=lambda x: " ".join(x))

    # Format the results as a numbered list
    formatted_results = [f"{i + 1}) {' '.join(combination)}" for i, combination in enumerate(all_combinations)]
    return {
        'original': number_str,
        'type': 'predefined',
        'result': "\n".join(formatted_results)  # Ensure proper newline separation
    }
