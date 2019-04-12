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

        # Write new headers
        header = next(reader) + NEW_HEADERS
        writer.writerow(header)

        lines = [line for line in csv_input]

        # Indices
        pos_each_day_index = header.index("pos_each_day")

        songs_dict = {}

        # First Iteration: Get unique values
        for row in tqdm(csv.reader(lines), total=len(lines)):
            # URL value
            url = row[header.index("URL")]

            # Use the url of the song as the key and add if not already in dict
            if url not in songs_dict:
                row.append([])
                songs_dict[url] = row


        last_day = 1
        start_year = 2017

        # TODO: FINISH. NOT WORKING. WIP
        # Second Iteration: Count positions for each day
        for row in tqdm(csv.reader(lines), total=len(lines)):
            current_day = int(row[header.index("Day")])

            # URL value
            url = row[header.index("URL")]

            # Posiiton value
            pos = row[header.index("Position")]

            if url in songs_dict:
                songs_dict[url][pos_each_day_index].append(pos)

            if current_day != last_day:
                last_day = current_day
                month = int(row[header.index("Month")])
                year = int(row[header.index("Year")])

                year_diff = year - start_year + 1

                for song_row in songs_dict.values():
                    if(len(song_row[pos_each_day_index]) < last_day * month * year_diff):
                        song_row[pos_each_day_index].append(0)

        for song_row in songs_dict.values():
            writer.writerow(song_row);


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add audio features to .csv')
    parser.add_argument('input_file', help='input file in .csv format')
    args = parser.parse_args()

    get_unique_songs(args.input_file)
