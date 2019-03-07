import argparse
import csv
import os

from tqdm import tqdm

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

MAX_ROW_BATCH = 50

CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(
    client_id='921cd58da9e24cefb5b4e666007085e5',
    client_secret='dda0f3da4fc04e879e37a6289999fb6c')

SP = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

NEW_HEADERS = [
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
    'duration_ms', 'time_signature'
]


def add_audio_features_to_csv(input_filepath):
    output_filepath = os.path.splitext(input_filepath)[0] + '_waf.csv'

    with open(input_filepath, 'r') as csv_input, \
            open(output_filepath, 'w') as csv_output:

        # Csv files
        reader = csv.reader(csv_input)
        writer = csv.writer(csv_output)

        # Skip header and get the index of the 'URL' column
        header = next(reader)
        url_header_index = header.index('URL')

        # Extend the header with the new columns and write to output file
        writer.writerow(header + NEW_HEADERS)

        # Array holding the read rows still to be written
        stored_rows = []

        # Count the num of lines the csv file has (used for the progress bar)
        lines = [line for line in csv_input]

        row_count = 0
        for row in tqdm(csv.reader(lines), total=len(lines)):
            row_count += 1
            stored_rows.append(row)

            # 'Continue' accumulating songs in 'stored_rows'
            if row_count < MAX_ROW_BATCH:
                continue

            # Once we have accumulated enough songs, bach process them
            song_ids = [r[url_header_index] for r in stored_rows]
            features = SP.audio_features(song_ids)

            for song, feature in zip(stored_rows, features):
                for column in NEW_HEADERS:
                    song.append(feature[column])

                print(song)
                writer.writerow(song)

            # Reset array and start accumulating the next batch again
            row_count = 0
            del stored_rows[:]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add audio features to .csv')
    parser.add_argument('input_file', help='input file in .csv format')
    args = parser.parse_args()

    add_audio_features_to_csv(args.input_file)
