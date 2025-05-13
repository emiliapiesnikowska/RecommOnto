import sqlite3
import pandas as pd
import re
from rdflib import Graph

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

cursor.execute('UPDATE labels SET label = NULL WHERE label = \'\"fantasy live 1999\"\'')
conn.commit()
reviews_df = pd.read_sql('SELECT * FROM reviews', conn)
artists_df = pd.read_sql('SELECT * FROM artists', conn)
genres_df = pd.read_sql('SELECT * FROM genres', conn)
labels_df = pd.read_sql('SELECT * FROM labels', conn)
years_df = pd.read_sql('SELECT * FROM years', conn)
content_df = pd.read_sql('SELECT * FROM content', conn)

conn.close()

merged_df = reviews_df.merge(artists_df, on='reviewid')
merged_df = merged_df.merge(genres_df, on='reviewid')
merged_df = merged_df.merge(labels_df, on='reviewid')
merged_df = merged_df.merge(years_df, on='reviewid')
merged_df = merged_df.merge(content_df, on='reviewid')

def sanitize_identifier(name):
    return re.sub(r'\W|^(?=\d)', '_', name.strip().replace(' ', '_').replace('"',"").replace("'",''))

def generate_artist_triple(artist):
    if pd.isna(artist): return ""
    artist_uri = f":{sanitize_identifier(artist)}"
    return f"{artist_uri} a :Artist ;\n    rdfs:label \"{artist}\" ."

def generate_genre_triple(genre):
    if pd.isna(genre): return ""
    genre_uri = f":{sanitize_identifier(genre)}"
    return f"{genre_uri} a :Genre ;\n    rdfs:label \"{genre}\" ."

def generate_review_triple(row):
    review_uri = f":Rating_{row.get('reviewid', 'UnknownID')}"
    album_uri = f":Album_{row.get('reviewid', 'UnknownID')}"
    score = row.get('score', '0.0')
    return f"""{review_uri} a schema:Rating ;
    :aboutAlbum {album_uri} ;
    :Value \"{score}\"^^xsd:float ."""

def generate_user_triple(username):
    if pd.isna(username): return ""
    cleaned = username.replace('"', '')
    user_uri = f":{sanitize_identifier(cleaned)}"
    return f"""{user_uri} a foaf:Person ;
    rdfs:label \"{username}\" ."""

def generate_user_review_relation(row):
    username = row.get('author')
    review_uri = f":Rating_{row.get('reviewid', 'UnknownID')}"
    if pd.isna(username): return ""
    user_uri = f":{sanitize_identifier(username)}"
    return f"{user_uri} schema:rating {review_uri} ."

def generate_album_triples(row):
    album_uri = f":Album_{row.get('reviewid', 'UnknownID')}"
    artist = row.get('artist_x', 'UnknownArtist')
    genre = row.get('genre', 'UnknownGenre')
    label = row.get('label', 'UnknownLabel')
    year = row.get('year', 'UnknownYear')
    score = row.get('score', '0.0')
    title = row.get('title', 'Untitled Album')

    artist_uri = f":{sanitize_identifier(artist) if artist is not None else 'UnknownArtist'}"
    genre_uri = f":{sanitize_identifier(genre) if genre is not None else 'UnknownGenre'}"
    year = str(int(float(row.get('year', 0))))

    triples = [
        f"{album_uri} a schema:MusicAlbum ;",
        f'    rdfs:label \"{title}\" ;',
        f'    :hasArtist {artist_uri} ;',
        f'    :hasGenre {genre_uri} ;',
        f'    :releaseYear \"{year}\" .'
    ]
    return "\n".join(triples)

# Write RDF triples to Turtle file
with (open('pitchfork_album_reviews.ttl', 'w', encoding='utf-8') as f):
    f.write("""@prefix : <http://www.semanticweb.org/emili/ontologies/2025/3/recommendations/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix schema: <http://schema.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Genre a rdfs:Class .
:Artist a rdfs:Class .

""")
    i=0
    for index, row in merged_df.head(1000).iterrows():  # ograniczenie do 1000 opinii

        author = row.get('author') or ""
        title = row.get('title') or ""

        if '"' in author or "fantasy live 1999" in title.lower():
            continue

        genre_triple = generate_genre_triple(row.get('genre'))
        if genre_triple:
            f.write(genre_triple + '\n\n')

        artist_triple = generate_artist_triple(row.get('artist_x'))
        if artist_triple:
            f.write(artist_triple + '\n\n')

        review_triple = generate_review_triple(row)
        f.write(generate_album_triples(row) + '\n\n')
        f.write(review_triple + '\n\n')


        user_triple = generate_user_triple(row.get('author'))
        if user_triple:
            f.write(user_triple + '\n\n')

        user_review_relation = generate_user_review_relation(row)
        if user_review_relation:
            f.write(user_review_relation + '\n\n')

rdf_graph = Graph()
rdf_graph.parse('pitchfork_album_reviews.ttl', format='turtle')
rdf_graph.serialize(destination='pitchfork_album_reviews.rdf', format='xml')
