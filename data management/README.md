# Music Data Integration and Management

Data Management Project — MSc in Data Science  
University of Milano-Bicocca

## Overview

Data management project focused on building an integrated music dataset combining **Spotify metadata, audio features and song lyrics**.

Data were collected from three heterogeneous sources: the **Spotify API**, multiple **Kaggle datasets**, and **AZLyrics** through web scraping. The resulting data were cleaned, harmonised and integrated into a relational database designed to support future analyses such as sentiment analysis, music clustering and trend exploration.

The project covers the complete data lifecycle, from acquisition and integration to data-quality assessment and relational storage.

## Pipeline

Spotify's API was used to collect the **Top 50 Global Songs from 2020 to 2023**, including track metadata, artists, albums, release dates and genres.

Kaggle datasets were integrated to enrich the tracks with audio features such as **danceability, energy, acousticness, valence, tempo, loudness and instrumentalness**.

Song lyrics were collected from **AZLyrics** through a custom web-scraping pipeline with URL generation, artist-name normalization and multiple fallback patterns.

Heterogeneous schemas were standardised before merging the different sources. Track IDs were used as the primary integration key, with additional matching based on artist and track names when necessary.

The final data architecture was designed using a **relational E-R model** and stored in **MySQL**, separating song metadata, audio features, collaborations and lyrics.

## Outcomes

- Integrated Spotify, Kaggle and AZLyrics data into a unified music dataset
- Collected data for global top songs across **2020–2023**
- Recovered missing Spotify identifiers through API queries
- Standardised heterogeneous schemas and naming conventions
- Implemented duplicate detection and missing-data quality checks
- Built a relational database supporting structured metadata, audio features, collaborations and lyrics
- Preserved raw lyrics for future NLP and sentiment-analysis applications

## Technologies

`Python` · `SQL` · `MySQL` · `Spotify API` · `Spotipy` · `Pandas` · `Requests` · `BeautifulSoup` · `Regular Expressions` · `mysql.connector`

## Methods

`Data Acquisition` · `REST API Integration` · `Web Scraping` · `Data Cleaning` · `Schema Harmonisation` · `Data Integration` · `Record Linkage` · `String Matching` · `Deduplication` · `Data Quality Assessment` · `Relational Data Modeling` · `E-R Modeling` · `ETL`

## Repository

This repository contains the project report and the **Python implementation of the complete data acquisition, integration, cleaning and database-loading pipeline**.
