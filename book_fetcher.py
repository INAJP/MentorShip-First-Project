"""
book_fetcher.py

This script fetches book information from the public OpenLibrary API,
keeps only the books whose first publish year is after 2000,
and saves the output sorted (by publish year) in a CSV file.

How to run:
    python book_fetcher.py

Dependencies:
    Only the requests library (see requirements.txt).
"""

from __future__ import annotations

import csv
import sys
from typing import Dict, List, Optional

import requests

# ---------------------------------------------------------------------------
# Configurable Settings
# ---------------------------------------------------------------------------
SUBJECT: str = "cyberpunk"              # Book subject; you can change it to any other subject
BOOK_LIMIT: int = 50                  # Number of books to fetch from the API
MIN_PUBLISH_YEAR: int = 2000          # Only books published after this year will be kept
OUTPUT_CSV_PATH: str = "books_after_2000.csv"
REQUEST_TIMEOUT_SECONDS: int = 15


def fetch_books_by_subject(subject: str, limit: int) -> List[Dict]:
    """
    Fetches raw book information for a specific subject from the OpenLibrary Subjects API.

    API Documentation:
        https://openlibrary.org/dev/docs/api/subjects
    """
    url = f"https://openlibrary.org/subjects/{subject}.json"
    params = {"limit": limit}

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    data = response.json()
    return data.get("works", [])


def extract_book_info(raw_book: Dict) -> Dict:
    """Converts a raw API record into a clean dictionary ready for CSV output."""
    authors = raw_book.get("authors", [])
    author_names = ", ".join(author.get("name", "Unknown") for author in authors)

    return {
        "title": raw_book.get("title", "Untitled"),
        "author": author_names or "Unknown",
        "first_publish_year": raw_book.get("first_publish_year"),
        "edition_count": raw_book.get("edition_count", 0),
        "openlibrary_key": raw_book.get("key", ""),
    }


def filter_books_after_year(books: List[Dict], min_year: int) -> List[Dict]:
    """Returns only books with a known publish year that is strictly after min_year."""
    filtered: List[Dict] = []
    for book in books:
        year: Optional[int] = book.get("first_publish_year")
        if year is not None and year > min_year:
            filtered.append(book)
    return filtered


def save_books_to_csv(books: List[Dict], output_path: str) -> None:
    """Saves the filtered books sorted by publish year into a CSV file."""
    if not books:
        print("No books found to save; CSV file will not be created.")
        return

    sorted_books = sorted(books, key=lambda b: b["first_publish_year"])

    fieldnames = [
        "title",
        "author",
        "first_publish_year",
        "edition_count",
        "openlibrary_key",
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_books)


def main() -> None:
    print(f"Fetching {BOOK_LIMIT} books for the subject '{SUBJECT}' from OpenLibrary...")
    raw_books = fetch_books_by_subject(SUBJECT, BOOK_LIMIT)
    print(f"{len(raw_books)} books fetched.")

    books = [extract_book_info(raw_book) for raw_book in raw_books]

    filtered_books = filter_books_after_year(books, MIN_PUBLISH_YEAR)
    print(f"{len(filtered_books)} books published after {MIN_PUBLISH_YEAR} found.")

    save_books_to_csv(filtered_books, OUTPUT_CSV_PATH)
    print(f"Output saved to file '{OUTPUT_CSV_PATH}'.")


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print(f"Error connecting to OpenLibrary API: {error}", file=sys.stderr)
        sys.exit(1)