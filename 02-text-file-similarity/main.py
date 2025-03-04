import os 
import spacy
import logging

# BOOKS_DIR is path to the directory of the downloaded books.
BOOKS_DIR = "./books"

# Load the spacy instance.
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 99999999999

# Disable spacy warnings and only show errors (if any).
logger = logging.getLogger("spacy")
logger.setLevel(logging.ERROR)

def read_and_process(path: str):
    """
    read_and_process opens the file in read-mode and process it
    using the spacy's nlp instance.
    """

    with open(path, 'r', encoding='utf-8') as file:
        doc = file.read()

    return nlp(doc)

# List books from the directory.
books = os.listdir(BOOKS_DIR)

# Write the book names
for index, book in enumerate(books):
    print(f'{index}\t- {book}')

# Ask user to choose a book as source file.
chosen_index = int(input(f"\nSelect a book [0-{len(books)-1}]: "))
chosen_book = books[chosen_index]

# Read an process the source book.
print(f"Processing '{chosen_book}'...")
main_doc = read_and_process(f'{BOOKS_DIR}/{chosen_book}')

# Remove the chosen book from the list.
books.pop(chosen_index)

# Read all books and compare them with the source book.
for book in books:
    print(f"Processing '{book}'...")
    doc = read_and_process(f'{BOOKS_DIR}/{book}')


    similarity = main_doc.similarity(doc)
    similarity_percentage = int(similarity * 100)

    print(f"{similarity_percentage}% of similarity between {chosen_book} and {book}")
