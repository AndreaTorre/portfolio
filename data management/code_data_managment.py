## LIBRERIE


import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
import csv
import pandas as pd
import re
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
import unicodedata
import mysql.connector
import pandas as pd






## DATA ACQUISITION:
# API SPOTIFY 


# Chiavi per accedere all'API di Spotify
CLIENT_ID = 'c20e63b0992a4a71869bf25a33d7c2a4'
CLIENT_SECRET = 'b4157ee671684e44abcecdfff3c76105'
REDIRECT_URI = 'https://localhost:5000/callback'  
SCOPE = 'user-read-private'  

# Configurazione del gestore di autenticazione OAuth
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    open_browser=True  
)

sp = Spotify(auth_manager=auth_manager)

playlist_ids = {
    2020: '2fmTTbBkXi8pewbUvG3CeZ',  # Top 50 del 2020
    2021: '5GhQiRkGuqzpWZSE7OU4Se',  # Top 50 del 2021
    2022: '56r5qRUv3jSxADdmBkhcz7',  # Top 50 del 2022
    2023: '6unJBM7ZGitZYFJKkO0e4P',  # Top 50 del 2023
}

# Per ottenere genere artista
def get_artist_genres(artist_id):
    artist = sp.artist(artist_id)
    return ', '.join(artist.get('genres', []))

# Per ottenere le canzoni per i vari anni
def get_top_hits(year):
    if year not in playlist_ids:
        print(f"Nessuna playlist trovata per l'anno {year}.")
        return []

    playlist_id = playlist_ids[year]
    playlist_tracks = sp.playlist_tracks(playlist_id, limit=50)
    songs = []

    for item in playlist_tracks['items']:
        track = item['track']
        artist_id = track['artists'][0]['id'] 
        genres = get_artist_genres(artist_id)

        song_info = {
            'id': track['id'],
            'name': track['name'],
            'artist': ', '.join(artist['name'] for artist in track['artists']),
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'genre': genres
        }
        songs.append(song_info)

    return songs



# Salvo canzoni in un csv
def save_songs_to_csv(year, songs):
    filename = f"Top_50_Global_Songs_{year}.csv"
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Artist', 'Album', 'Release Date', 'Genre'])
        for song in songs:
            writer.writerow([
                song['id'],
                song['name'],
                song['artist'],
                song['album'],
                song['release_date'],
                song['genre']
                
            ])

    print(f"File salvato: {filename}")

for year in range(2020, 2024):
    print(f"\nProcessing Top 50 Global Songs of {year}...")
    top_hits = get_top_hits(year)
    if top_hits:
        save_songs_to_csv(year, top_hits)


## CONCTENAZIONE DEI DATASET DI SPOTIFY

def concatenate_datasets(years):
    dataframes = []
    for year in years:
        filename = f"Top_50_Global_Songs_{year}.csv"
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            df['Year'] = year  
            dataframes.append(df)
        else:
            print(f"File non trovato: {filename}")
    
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_filename = "Top_50_Global_Songs_Combined.csv"
        combined_df.to_csv(combined_filename, index=False)
        print(f"Dataset combinato salvato: {combined_filename}")
    else:
        print("Nessun dataset da combinare.")

concatenate_datasets(range(2020, 2024))




## RIMOZIONE DEI FEAT PRESENTI NELLE COLONNE: "Name" e "Artist" per poter fare web scraping



# Rimuovo il testo tra parentesi dal titolo
def clean_title(title):
    return re.sub(r"\(.*?\)", "", title).strip()

# Prendo solo il cantante principale
def get_first_artist(artist):
    return artist.split(",")[0].strip()

#Applico funzioni per pulire il dataset 
input_csv = "Top_50_Global_Songs_Combined.csv"  
output_csv = "Top_50_Global_Songs_Cleaned.csv"  

df = pd.read_csv(input_csv, delimiter=",")  

df["Name"] = df["Name"].apply(clean_title)  
df["Artist"] = df["Artist"].apply(get_first_artist)  

df.to_csv(output_csv, index=False, sep=",")



##Salvare fino a un massimo di 2 feat in due colonne separate


# Funzione per estrarre featuring dal titolo della canzone
def extract_featuring_from_title(Name):
    patterns = [
        r"\(feat\. (.*?)\)",  # (feat. Artist)
        r"\[feat\. (.*?)\]",  # "[feat. Artist]
        r"feat\. (.*)",       # "feat. Artist
        r"ft\. (.*)",         # "ft. Artist
        r"-feat\. (.*)",      # "-feat. Artist
        r"\(feat (.*?)\)",   # "(feat Artist)
        r"\[feat (.*?)\]",   # "[feat Artist]
        r"feat (.*)",          # "feat Artist
        r"ft (.*)",            # "ft Artist
        r"-feat (.*)",         # -feat Artist
        r"\(with (.*?)\)",   # (with Artist)
        r"with (.*)",          # with Artist
    ]

    featuring_artists = []
    for pattern in patterns:
        match = re.search(pattern, Name, re.IGNORECASE)
        if match:
            artists = match.group(1)
            # Divido per virgola o '&' se ci sono più artisti
            featuring_artists.extend([artist.strip() for artist in re.split(r",| & ", artists)])
    # Rimuovo duplicati
    return list(set(featuring_artists))

# Pulisco titolo della canzone
def clean_title(Name):
    patterns = [
        r"\(feat\. .*?\)",  # Es. "(feat. Artist)"
        r"\[feat\. .*?\]",  # Es. "[feat. Artist]"
        r"feat\. .*",        # Es. "feat. Artist"
        r"ft\. .*",          # Es. "ft. Artist"
        r"-feat\. .*",       # Es. "-feat. Artist"
        r"\(feat .*?\)",    # Es. "(feat Artist)"
        r"\[feat .*?\]",    # Es. "[feat Artist]"
        r"feat .*",           # Es. "feat Artist"
        r"ft .*",             # Es. "ft Artist"
        r"-feat .*",          # Es. "-feat Artist"
        r"\(with .*?\)",    # Es. "(with Artist)"
        r"with .*",           # Es. "with Artist"
    ]

    cleaned_title = Name
    for pattern in patterns:
        cleaned_title = re.sub(pattern, "", cleaned_title, flags=re.IGNORECASE).strip()

    return cleaned_title

# Applico pulizia
input_csv = "Top_50_Global_Songs_Combined.csv" 
try:
    playlist_data = pd.read_csv(input_csv, delimiter=',', on_bad_lines='skip')
except Exception as e:
    print(f"Errore durante la lettura del CSV: {e}")
    exit()

required_columns = ['Name', 'Artist', 'ID']
missing_columns = [col for col in required_columns if col not in playlist_data.columns]
if missing_columns:
    
    exit()


results = []
for index, row in playlist_data.iterrows():
    titolo = row['Name']
    artist = row['Artist']
    ID = row['ID']  
    featuring_artists = extract_featuring_from_title(titolo)

    if featuring_artists:
        
        cleaned_title = clean_title(titolo)
        feat_1 = featuring_artists[0] if len(featuring_artists) > 0 else None
        feat_2 = featuring_artists[1] if len(featuring_artists) > 1 else None

        results.append({
            'Name': cleaned_title,
            'ID': ID,
            'Featuring_1': feat_1,
            'Featuring_2': feat_2 if feat_2 else "NULL"
        })

# Salvo in un csv solo le canzoni che hanno almeno un feat dal dataset di tutte le canzoni
output_csv = "featuring_results_with_ID_SPOTIFY.csv"
results_df = pd.DataFrame(results)
results_df.to_csv(output_csv, index=False, sep=';')




## WEB SCRAPING con AZLyrics

#Primo Scraping



# Funzione per rimuovere spazi e caratteri speciali
def clean_string(string):
    return re.sub(r"[^a-zA-Z0-9]", "", string.lower())

# Funzione per generare l'URL di AZLyrics
def generate_url(artist, song_title):
    artist = clean_string(artist)
    song_title = clean_string(song_title)
    return f"https://www.azlyrics.com/lyrics/{artist}/{song_title}.html"

# Funzione per effettuare lo scraping dei testi
def get_lyrics(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            main_div = soup.find("div", class_="col-xs-12 col-lg-8 text-center")
            if main_div:
                lyrics_div = main_div.find("div", class_=None)
                if lyrics_div:
                    return lyrics_div.get_text(strip=True)
        return None
    except Exception as e:
        print(f"Errore durante lo scraping di {url}: {e}")
        return None

# Funzione per generare varianti del nome artista
def generate_artist_variants(artist):
    parts = artist.split(" ")
    variants = [artist, "".join(parts), "-".join(parts)]
    if len(parts) > 1:
        variants.append("-".join(parts[:-1]))  # Senza ultima parola
        variants.append("-".join(parts[1:]))   # Senza prima parola
        variants.append(parts[0])              # Solo prima parola
        variants.append(parts[-1])             # Solo ultima parola
    return list(set(variants))

# Funzione per generare varianti del titolo della canzone
def generate_title_variants(song_title):
    song_title = re.sub(r"\(.?\)|\[.?\]|-.*", "", song_title)  # Rimuove testo tra parentesi e dopo trattini
    song_title = song_title.strip()
    variants = [
        song_title,
        song_title.replace(" ", ""),
        song_title.replace(" ", "-")
    ]
    return list(set(variants))

# Funzione principale per scraping
def scrape_lyrics(input_file, output_file, max_attempts=6):
    data = pd.read_csv(input_file, delimiter=';')
    results = []

    for index, row in data.iterrows():
        artist = row['Artist']
        song_title = row['Title']
        lyrics = None

        # Genera varianti di artisti e titoli
        artist_variants = generate_artist_variants(artist)
        title_variants = generate_title_variants(song_title)

        attempts = 0
        found = False
        for artist_variant in artist_variants:
            if found:
                break
            for title_variant in title_variants:
                if attempts >= max_attempts:
                    break

                url = generate_url(artist_variant, title_variant)
                print(f"Tentativo URL: {url}")
                lyrics = get_lyrics(url)

                if lyrics:
                    found = True
                    break

                attempts += 1
                time.sleep(random.uniform(10, 17))  # Pausa per rispettare il sito

        # Salva i risultati
        results.append({'artist': artist, 'song_title': song_title, 'lyrics': lyrics})
        print(f"Completato: {song_title} di {artist}, Testo trovato: {'Sì' if lyrics else 'No'}.")

   
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Risultati salvati in {output_file}.")

    # Controllo quali testi mancano
    missing_lyrics = results_df[results_df['lyrics'].isnull()]
    if not missing_lyrics.empty:
        print(f"{len(missing_lyrics)} canzoni non hanno ancora il testo.")
    else:
        print("Tutti i testi sono stati trovati!")

# dataset su cui fare lo scraping, basandomi sugli URL di AZLyrics 
input_file = "Top_50_Global_Songs_Cleaned.csv"
output_file = "prova1.csv"
scrape_lyrics(input_file, output_file)




## Scraping Finale


# Dizionario per correggere nomi di artisti

artist_name_map = {
    "Tyler": "Tyler, The Creator",
    "BTS": "bangtanboys",
    "Beyoncé":"beyonceknowles",
    "ROSALÍA": "rosala"

}

# Funzione per correggere nomi degli artisti
def correct_artist_name(artist):
    return artist_name_map.get(artist, artist)

# Funzione per normalizzare e rimuovere caratteri speciali e punteggiatura
def normalize_for_url(string):
    
    normalized = ''.join(
        c for c in unicodedata.normalize('NFD', string)
        if unicodedata.category(c) != 'Mn'
    )
    
    normalized = re.sub(r"[^\w\s-]", "", normalized) 
    return normalized.replace(" ", "").lower()

# Funzione per generare varianti del titolo
def generate_title_variants(song_title):
    # Rimuove contenuti (parentesi, feat., remix) ma mantiene i trattini
    song_title_clean = re.sub(r"\(.*?\)|\[.*?\]|feat.*|remix.*|vol\..*", "", song_title, flags=re.IGNORECASE).strip()
    song_title_clean = re.sub(r"[^\w\s-]", "", song_title_clean)  
    
    # Genera varianti del titolo
    variants = [
        song_title_clean.replace(" ", ""),  
        song_title_clean.replace(" ", "-"),  
        song_title_clean.replace("-", "")  
    ]
    return list(set(variants))

# Funzione per generare varianti degli artisti
def generate_artist_variants(artist):
    artist = correct_artist_name(artist)
    parts = artist.split(" ")
    variants = [artist.replace(" ", ""), "-".join(parts)]  
    if len(parts) > 1:
        variants.append(parts[0])  
        variants.append(parts[-1])  
    return list(set(variants))

# Funzione per generare l'URL
def generate_url(artist, song_title):
    artist = normalize_for_url(artist)
    song_title = normalize_for_url(song_title)
    return f"https://www.azlyrics.com/lyrics/{artist}/{song_title}.html"

# Funzione per effettuare lo scraping
def get_lyrics(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        print(f"Richiesta URL: {url}, Status Code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            main_div = soup.find("div", class_="col-xs-12 col-lg-8 text-center")
            if main_div:
                lyrics_div = main_div.find("div", class_=None)
                if lyrics_div:
                    for br in lyrics_div.find_all("br"):
                        br.replace_with("\n")
                    return lyrics_div.get_text(strip=True)
        return None
    except Exception as e:
        print(f"Errore durante lo scraping di {url}: {e}")
        return None

# Funzione principale per scraping
def scrape_missing_lyrics(input_file, output_file, max_attempts=10):
    data = pd.read_csv(input_file)
    missing_lyrics = data[data['lyrics'].isnull()].copy()

    for index, row in missing_lyrics.iterrows():
        artist = row['artist']
        song_title = row['song_title']
        lyrics = None

        artist_variants = generate_artist_variants(artist)
        title_variants = generate_title_variants(song_title)

        attempts = 0
        found = False
        for artist_variant in artist_variants:
            if found:
                break
            for title_variant in title_variants:
                if attempts >= max_attempts:
                    break

                url = generate_url(artist_variant, title_variant)
                print(f"Tentativo URL: {url}")
                lyrics = get_lyrics(url)
                if lyrics:
                    found = True
                    data.at[index, 'lyrics'] = lyrics
                    print(f"Testo trovato per {song_title} di {artist}")
                    break
                attempts += 1
                time.sleep(random.uniform(5, 10))

            if not found:
                print(f"Nessun testo trovato per {song_title} di {artist}")

    data.to_csv(output_file, index=False)

# Passo il file del primo scraping e cerco solo le canzoni che non hanno ottenuto un lyrics dal processo precedente
input_file = "prova1.csv"
output_file = "final_lyrics_spotify.csv"
scrape_missing_lyrics(input_file, output_file)




## AGGIUNTA DELLA COLONNA "ID" AL DATASET "final_lyrics_spotify"


dataset_1 = pd.read_csv("Top_50_Global_Songs_Combined.csv") 
dataset_2 = pd.read_csv("final_lyrics_spotify.csv") 

# Normalizza i valori per evitare incongruenze
dataset_1["Artist"] = dataset_1["Artist"].str.lower().str.strip()
dataset_1["Name"] = dataset_1["Name"].str.lower().str.strip()
dataset_2["Artist"] = dataset_2["artist"].str.lower().str.strip()
dataset_2["song_title"] = dataset_2["song_title"].str.lower().str.strip()

# Esegui il merge basato su "Artist" e "song_title" (corrisponde a "Name" in dataset_1)
merged_data = pd.merge(
    dataset_1,
    dataset_2,
    left_on=["Artist", "Name"],
    right_on=["Artist", "song_title"],
    how="inner"
)


output = merged_data[["ID", "Artist", "Name", "lyrics"]]

output.to_csv("lyrics_FINALE.csv", index=False)




### DATASET DI KAGGLE 2023 per aggiungere la colonna "ID" mancante
# Abbiamo utilizzato le API di SPOTIFY per aggiungere ID

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

file_path = "SPOTIFY_KAGGLE_2023.csv"

df = pd.read_csv(file_path, sep=';')

# Funzione per cercare l'id dati il titolo e il cantante
def get_track_id(artist, song):
    query = f"track_name:{song} artist_name:{artist}"  
    result = sp.search(q=query, type="track", limit=1)  
    tracks = result.get('tracks', {}).get('items', [])
    if tracks: 
        return tracks[0]['id']  
    return None  


df['spotify_id'] = df.apply(lambda row: get_track_id(row['artist_name'], row['track_name']), axis=1)

df.to_csv("SPOTIFY_KAGGLE_2023_ID.csv", index=False)
print("Dataset aggiornato con gli ID di Spotify salvato come 'SPOTIFY_KAGGLE_2023_ID.csv'.")


### INTEGRAZIONE TRA I 4 DATASET DI KAGGLE


file_2020 = "SPOTIFY_KAGGLE_2020.csv"
file_2021 = "SPOTIFY_KAGGLE_2021.csv"
file_2022 = "SPOTIFY_KAGGLE_2022.csv"
file_2023 = "SPOTIFY_KAGGLE_2023_ID.csv"  # dataset da cui ho ricavato l'Id attraverso API di SPoty

#Elimino il problema di Eterogeneità nei nomi (in questo caso sinonimia) dando alle colonne che contengono le stesse info lo stesso nome
column_mapping_2020 = {
    "track_name": "Track Name",
    "artist": "Artist Name",
    "album": "Album",
    "track_id": "Track ID",
    "danceability": "Danceability",
    "energy": "Energy",
    "key": "Key",
    "loudness": "Loudness (dB)",
    "mode": "Mode",
    "speechiness": "Speechiness",
    "acousticness": "Acousticness",
    "instrumentalness": "Instrumentalness",
    "liveness": "Liveness",
    "valence": "Valence",
    "tempo": "Tempo",
    "duration_ms": "Duration",
    "time_signature": "Time Signature",
    "popularity": "Popularity"
}

column_mapping_2021 = {
    "track_name": "Track Name",
    "artist_name": "Artist Name",
    "album": "Album",
    "track_id": "Track ID",
    "danceability": "Danceability",
    "energy": "Energy",
    "key": "Key",
    "loudness": "Loudness (dB)",
    "mode": "Mode",
    "speechiness": "Speechiness",
    "acousticness": "Acousticness",
    "instrumentalness": "Instrumentalness",
    "liveness": "Liveness",
    "valence": "Valence",
    "tempo": "Tempo",
    "duration_ms": "Duration",
    "time_signature": "Time Signature",
    "popularity": "Popularity"
}

column_mapping_2022 = {
    "Track Name": "Track Name",
    "Artist Name(s)": "Artist Name",
    "Album Name": "Album",
    "Spotify ID": "Track ID",
    "Danceability": "Danceability",
    "Energy": "Energy",
    "Key": "Key",
    "Loudness": "Loudness (dB)",
    "Mode": "Mode",
    "Speechiness": "Speechiness",
    "Acousticness": "Acousticness",
    "Instrumentalness": "Instrumentalness",
    "Liveness": "Liveness",
    "Valence": "Valence",
    "Tempo": "Tempo",
    "Duration (ms)": "Duration",
    "Time Signature": "Time Signature",
    "Popularity": "Popularity"
}

column_mapping_2023 = {
    "track_name": "Track Name",
    "artist_name": "Artist Name",
    "album": "Album",
    "spotify_id": "Track ID",
    "danceability": "Danceability",
    "energy": "Energy",
    "key": "Key",
    "loudness": "Loudness (dB)",
    "mode": "Mode",
    "speechiness": "Speechiness",
    "acousticness": "Acousticness",
    "instrumentalness": "Instrumentalness",
    "liveness": "Liveness",
    "valence": "Valence",
    "tempo": "Tempo",
    "duration_ms": "Duration",
    "time_signature": "Time Signature",
    "popularity": "Popularity"
}

# colonne che voglio tenere quando facciola concatenazione (quelle in comune/utili)
columns_to_keep = [
    "Track Name", "Artist Name", "Album", "Track ID", "Danceability", "Energy", "Key",
    "Loudness (dB)", "Mode", "Speechiness", "Acousticness", "Instrumentalness",
    "Liveness", "Valence", "Tempo", "Duration", "Time Signature", "Popularity"
]


df_2020 = pd.read_csv(file_2020, delimiter=";", encoding="utf-8", on_bad_lines='skip')
df_2021 = pd.read_csv(file_2021, delimiter=";", encoding="utf-8", on_bad_lines='skip')
df_2022 = pd.read_csv(file_2022, delimiter=";", encoding="latin1", on_bad_lines='skip')
df_2023 = pd.read_csv(file_2023, delimiter=",", encoding="utf-8", on_bad_lines='skip')


df_2020.rename(columns=column_mapping_2020, inplace=True)
df_2021.rename(columns=column_mapping_2021, inplace=True)
df_2022.rename(columns=column_mapping_2022, inplace=True)
df_2023.rename(columns=column_mapping_2023, inplace=True)

def filter_columns(df, common_columns):
    return df[[col for col in common_columns if col in df.columns]]


common_columns = set(columns_to_keep)
common_columns &= set(df_2020.columns) & set(df_2021.columns) & set(df_2022.columns) & set(df_2023.columns)

df_2020_filtered = filter_columns(df_2020, common_columns)
df_2021_filtered = filter_columns(df_2021, common_columns)
df_2022_filtered = filter_columns(df_2022, common_columns)
df_2023_filtered = filter_columns(df_2023, common_columns)


combined_df = pd.concat([df_2020_filtered, df_2021_filtered, df_2022_filtered, df_2023_filtered], ignore_index=True)

output_file = "KAGGLE_COMPLETO.csv"   
combined_df.to_csv(output_file, index=False)

print(f"Dataset combinato salvato come '{output_file}'")




##Il codice seguente trova le canzoni in comune tra spotify e kaggle


df_kaggle = pd.read_csv("KAGGLE_COMPLETO.csv")  # Kaggle dataset
df_spotify = pd.read_csv("Top_50_Global_Songs_Combined.csv")  # Spotify dataset

# Rinominare la colonna 'Track ID' in Kaggle per uniformità
df_kaggle.rename(columns={
    'Track ID': 'ID',  # Uniformare il nome della colonna ID
    'Artist Name': 'Artist',
    'Track Name': 'Name'
}, inplace=True)

# Merge solo su 'ID'
merged_by_id = pd.merge(df_kaggle, df_spotify, on="ID", how="inner")

# Identificare le canzoni non abbinate solo tramite 'ID'
remaining_kaggle = df_kaggle[~df_kaggle['ID'].isin(merged_by_id['ID'])]
remaining_spotify = df_spotify[~df_spotify['ID'].isin(merged_by_id['ID'])]
#Doppio controllo anche rispetto alla coppia nome artista
merged_by_name_artist = pd.merge(
    remaining_kaggle,
    remaining_spotify,
    on=["Name", "Artist"],
    how="inner"
)

# Mantieni solo l'ID di Spotify per il secondo match
merged_by_name_artist["ID"] = merged_by_name_artist["ID_y"]
merged_by_name_artist.drop(columns=["ID_x", "ID_y"], inplace=True)

# unisco i risultati di entrambi i merge
final_combined = pd.concat([merged_by_id, merged_by_name_artist], ignore_index=True)

# Rimuovere eventuali duplicati basati su 'ID'
final_result = final_combined.drop_duplicates(subset=["ID"])


final_result.to_csv("songs_in_common_with_id.csv", index=False)

print("Dataset finale salvato come 'songs_in_common_with_id.csv'.")


import pandas as pd

# Percorso del file input
file_path_with_id = 'songs_in_common_with_id.csv'

# Carica il file CSV
with_id_data = pd.read_csv(file_path_with_id)

# Identifica le righe vuote nella colonna "Artist_x" e "Name_x" a partire dalla riga 66
missing_artist_x_mask = with_id_data.index >= 65  # Filtra per indice maggiore o uguale a 65
missing_artist_x_mask &= with_id_data['Artist_x'].isna()  # Verifica i valori NaN in 'Artist_x'

missing_name_x_mask = with_id_data.index >= 65  # Filtra per indice maggiore o uguale a 65
missing_name_x_mask &= with_id_data['Name_x'].isna()  # Verifica i valori NaN in 'Name_x'

# Riempie le righe vuote di "Artist_x" con i valori corrispondenti da "Artist"
with_id_data.loc[missing_artist_x_mask, 'Artist_x'] = with_id_data.loc[missing_artist_x_mask, 'Artist']

# Riempie le righe vuote di "Name_x" con i valori corrispondenti da "Name"
with_id_data.loc[missing_name_x_mask, 'Name_x'] = with_id_data.loc[missing_name_x_mask, 'Name']

# Salva il file aggiornato
output_path = 'songs_in_common_with_id_updated.csv'
with_id_data.to_csv(output_path, index=False)

print(f"File aggiornato salvato in: {output_path}")




##Puliamo il dataset ottenuto eliminando le colonne che rappresentano lo stesso valore

common_songs = pd.read_csv("songs_in_common_with_id_updated.csv")

# Rimuovere le colonne inutili: 'Name_y', 'Artist_y', 'Artist', 'Name'
columns_to_drop = ["Name_y", "Artist_y", "Artist", "Name"]
common_songs.drop(columns=columns_to_drop, inplace=True)

# Rinominare le colonne con suffisso '_x' rimuovendo il suffisso
common_songs.columns = [col.replace('_x', '') if '_x' in col else col for col in common_songs.columns]

# Salvare il risultato
common_songs.to_csv("songs_in_common_cleaned.csv", index=False)


############## Il codice separa in due dataset le canzoni non in comune per spotify e kaggle

### Pulizia artista dai feat


file_path_cleaned = 'songs_in_common_cleaned.csv' 

cleaned_data = pd.read_csv(file_path_cleaned)

# Funzione per mantenere solo il primo nome e rimuovere le virgolette
def clean_artist_name(artist):
    if pd.isna(artist):
        return artist  # Mantiene NaN
    artist = artist.replace('"', '') 
    return artist.split(',')[0].strip()  # Mantiene solo il primo nome

# Applica la funzione alla colonna 'Artist'
cleaned_data['Artist'] = cleaned_data['Artist'].apply(clean_artist_name)


output_path = 'songs_in_common_cleaned_updated.csv'  
cleaned_data.to_csv(output_path, index=False)

print(f"File aggiornato salvato in: {output_path}")


### Pulizia titoli 

file_path_cleaned = 'songs_in_common_cleaned_updated.csv'  

cleaned_data = pd.read_csv(file_path_cleaned)

# Definizione dei pattern da rimuovere
patterns = [
    r"\(feat\. (.*?)\)",  # (feat. Artist)
    r"\[feat\. (.*?)\]",  # "[feat. Artist]
    r"feat\. (.*)",       # "feat. Artist
    r"ft\. (.*)",         # "ft. Artist
    r"-feat\. (.*)",      # "-feat. Artist
    r"\(feat (.*?)\)",    # "(feat Artist)
    r"\[feat (.*?)\]",    # "[feat Artist]
    r"feat (.*)",         # "feat Artist
    r"ft (.*)",           # "ft Artist
    r"-feat (.*)",        # -feat Artist
    r"\(with (.*?)\)",    # (with Artist)
    r"with (.*)",         # with Artist
]

# Funzione per rimuovere i featuring dal titolo
def clean_title(title):
    if pd.isna(title):
        return title  # Mantiene NaN
    for pattern in patterns:
        title = re.sub(pattern, '', title, flags=re.IGNORECASE)  # Rimuove il pattern
    return title.strip()  # Rimuove spazi extra

# Applica la funzione alla colonna 'Name'
cleaned_data['Name'] = cleaned_data['Name'].apply(clean_title)

output_path = 'songs_in_common_cleaned_final.csv' 
cleaned_data.to_csv(output_path, index=False)





######### Il codice separa in due dataset le canzoni non in comune per spotify e kaggle

df1 = pd.read_csv("Top_50_Global_Songs_Combined.csv")  
common_songs = pd.read_csv("songs_in_common_cleaned.csv")

# Rimuovi spazi indesiderati dai nomi delle colonne
df1.columns = df1.columns.str.strip()
common_songs.columns = common_songs.columns.str.strip()


# Normalizza i valori delle colonne 'Name' e 'Artist' per evitare problemi di confronto
df1["Name"] = df1["Name"].str.lower().str.strip()
df1["Artist"] = df1["Artist"].str.lower().str.strip()
common_songs["Name"] = common_songs["Name"].str.lower().str.strip()
common_songs["Artist"] = common_songs["Artist"].str.lower().str.strip()


# Ottieni le canzoni non comuni in df1
not_in_common_df1 = pd.merge(
    df1, 
    common_songs, 
    on=["ID"], 
    how="outer", 
    indicator=True
).query('_merge == "left_only"').drop(columns=['_merge'])


not_in_common_df1.to_csv("spotify_not_in_common.csv", index=False)




#### PULISCO SPOTIFY_NOT_IN_COMMON

# Carica il dataset
spotify_not_in_common = pd.read_csv("spotify_not_in_common.csv")

# Rimuovo le colonne completamente vuote
spotify_not_in_common_cleaned = spotify_not_in_common.dropna(axis=1, how='all')

# Salva il risultato pulito in un nuovo file
spotify_not_in_common_cleaned.to_csv("spotify_not_in_common_cleaned.csv", index=False)






### Crea due dataset separati per ottenere i feat con le canzoni non in comune e uno con le canzoni in comune


featuring_dataset = pd.read_csv("featuring_results_with_ID_SPOTIFY.csv", delimiter=';')  # Dataset con tutti i feat di spotify 
spotify_not_in_common = pd.read_csv("spotify_not_in_common_cleaned.csv", delimiter=',')  # Dataset con le canzoni che non sono presenti in Kaggle

# Mantieni solo le colonne 'ID' dal dataset spotify_not_in_common per confrontare
spotify_not_in_common_ids = spotify_not_in_common["ID"]

# Dividi il dataset dei feat in due: canzoni presenti solo su Spotify e le restanti
feat_in_not_in_common = featuring_dataset[featuring_dataset["ID"].isin(spotify_not_in_common_ids)]
feat_not_in_not_in_common = featuring_dataset[~featuring_dataset["ID"].isin(spotify_not_in_common_ids)]

# Salva i due dataset risultanti
feat_in_not_in_common.to_csv("feat_in_spotify_not_in_common.csv", index=False)
feat_not_in_not_in_common.to_csv("feat_in_spotify_and_kaggle.csv", index=False)



lyrics_dataset = pd.read_csv("lyrics_FINALE.csv", delimiter=',')  # Dataset con tutti i feat
# Dividi il dataset dei feat in due: canzoni presenti solo su Spotify e le restanti
lyrics_in_not_in_common = lyrics_dataset[lyrics_dataset["ID"].isin(spotify_not_in_common_ids)]
lyrics_not_in_not_in_common = lyrics_dataset[~lyrics_dataset["ID"].isin(spotify_not_in_common_ids)]

# Salva i due dataset risultanti
lyrics_in_not_in_common.to_csv("lyrics_in_spotify_not_in_common.csv", index=False)
lyrics_not_in_not_in_common.to_csv("lyrics_in_spotify_and_kaggle.csv", index=False)



###DATA CLEANING

#Funzione per pulire i featuring
def clean_featuring_column(column):

    return column.str.replace(r"[()]", "", regex=True).str.strip()

new_spotify_feat_csv = "feat_in_spotify_not_in_common.csv"
spotify_kaggle_feat_csv = "feat_in_spotify_and_kaggle.csv"

# Caricamento dei dati
new_spotify_feat = pd.read_csv(new_spotify_feat_csv)
spotify_kaggle_feat = pd.read_csv(spotify_kaggle_feat_csv)

# Pulizia delle colonne Featuring_1 e Featuring_2
for dataset, name in zip([new_spotify_feat, spotify_kaggle_feat], ['new_spotify_feat', 'spotify_kaggle_feat']):
    dataset['Featuring_1'] = clean_featuring_column(dataset['Featuring_1'])
    dataset['Featuring_2'] = clean_featuring_column(dataset['Featuring_2'])

    # Salva i risultati puliti
    output_csv = f"{name}_cleaned.csv"
    dataset.to_csv(output_csv, index=False, sep=';')



###Funzione per pulire i dataset con i feat, eliminando eventuali doppioni nelle colonne, check anche su remix


file_path = 'spotify_kaggle_feat_cleaned.csv'  
data = pd.read_csv(file_path, delimiter=';')

# Funzione per rimuovere la parola "Remix" dalle stringhe
def remove_remix(text):
    if isinstance(text, str):
        return text.replace('Remix', '').strip()
    return text

# Applica la funzione per rimuovere "Remix" su entrambe le colonne
data['Featuring_1'] = data['Featuring_1'].apply(remove_remix)
data['Featuring_2'] = data['Featuring_2'].apply(remove_remix)

# Sostituisci i valori corrispondenti in 'Featuring_2' con NULL (NaN) se coincidono con 'Featuring_1'
data['Featuring_2'] = data.apply(
    lambda row: None if row['Featuring_1'] == row['Featuring_2'] else row['Featuring_2'],
    axis=1
)


output_path = 'spotify_kaggle_feat_cleaned_updated.csv'  
data.to_csv(output_path, sep=';', index=False)



file_path = 'new_spotify_feat_cleaned.csv' 
data = pd.read_csv(file_path, delimiter=';')

# Funzione per rimuovere la parola "Remix" dalle stringhe
def remove_remix(text):
    if isinstance(text, str):
        return text.replace('Remix', '').strip()
    return text

# Applica la funzione per rimuovere "Remix" su entrambe le colonne
data['Featuring_1'] = data['Featuring_1'].apply(remove_remix)
data['Featuring_2'] = data['Featuring_2'].apply(remove_remix)

# Sostituisci i valori corrispondenti in 'Featuring_2' con NULL (NaN) se coincidono con 'Featuring_1'
data['Featuring_2'] = data.apply(
    lambda row: None if row['Featuring_1'] == row['Featuring_2'] else row['Featuring_2'],
    axis=1
)

# Salva il DataFrame modificato in un nuovo file
output_path = 'new_spotify_feat_cleaned_updated.csv'  
data.to_csv(output_path, sep=';', index=False)




####DATA QUALITY

## DIMENSIONI QUALITATIVE

##Completezza: Calcola la percentuale di valori mancanti e li elenca per colonna.
#Deduplicazione: Cerca duplicati basati su ID, nome e artista.
#Rapporto: Salva un file CSV con un riassunto delle metriche di qualità dei dati.



datasets = {
    "new_spotify_feat_cleaned_updated.csv": {"columns": ["Name", "ID", "Featuring_1", "Featuring_2"], "delimiter": ";"},
    "spotify_kaggle_feat_cleaned_updated.csv": {"columns": ["Name", "ID", "Featuring_1", "Featuring_2"], "delimiter": ";"},
    "lyrics_FINALE.csv": {"columns": ["ID", "Artist", "Name", "lyrics"], "delimiter": ","},
    "spotify_not_in_common_cleaned.csv": {"columns": ["ID", "Name_x", "Artist_x", "Album_x", "Release Date_x", "Genre_x", "Year_x"], "delimiter": ","},
    "lyrics_in_spotify_not_in_common.csv": {"columns": ["ID", "Artist", "Name", "lyrics"], "delimiter": ","},
    "songs_in_common_cleaned_final.csv": {"columns": ["ID", "Name", "Artist", "Album", "Release Date", "Genre", "Year"], "delimiter": ","}
}

def check_data_quality(file_path, expected_columns, delimiter=","):
    try:
        data = pd.read_csv(file_path, delimiter=delimiter, on_bad_lines='skip')
    except Exception as e:
        return f"Errore durante la lettura di {file_path}: {e}"

    report = {}

    # Completezza
    missing_values = data.isnull().sum().sum()
    total_values = data.shape[0] * data.shape[1]
    missing_percentage = (missing_values / total_values) * 100 if total_values > 0 else 0
    report["Completezza"] = f"{missing_percentage:.2f}% valori mancanti"
    
    # Deduplicazione
    duplicates = data.duplicated().sum()
    report["Duplicati"] = f"{duplicates} duplicati trovati"

    return report

# Itera sui dataset
for dataset, details in datasets.items():
    # Usa il percorso completo o aggiungi "datasets/"
    file_path = dataset if ":" in dataset else f"datasets/{dataset}"
    columns = details["columns"]
    delimiter = details["delimiter"]
    
    print(f"\nAnalizzando {file_path}...")
    report = check_data_quality(file_path, columns, delimiter)
    print(report)




all_reports = []
for dataset, details in datasets.items():
    file_path = dataset if ":" in dataset else f"datasets/{dataset}"
    columns = details["columns"]
    delimiter = details["delimiter"]
    
    print(f"Analizzando {file_path}...")
    report = check_data_quality(file_path, columns, delimiter)
    print(report)
    
    # Aggiungi il report alla lista
    report["Dataset"] = file_path  
    all_reports.append(report)

# Salva tutti i report in un file CSV
output_csv = "data_quality_reports.csv"
with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Dataset", "Completezza", "Duplicati"])
    writer.writeheader()
    for report in all_reports:
        writer.writerow(report)







### MODELLO RELAZIONE MYSQL


## SPOTIFY E KAGGLE IN COMMON
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="DataMan.24",  
    database="SpotifyGeniusDB" 
)

cursor = db.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS songs_in_common (
    ID VARCHAR(255) PRIMARY KEY,            -- ID univoco della canzone
    Name VARCHAR(255) NOT NULL,             -- Nome della canzone
    Artist VARCHAR(255) NOT NULL,           -- Nome dell'artista
    Album VARCHAR(255),                     -- Nome dell'album
    Release_Date DATE,                      -- Data di rilascio
    Genre VARCHAR(255),                     -- Genere musicale
    Year INT,                               -- Anno
    Acousticness DECIMAL(10, 7),            -- Acousticness
    Instrumentalness DECIMAL(10, 7),        -- Instrumentalness
    Duration INT,                           -- Durata in millisecondi
    Danceability DECIMAL(10, 7),            -- Danceability
    Liveness DECIMAL(10, 7),                -- Liveness
    Speechiness DECIMAL(10, 7),             -- Speechiness
    `Key` INT,                              -- Chiave musicale
    Valence DECIMAL(10, 7),                 -- Valence
    Tempo DECIMAL(10, 7),                   -- Tempo
    Energy DECIMAL(10, 7),                  -- Energia
    Loudness_dB DECIMAL(10, 7)              -- Volume in decibel
);
"""
cursor.execute(create_table_query)
db.commit()
print("Tabella 'songs_in_common' creata con successo!")

csv_file = "songs_in_common_cleaned_final.csv" 
data = pd.read_csv(csv_file)

numerical_columns = [
    'Acousticness', 'Instrumentalness', 'Danceability', 'Liveness',
    'Speechiness', 'Valence', 'Tempo', 'Energy', 'Loudness (dB)'
]
for col in numerical_columns:
    if col in data.columns:
        # Converti valori scientifici e sostituisci separatori decimali
        data[col] = (
            data[col]
            .astype(str)
            .str.replace(',', '.', regex=False)  
            .astype(float)  # Converte a float perchè intrumentalness espressa in notazione scientifica
        )

data = data.where(pd.notnull(data), None)

insert_query = """
INSERT INTO songs_in_common (
    ID, Name, Artist, Album, Release_Date, Genre, Year, Acousticness,
    Instrumentalness, Duration, Danceability, Liveness, Speechiness,
    `Key`, Valence, Tempo, Energy, Loudness_dB
) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
for _, row in data.iterrows():
    cursor.execute(insert_query, (
        row['ID'], row['Name'], row['Artist'], row['Album'], row['Release Date'],
        row['Genre'], row['Year'], row['Acousticness'], row['Instrumentalness'],
        row['Duration'], row['Danceability'], row['Liveness'], row['Speechiness'],
        row['Key'], row['Valence'], row['Tempo'], row['Energy'], row['Loudness (dB)']
    ))
db.commit()
print(f"Dati importati con successo nella tabella 'songs_in_common'!")

cursor.close()
db.close()





## SPOTIFY NOT IN COMMON


import unicodedata
import mysql.connector
import pandas as pd
import csv 

db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="DataMan.24",  
    database="SpotifyGeniusDB"
)

cursor = db.cursor()


# Leggi il dataset CSV
csv_file = "C:\\Users\\yasmi\\Desktop\\Data_Man_progetto\\Data_Man_progett\\spotify_not_in_common_cleaned.csv"  # Sostituisci con il nome corretto del file CSV
spotify_data = pd.read_csv(csv_file)

# Inserisci i dati nella nuova tabella
for _, row in spotify_data.iterrows():
    try:
        query = """
        INSERT INTO spotify_new (ID, Name_x, Artist_x, Album_x, Release_Date_x, Genre_x, Year_x)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row['ID'],  # ID della canzone
            row['Name_x'],  # Nome della canzone
            row['Artist_x'],  # Nome dell'artista
            row['Album_x'],  # Nome dell'album
            row['Release Date_x'],  # Data di rilascio
            row['Genre_x'],  # Genere musicale
            int(row['Year_x']) if not pd.isnull(row['Year_x']) else None  # Anno
        )
        cursor.execute(query, values)
    except mysql.connector.Error as err:
        print(f"Errore durante l'inserimento: {err}")
        continue

# Conferma le modifiche
db.commit()
print(f"Importazione completata con successo. {cursor.rowcount} righe inserite.")

# Chiudi la connessione al database
cursor.close()
db.close()





###feat non in comune


import unicodedata
import mysql.connector
import pandas as pd
import csv 

db = mysql.connector.connect(
    host="localhost",
    user="root",  # Sostituisci con il tuo username
    password="DataMan.24",  # Sostituisci con la tua password
    database="SpotifyGeniusDB"  # Nome del database
)

cursor = db.cursor()

# Query SQL per creare la nuova tabella
create_table_query = """
CREATE TABLE IF NOT EXISTS new_spotify_feat (
    Name VARCHAR(255) NOT NULL,       -- Nome della canzone
    ID VARCHAR(255) PRIMARY KEY,     -- ID della canzone
    Featuring_1 VARCHAR(255),        -- Primo artista in featuring
    Featuring_2 VARCHAR(255)         -- Secondo artista in featuring
);
"""

# Esegui la query per creare la tabella
cursor.execute(create_table_query)
db.commit()
print("Tabella 'new_spotify_feat' creata con successo.")

# Carica il dataset
csv_file = "new_spotify_feat_cleaned_updated.csv"  # Nome del file CSV
try:
    feat_data = pd.read_csv(csv_file, delimiter=',')  # Modifica il delimitatore se necessario
except Exception as e:
    print(f"Errore durante la lettura del file CSV: {e}")
    exit()

# Inserisci i dati nella tabella
insert_query = """
INSERT INTO new_spotify_feat (Name, ID, Featuring_1, Featuring_2)
VALUES (%s, %s, %s, %s)
"""

# Loop sui dati del CSV
for index, row in feat_data.iterrows():
    try:
        cursor.execute(insert_query, (
            row['Name'],
            row['ID'],
            row['Featuring_1'],
            row['Featuring_2']
        ))
    except Exception as e:
        print(f"Errore durante l'inserimento della riga {index}: {e}")

db.commit()
print("Dati importati con successo nella tabella 'new_spotify_feat'.")

# Chiudi la connessione al database
cursor.close()
db.close()


## feat in comune
import unicodedata
import mysql.connector
import pandas as pd
import csv 


db = mysql.connector.connect(
    host="localhost",
    user="root",  # Sostituisci con il tuo username
    password="DataMan.24",  # Sostituisci con la tua password
    database="SpotifyGeniusDB"  # Nome del database
)

cursor = db.cursor()

csv_file = "spotify_kaggle_feat_cleaned_updated.csv"  # Nome del file CSV
try:
    feat_data = pd.read_csv(csv_file, delimiter=',')  # Modifica il delimitatore se necessario
except Exception as e:
    print(f"Errore durante la lettura del file CSV: {e}")
    exit()

# Inserisci i dati nella tabella
insert_query = """
INSERT INTO spotify_kaggle_feat (Name, ID, Featuring_1, Featuring_2)
VALUES (%s, %s, %s, %s)
"""

# Loop sui dati del CSV
for index, row in feat_data.iterrows():
    try:
        cursor.execute(insert_query, (
            row['Name'],
            row['ID'],
            row['Featuring_1'],
            row['Featuring_2']
        ))
    except Exception as e:
        print(f"Errore durante l'inserimento della riga {index}: {e}")

db.commit()
print("Dati importati con successo nella tabella 'spotify_kaggle_feat'.")

# Chiudi la connessione al database
cursor.close()
db.close()


###lyrics in comune

# Connessione al database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Sostituisci con il tuo username
    password="DataMan.24",  # Sostituisci con la tua password
    database="SpotifyGeniusDB"  # Nome del database
)

cursor = db.cursor()

# Query SQL per creare la nuova tabella
create_table_query = """
CREATE TABLE IF NOT EXISTS spotify_kaggle_lyrics (
    ID VARCHAR(255) PRIMARY KEY,     -- ID della canzone (chiave primaria)
    Artist VARCHAR(255) NOT NULL,    -- Nome dell'artista
    Name VARCHAR(255) NOT NULL,      -- Titolo della canzone
    lyrics TEXT                      -- Testo della canzone
);
"""

# Esegui la query per creare la tabella
cursor.execute(create_table_query)
db.commit()
print("Tabella 'spotify_kaggle_lyrics' creata con successo.")

# Carica il dataset
csv_file = "lyrics_finale"  # Nome del file CSV
try:
    lyrics_data = pd.read_csv(csv_file, delimiter=',')  # Modifica il delimitatore se necessario
except Exception as e:
    print(f"Errore durante la lettura del file CSV: {e}")
    exit()

# Inserisci i dati nella tabella
insert_query = """
INSERT INTO spotify_kaggle_lyrics (ID, Artist, Name, lyrics)
VALUES (%s, %s, %s, %s)
"""

# Loop sui dati del CSV
for index, row in lyrics_data.iterrows():
    try:
        cursor.execute(insert_query, (
            row['ID'],
            row['Artist'],
            row['Name'],
            row['lyrics']
        ))
    except Exception as e:
        print(f"Errore durante l'inserimento della riga {index}: {e}")

db.commit()
print("Dati importati con successo nella tabella 'spotify_kaggle_lyrics'.")

# Chiudi la connessione al database
cursor.close()
db.close()


### lyrics non in comune

db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="DataMan.24", 
    database="SpotifyGeniusDB"  
)

cursor = db.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS spotify_lyrics (
    ID VARCHAR(255) PRIMARY KEY,     -- ID della canzone (chiave primaria)
    Artist VARCHAR(255) NOT NULL,    -- Nome dell'artista
    Name VARCHAR(255) NOT NULL,      -- Titolo della canzone
    lyrics TEXT                      -- Testo della canzone
);
"""

cursor.execute(create_table_query)
db.commit()
print("Tabella 'spotify_not_in_common_lyrics' creata con successo.")

csv_file = "lyrics_in_spotify_not_in_common.csv" 
try:
    lyrics_data = pd.read_csv(csv_file, delimiter=',') 
except Exception as e:
    print(f"Errore durante la lettura del file CSV: {e}")
    exit()

# Inserisci i dati nella tabella
insert_query = """
INSERT INTO spotify_not_in_common_lyrics (ID, Artist, Name, lyrics)
VALUES (%s, %s, %s, %s)
"""

# Loop sui dati del CSV
for index, row in lyrics_data.iterrows():
    try:
        cursor.execute(insert_query, (
            row['ID'],
            row['Artist'],
            row['Name'],
            row['lyrics']
        ))
    except Exception as e:
        print(f"Errore durante l'inserimento della riga {index}: {e}")

db.commit()
print("Dati importati con successo nella tabella 'spotify_not_in_common_lyrics'.")

# Chiudi la connessione al database
cursor.close()
db.close()
