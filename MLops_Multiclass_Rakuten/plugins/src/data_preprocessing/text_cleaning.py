import re
import html
import string
import unicodedata
import pandas as pd
import nltk
from nltk.corpus import stopwords 
import mlflow
import mlflow.tensorflow


# ----------------------------- #
#        GLOBAL SETTINGS        #
# ----------------------------- #

# IS_DEBUG = True  # Enable debug messages
IS_DEBUG = False  # Disable debug messages
# ----------------------------- #
#   TEXT CLEANING FUNCTIONS     #s
# ----------------------------- #
nltk.download("stopwords")
def debug_print(message: str):
    """Print debug messages if IS_DEBUG is True."""
    if IS_DEBUG:
        print(f"[DEBUG] {message}")

def remove_duplicate_words(text: str) -> str:
    """Remove duplicate words while preserving their order."""
    debug_print("Removing duplicate words...")
    words = text.split()
    unique_words = list(dict.fromkeys(words))
    return " ".join(unique_words)

def create_clean_text(designation: str, description: str) -> str:
    """
    Combines 'designation' and 'description' into a single text column.
    - Handles missing descriptions.
    - Merges text fields and removes duplicate words.
    """
    debug_print("Creating unified text column...")
    if pd.isna(description) or description.strip() == "":
        text = designation
    else:
        text = f"{designation} {description}"
    return remove_duplicate_words(text)

def lower_case(text: str) -> str:
    """Convert text to lowercase and remove leading/trailing spaces."""
    debug_print("Converting text to lowercase...")
    return text.lower().strip()

def decode_html_entities(text: str) -> str:
    """Decodes HTML entities in the text (e.g., '&eacute;' → 'é')."""
    debug_print("Decoding HTML entities...")
    return html.unescape(text)

def remove_html_tags(text: str) -> str:
    """Removes HTML tags such as <p>, <b>, etc."""
    debug_print("Removing HTML tags...")
    return re.sub(r"<[^<]+?>", "", text)

def remove_accents(text: str) -> str:
    """Removes accented characters from text (e.g., 'é' → 'e')."""
    debug_print("Removing accents from text...")
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")

def normalize_text(text: str) -> str:
    """
    Replace special characters with their standard equivalents.
    Handles smart quotes, dashes, ellipses, and removes unwanted characters.
    """
    debug_print("Normalizing text (smart quotes, dashes, ellipses)...")
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "…": "...", "¿": ""
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

def keep_essential_characters(text: str) -> str:
    """Removes all non-alphabetic characters and keeps only letters."""
    debug_print("Keeping only essential characters (removing numbers, symbols)...")
    return re.sub(r"[^a-zA-Z]+", " ", text)

def remove_punctuation(text: str) -> str:
    """Remove punctuation using Python's `string.punctuation`."""
    debug_print("Removing punctuation...")
    return text.translate(str.maketrans('', '', string.punctuation))

# ----------------------------- #
#  STOPWORDS & SHORT WORDS      #
# ----------------------------- #

# Define stopwords list (French, English, German + custom)
debug_print("Loading stopwords...")
STOP_WORDS = set(
    stopwords.words('french') + stopwords.words('english') + stopwords.words('german') +
    ['plus', 'peut', 'tout', 'etre', 'sans', 'dont', 'aussi', 'comme', 'meme', 'bien',
     'leurs', 'elles', 'cette', 'celui', 'ainsi', 'encore', 'alors', 'toujours', 'toute',
     'deux', 'nouveau', 'peu', 'car', 'autre', 'jusqu', 'quand', 'ici', 'ceux', 'enfin',
     'jamais', 'autant', 'tant', 'avoir', 'moin', 'celle', 'tous', 'contre', 'pourtant',
     'quelque', 'toutes', 'surtout', 'cet', 'comment', 'rien', 'avant', 'doit', 'autre',
     'depuis', 'moins', 'tre', 'souvent', 'etait', 'pouvoir', 'apre', 'non', 'ver', 'quel',
     'pourquoi', 'certain', 'fait', 'faire', 'sou', 'donc', 'trop', 'quelques', 'parfois',
     'tres', 'donc', 'dire', 'eacute', 'egrave', 'rsquo', 'agrave', 'ecirc', 'nbsp', 'acirc',
     'apres', 'autres', 'ocirc', 'entre', 'sous', 'quelle']
)

def remove_stopwords_and_short_words(text: str) -> str:
    """Removes stopwords and filters out words shorter than 3 characters."""
    debug_print("Removing stopwords and short words...")
    words = text.split()
    return " ".join([word for word in words if word not in STOP_WORDS and len(word) > 2])

# ----------------------------- #
#  FULL CLEANING PIPELINE       #
# ----------------------------- #

def clean_text_pipeline(text: str) -> str:
    """Apply full text preprocessing pipeline."""
    debug_print(f"Cleaning text: {text[:50]}...")  # Show only first 50 characters 
    text = lower_case(text)
    text = decode_html_entities(text)
    text = remove_html_tags(text)
    text = remove_accents(text)
    text = normalize_text(text)
    text = keep_essential_characters(text)
    text = remove_punctuation(text)
    text = remove_stopwords_and_short_words(text)
    return text

def clean_dataframe(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Apply text cleaning pipeline to a DataFrame."""
    debug_print(f"Applying text cleaning pipeline to DataFrame on column: {text_column}")
    df[text_column] = df[text_column].astype(str).apply(clean_text_pipeline)
    return df
