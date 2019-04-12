import argparse
import csv
import os

from tqdm import tqdm

NEW_HEADERS = ["top_pos", "pos_area", "pos_each_day"]


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
        top_pos_index = header.index("top_pos")
        pos_each_day_index = header.index("pos_each_day")
        pos_area_index = header.index("pos_area")

        songs_dict = {}

        # First Iteration: Get unique values
        for row in tqdm(csv.reader(lines), total=len(lines)):
            # URL value
            url = row[header.index("URL")]

            # Use the url of the song as the key and add if not already in dict
            if url not in songs_dict:
                row.append([])  # TODO: Make better
                row.append([])
                row.append([])
                songs_dict[url] = row

        last_day = 1
        iter_day = 1

        # Second Iteration: Track the position value for each song each day
        for row in tqdm(csv.reader(lines), total=len(lines)):
            # Current day value
            current_day = int(row[header.index("Day")])
            # URL value
            url = row[header.index("URL")]
            # Posiiton value
            pos = int(row[header.index("Position")])

            if url in songs_dict:
                songs_dict[url][pos_each_day_index].append(pos)

            if current_day != last_day:
                last_day = current_day

                for song_row in songs_dict.values():
                    if (len(song_row[pos_each_day_index]) < iter_day):
                        song_row[pos_each_day_index].append(0)

                iter_day += 1

        # Third iteration: Calculate the area for each song and the top pos
        for song_row in tqdm(songs_dict.values(), total=len(songs_dict)):
            # Get song area
            song_row[pos_area_index] = sum(
                map(lambda x: 0 if x == 0 else 101 - x,
                    song_row[pos_each_day_index]))

            # Get top pos
            song_row[top_pos_index] = max(song_row[pos_each_day_index])

        # Write the results to the output .csv
        for song_row in tqdm(songs_dict.values(), total=len(songs_dict)):
            if (len(song_row[pos_each_day_index]) < iter_day):
                song_row[pos_each_day_index].append(0)

            writer.writerow(song_row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add audio features to .csv')
    parser.add_argument('input_file', help='input file in .csv format')
    args = parser.parse_args()

    get_unique_songs(args.input_file)
