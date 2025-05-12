import csv

movie_mapping_file = "mapping_files/Out_Mapping_Film.txt"
actor_mapping_file = "mapping_files/Out_Mapping_Attori.txt"
director_mapping_file = "mapping_files/Out_Mapping_Registi.txt"
csv_file_path = "LDOS-CoMoDa.csv"
ttl_output_path = "output_LDOS-CoMoDa.ttl"

gender_map = {'1': 'Male', '2': 'Female'}
time_map = {'1': 'Morning', '2': 'Afternoon', '3': 'Evening', '4': 'Night'}
daytype_map = {'1': 'WorkingDay', '2': 'Weekend', '3': 'Holiday'}
season_map = {'1': 'Spring', '2': 'Summer', '3': 'Autumn', '4': 'Winter'}
location_map = {'1': 'Home', '2': 'PublicPlace', '3': 'FriendsHouse'}
weather_map = {'1': 'Sunny', '2': 'Rainy', '3': 'Stormy', '4': 'Snowy', '5': 'Cloudy'}
social_map = {
    '1': 'Alone', '2': 'Partner', '3': 'Friends', '4': 'Colleagues',
    '5': 'Parents', '6': 'Public', '7': 'Family'
}
emotion_map = {
    '1': 'Sad', '2': 'Happy', '3': 'Scared', '4': 'Surprised',
    '5': 'Angry', '6': 'Disgusted', '7': 'Neutral'
}
mood_map = {'1': 'Positive', '2': 'Neutral', '3': 'Negative'}
physical_map = {'1': 'Healthy', '2': 'Ill'}
genre_map = {
    '1': 'Action', '2': 'Adventure', '3': 'Animation', '4': 'Biography', '5': 'Comedy', '6': 'Crime',
    '7': 'Documentary', '8': 'Drama', '9': 'Family', '10': 'Fantasy', '11': 'History', '12': 'Horror',
    '13': 'Music', '14': 'Musical', '15': 'Mystery', '16': 'Romance', '17': 'Sci-Fi', '18': 'Sport',
    '19': 'Thriller', '20': 'War', '21': 'Western'
}
age_map = {'1':'Teen', '2':'Adult', '3':'Senior', '4':'UnknownAge'}

movie_map = {}
actor_map = {}
director_map = {}

with open(movie_mapping_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) < 3:
            parts = line.strip().split(" ", 2)
        if len(parts) == 3:
            mid, title, uri = parts
            movie_map[mid.strip()] = {"title": title.strip(), "uri": uri.strip()}

with open(actor_mapping_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) != 3:
            parts = line.strip().split(" ", 2)
        if len(parts) == 3:
            aid, name, uri = parts
            actor_map[aid.strip()] = {"name": name.strip(), "uri": uri.strip()}

with open(director_mapping_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) != 3:
            parts = line.strip().split(" ", 2)
        if len(parts) == 3:
            did, name, uri = parts
            director_map[did.strip()] = {"name": name.strip(), "uri": uri.strip()}

def map_value(value, mapping):
    return mapping.get(str(value).strip(), "Unknown")

def get_age_group(age_value):
    try:
        age = int(age_value)
        if age < 20:
            return "Teen"
        elif age < 65:
            return "Adult"
        else:
            return "Senior"
    except ValueError:
        return "UnknownAge"

def get_literal_or_unknown(value: str) -> str:
    val = value.strip()
    if not val or val.lower() == "unknown":
        return '"Unknown"^^xsd:string'
    return f':{val}'

def sanitize_identifier(name: str) -> str:
    return name.strip().replace(" ", "_").replace(".", "").replace(",", "").replace("-", "").replace("'", "").replace("/", "")


def generate_movie_triples(row):
    mid = row['itemID']
    movie_data = movie_map.get(mid, {})
    title = movie_data.get("title", f"UnknownMovie{mid}")
    movie_uri = f":Movie{mid}"

    did = row.get("director")
    director_data = director_map.get(did, {})
    director_uri = f":{sanitize_identifier(director_data.get('name', 'UnknownDirector'))}"

    actor_uris = []
    for actor_col in ['actor1', 'actor2', 'actor3']:
        aid = row.get(actor_col)
        if aid:
            actor_name = actor_map.get(aid.strip(), {}).get('name', 'UnknownActor')
            actor_uri = f":{sanitize_identifier(actor_name)}"
            actor_uris.append(actor_uri)

    genres = []
    for genre_col in ['genre1', 'genre2', 'genre3']:
        gids = row.get(genre_col, "").split(",")
        for gid in gids:
            gid = gid.strip()
            if gid:
                genre_uri = f":{map_value(gid, genre_map)}"
                genres.append(genre_uri)

    same_as = movie_data.get("uri")

    triples = [
        f"{movie_uri} a schema:Movie ;",
        f'    rdfs:label "{title}" ;',
        f'    :hasDirector {director_uri} ;',
        f'    :hasCountry "{row["movieCountry"]}"^^xsd:string ;',
        f'    :hasLanguage "{row["movieLanguage"]}"^^xsd:string ;',
        f'    :hasYearOfProduction "{row["movieYear"]}"^^xsd:gYear ;',
    ]

    if genres:
        triples.append(f'    :hasGenre {", ".join(genres)} ;')
    if actor_uris:
        triples.append(f'    :hasArtist {", ".join(actor_uris)} ;')

    triples.append(f'    :hasBudget "{row["budget"]}"^^xsd:float{" ;" if same_as else " ." }')

    if same_as:
        triples.append(f'    owl:sameAs <{same_as}> .')

    return "\n".join(triples)


def generate_contextual_triples(row):
    uid = row['userID']
    mid = row['itemID']
    context_uri = f":Context{uid}_{mid}"
    rating_uri = f":Rating{uid}_{mid}"

    triples = [
        f"{context_uri} a :Context ;",
        f"    :hasDemographicContext :DemographicContext{uid} ;",
        f"    :hasLocationContext :LocationContext{uid}_{mid} ;",
        f"    :hasWeatherContext :WeatherContext{uid}_{mid} ;",
        f"    :hasSocialContext :SocialContext{uid}_{mid} ;",
        f"    :hasUsersStateContext :UsersStateContext{uid}_{mid} ;",
        f"    :hasEmotionalContext :EmotionalContext{uid}_{mid} ;",
        f"    :hasTimeContext :TimeContext{uid}_{mid} .",

        f":DemographicContext{uid} a :DemographicContext ;",
        f"    :hasGender :{map_value(row['sex'], gender_map)} ;",
        f"    :hasAgeGroup :{get_age_group(row['age'])} .",

        f":LocationContext{uid}_{mid} a :LocationContext ;",
        f"    :hasLocation :Location{uid}_{mid} .",

        f":Location{uid}_{mid} a :Location ;",
        f"    :hasCity :City{row['city']} ;",
        f"    :hasCountry :Country{row['country']} ;",
        f"    :hasLocation :{map_value(row['location'], location_map)} .",

        f":WeatherContext{uid}_{mid} a :WeatherContext ;",
        f"    :hasWeather :{map_value(row['weather'], weather_map)} .",

        f":SocialContext{uid}_{mid} a :SocialContext ;",
        f"    :hasCompanion :{map_value(row['social'], social_map)} .",

        f":UsersStateContext{uid}_{mid} a :UsersStateContext ;",
        f"    :hasPhysicalState :{map_value(row['physical'], physical_map)} ;",
        f"    :hasUsersMood :{map_value(row['mood'], mood_map)} .",

        f":EmotionalContext{uid}_{mid} a :EmotionalContext ;",
        f"    :dominantEmotion :{map_value(row['dominantEmo'], emotion_map)} ;",
        f"    :endEmotion :{map_value(row['endEmo'], emotion_map)} .",

        f":TimeContext{uid}_{mid} a :TimeContext ;",
        f"    :hasTime :Time{uid}_{mid} .",

        f":Time{uid}_{mid} a :Time ;",
        f"    :hasSeason :{map_value(row['season'], season_map)} ;",
        f"    :hasTimeOfDay :{map_value(row['time'], time_map)} ;",
        f"    :hasDayOfWeek :{map_value(row['daytype'], daytype_map)} .",

        f":City{row['city']} a :City .",
        f":Country{row['country']} a :Country ."
    ]

    return "\n".join(triples)


def write_instances(mapping, class_name):
    return "\n".join([
        f":{v} a :{class_name} ; rdfs:label \"{v}\"^^xsd:string ." for v in mapping.values()
    ])

def generate_static_instances():
    lines = []

    added_actors = set()
    added_directors = set()

    for aid, actor in actor_map.items():
        name_id = actor["name"].replace(" ", "_").replace(".", "").replace(",", "").replace("'", "").replace("-","").replace("/","")
        if name_id not in added_actors:
            lines.append(f":{name_id} a :Actor ; rdfs:label \"{actor['name']}\" .")
            added_actors.add(name_id)

    for did, director in director_map.items():
        name_id = director["name"].replace(" ", "_").replace(".", "").replace(",", "").replace("'", "").replace("-","").replace("/","")
        if name_id not in added_directors and name_id not in added_actors:
            lines.append(f":{name_id} a :Director ; rdfs:label \"{director['name']}\" .")
            added_directors.add(name_id)

    return "\n".join(lines)

def generate_triples_from_row(row):
    uid = row['userID']
    mid = row['itemID']
    rating_val = float(row['rating'])
    context_uri = f":Context{uid}_{mid}"

    triples = [

        f":Rating{uid}_{mid} a schema:Rating ;",
        f"    schema:ratingValue \"{rating_val}\"^^xsd:float ;",
        f"    :hasContext {context_uri} ;",
        f"    schema:item :Movie{mid} . \n"

        f":User{uid} a foaf:Person ;",
        f"    :userID \"{uid}\"^^xsd:string ;",
        f"    :rated :Rating{uid}_{mid} . \n",
    ]

    context_triples = generate_contextual_triples(row)
    triples.append(context_triples)

    return "\n".join(triples)

def process_csv_to_ttl(csv_file_path, ttl_output_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(ttl_output_path, 'w', encoding='utf-8') as ttlfile:
            ttlfile.write("""@prefix : <http://www.semanticweb.org/emili/ontologies/2025/3/recommendations/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix schema: <http://schema.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Actor a owl:Class ;
    rdfs:label "Actor" .
:Director a owl:Class ;
    rdfs:label "Director" .


""")
            ttlfile.write(generate_static_instances())
            ttlfile.write("\n\n")
            ttlfile.write(write_instances(gender_map, "Gender") + "\n")
            ttlfile.write(write_instances(time_map, "TimeOfDay") + "\n")
            ttlfile.write(write_instances(daytype_map, "DayType") + "\n")
            ttlfile.write(write_instances(season_map, "Season") + "\n")
            ttlfile.write(write_instances(location_map, "LocationType") + "\n")
            ttlfile.write(write_instances(weather_map, "Weather") + "\n")
            ttlfile.write(write_instances(social_map, "Companion") + "\n")
            ttlfile.write(write_instances(emotion_map, "Emotion") + "\n")
            ttlfile.write(write_instances(mood_map, "UsersMood") + "\n")
            ttlfile.write(write_instances(physical_map, "PhysicalState") + "\n")
            ttlfile.write(write_instances(genre_map, "Genre") + "\n")
            ttlfile.write(write_instances(age_map, "AgeGroup") + "\n")
            ttlfile.write("\n\n\n\n")

            for row in reader:
                ttlfile.write(generate_movie_triples(row))
                ttlfile.write("\n\n")

                ttlfile.write("\n\n\n")
                ttlfile.write(generate_contextual_triples(row))
                ttlfile.write("\n\n")
                ttlfile.write(generate_triples_from_row(row))

                ttlfile.write("\n\n\n")




process_csv_to_ttl(csv_file_path, ttl_output_path)
print(f"TTL generated in '{ttl_output_path}'")
