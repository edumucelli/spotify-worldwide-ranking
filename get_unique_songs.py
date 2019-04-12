import argparse
import csv
import os

from tqdm import tqdm

NEW_HEADERS = ["pos_each_day"]

def get_unique_songs(input_filepath):
    region = os.path.splitext(os.path.basename(input_filepath))[0]
    output_filepath = region + '_unique.csv'

    with open(input_filepath, 'r') as csv_input, \
         open(output_filepath, 'w') as csv_output:

        reader = csv.reader(csv_input)
        writer = csv.writer(csv_output)

        header = next(reader)
        writer.writerow(header + NEW_HEADERS)

        songs_dict = {}

        lines = [line for line in csv_input]

        print(header)
        for row in tqdm(csv.reader(lines), total=len(lines)):
            url = row[header.index("URL")]

            # Use the url of the song as the key
            songs_dict[url] = row

        for song_row in songs_dict.values():
            writer.writerow(song_row);


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add audio features to .csv')
    parser.add_argument('input_file', help='input file in .csv format')
    args = parser.parse_args()

    get_unique_songs(args.input_file)
