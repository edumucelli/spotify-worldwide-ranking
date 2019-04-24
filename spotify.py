# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com
# Modified for working with Python 3 at 2019-02-28: David Afonso Dorta

import os
from datetime import timedelta, date, datetime
import csv
import threading
import requests
import argparse

from tqdm import tqdm

# Constants
DATA_DIR = 'data'
LOG_DIR = 'log'

TOP_ROWS = 100
ONE_DAY = timedelta(days=1)

REGIONS = [
    "global", "us", "gb", "ad", "ar", "at", "au", "be", "bg", "bo", "br", "ca",
    "ch", "cl", "co", "cr", "cy", "cz", "de", "dk", "do", "ec", "ee", "es",
    "fi", "fr", "gr", "gt", "hk", "hn", "hu", "id", "ie", "is", "it", "jp",
    "lt", "lu", "lv", "mc", "mt", "mx", "my", "ni", "nl", "no", "nz", "pa",
    "pe", "ph", "pl", "pt", "py", "se", "sg", "sk", "sv", "tr", "tw", "uy"
]


class Collector(threading.Thread):
    def __init__(self, region, start_date, end_date):
        super(Collector, self).__init__()
        self.region = region
        self.start_date = start_date
        self.end_date = end_date
        self.base_headers = [
            'Position', 'Track Name', 'Artist', 'Streams', 'URL', 'Year',
            'Month', 'Day', 'Region'
        ]

    def date_range(self):
        current_date = self.start_date
        while current_date <= self.end_date:
            yield current_date
            current_date += ONE_DAY

    def download_csv_file(self, url):
        with requests.Session() as session:
            download = session.get(url)

            return download.content.decode('utf-8')

    def extract_csv_rows(self, csv_file):
        csv_reader = csv.reader(csv_file.splitlines(), delimiter=',')

        # Skip headers
        next(csv_reader)

        for row in csv_reader:
            yield row

    def run(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        file_path = os.path.join(DATA_DIR, "%s.csv" % self.region)
        log_path = os.path.join(LOG_DIR, "%s_log.txt" % self.region)

        with open(file_path, 'w', 1) as out_csv_file, \
             open(log_path, 'w', 1) as log_file:

            writer = csv.writer(out_csv_file)
            writer.writerow(self.base_headers)

            for current_date in tqdm(
                    self.date_range(),
                    desc="Collecting from '%s'" % self.region):

                url = "https://spotifycharts.com/regional/%s/daily/%s/download" % (
                    self.region, current_date)
                print(" " + url)

                csv_file = self.download_csv_file(url)
                if csv_file is None:
                    message = "Error getting .csv on %s" % current_date
                    print(message)
                    log_file.write(message)
                    continue

                i = 0
                for row in self.extract_csv_rows(csv_file):

                    try:
                        if row[0].isdigit() and i < TOP_ROWS:
                            row.extend([
                                current_date.year, current_date.month,
                                current_date.day, self.region
                            ])
                            writer.writerow(row)
                            i += 1

                    except IndexError:
                        message = "[%s]: Invalid .csv\n" % current_date
                        i = TOP_ROWS
                        print(message)
                        log_file.write(message)
                        break

                if i < TOP_ROWS:
                    message = "[%s]: only %d rows\n" % (current_date, i)
                    print(message)
                    log_file.write(message)

    @staticmethod
    def generate_final_file():
        final_filename = 'data.csv'

        with open(final_filename, 'w') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(
                ['Position', 'Track Name', 'Artist', 'Streams', 'URL'])
            for filename in tqdm(
                    os.listdir(DATA_DIR),
                    desc="Generating final file: %s" % final_filename):

                if filename.endswith(".csv"):
                    with open(os.path.join(DATA_DIR, filename)) as infile:
                        csv_reader = csv.reader(infile)
                        next(csv_reader)
                        for row in csv_reader:
                            csv_writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Spotify Charts Data Crawler.\nAutomatically extract data \
        from https://spotifycharts.com")

    parser.add_argument('start_date', help="Start date. Format: (yyyy-mm-dd)")
    parser.add_argument('end_date', help="End date. Format: (yyy-mm-dd)")
    parser.add_argument('region', help="A valid region code")
    args = parser.parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
        region = args.region

        if region not in REGIONS:
            raise ValueError('Invalid region code: %s' % region)

        collector = Collector(region, start_date, end_date)
        collector.start()

    except Exception as error:
        print("Error while parsing the attributes: %s" % error)
