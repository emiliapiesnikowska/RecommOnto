import csv
import re

BOOKS_FILE = "books_data.csv"
RATINGS_FILE = "books_rating.csv"
OUTPUT_FILE = "amazon_books.ttl"
MAX_RECORDS = 1000

def sanitize_identifier(text):
    return re.sub(r'\W|^(?=\d)', '_', text.strip().lower()) if text else "unknown"

def create_ttl_prefixes():
    return """@prefix : <http://www.semanticweb.org/emili/ontologies/2025/3/recommendations/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix schema: <http://schema.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Book a rdfs:Class .
:Reviewer a rdfs:Class .
:Genre a rdfs:Class .

"""

def generate_genre_triple(genre):
    genre_clean = genre.replace('"', '')
    genre_id = sanitize_identifier(genre_clean)
    return f":{genre_id} a :Genre ;\n    rdfs:label \"{genre_clean}\" ."

def generate_book_triple(book_id, title, genre):
    title_clean = title.replace('"', '')
    genre_uri = f":{sanitize_identifier(genre)}"
    book_uri = f":Book_{sanitize_identifier(book_id)}"
    return f"""{book_uri} a schema:Book ;
    rdfs:label "{title_clean}" ;
    :hasGenre {genre_uri} ."""

def generate_rating_triple(user_id, book_id, rating):
    rating_uri = f":Rating_{sanitize_identifier(user_id)}_{sanitize_identifier(book_id)}"
    book_uri = f":Book_{sanitize_identifier(book_id)}"
    return f"""{rating_uri} a schema:Rating ;
    :aboutBook {book_uri} ;
    :Value "{rating}"^^xsd:float ."""

def generate_reviewer_triple(name):
    name_clean = name.replace('"', '')
    reviewer_uri = f":{sanitize_identifier(name_clean)}"
    return f"""{reviewer_uri} a foaf:Person ;
    rdfs:label "{name_clean}" ."""

def generate_reviewer_rating_link(name, user_id, book_id):
    reviewer_uri = f":{sanitize_identifier(name)}"
    rating_uri = f":Rating_{sanitize_identifier(user_id)}_{sanitize_identifier(book_id)}"
    return f"{reviewer_uri} schema:rating {rating_uri} ."


book_info = {}
with open(BOOKS_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row["Title"].replace('"', '').strip()
        category = row["categories"].replace('"', '').strip() if row["categories"] else None
        if title and category and category.lower() != "books":
            book_info[title.lower()] = {
                "category": category,
                "publisher": row.get("publisher", "")
            }

written_books = set()
written_genres = set()
written_reviewers = set()
count = 0

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(create_ttl_prefixes() + "\n")

    with open(RATINGS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if count >= MAX_RECORDS:
                break

            title = row["Title"].replace('"', '').strip()
            if not title or title.lower() not in book_info:
                continue

            book_data = book_info[title.lower()]
            genre = book_data["category"]
            user_id = row["User_id"]
            profile_name = row["profileName"].replace('"', '').strip() if row["profileName"] else user_id
            rating = row["review/score"]

            if genre not in written_genres:
                out.write(generate_genre_triple(genre) + "\n\n")
                written_genres.add(genre)

            if title not in written_books:
                out.write(generate_book_triple(title, title, genre) + "\n\n")
                written_books.add(title)

            out.write(generate_rating_triple(user_id, title, rating) + "\n\n")

            if profile_name not in written_reviewers:
                out.write(generate_reviewer_triple(profile_name) + "\n\n")
                written_reviewers.add(profile_name)

            out.write(generate_reviewer_rating_link(profile_name, user_id, title) + "\n\n")

            count += 1

