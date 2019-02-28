# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com
# Modified for working with Python 3 at 2019-02-28: David Afonso Dorta

import os
from datetime import datetime, timedelta, date
import csv
import threading

from tqdm import tqdm
import requests

DATA_DIR = 'data'


class Collector(threading.Thread):
    def __init__(self, region, start_date, end_date):
        super(Collector, self).__init__()
        self.region = region
        self.start_date = start_date
        self.end_date = end_date
        self.base_headers = ['Position',
                             'Track Name', 'Artist', 'Streams', 'URL']

    def date_range(self):
        one_day = timedelta(days=1)
        current_date = self.start_date
        while current_date <= self.end_date:
            yield current_date
            current_date += one_day

    def is_csv_ok(self, download_content):
        csv_reader = csv.reader(download_content.splitlines(), delimiter=',')
        headers = next(csv_reader)
        return set(headers) == set(self.base_headers)

    def download_csv_file(self, url):
        with requests.Session() as session:
            download = session.get(url)

            return download.content.decode('utf-8')

    def extract_csv_rows(self, csv_file):
        csv_reader = csv.reader(csv_file.splitlines(), delimiter=',')
        # Skip headers (for some reason there's a blank line after headers)
        next(csv_reader)
        next(csv_reader)
        for row in csv_reader:
            yield row

    def run(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        headers = self.base_headers + ["Date", "Region"]

        file_path = os.path.join(DATA_DIR, "%s.csv" % self.region)
        if os.path.exists(file_path):
            print("File '%s' already exists, skipping" % file_path)

        with open(file_path, 'w', 1) as out_csv_file:
            writer = csv.writer(out_csv_file)
            writer.writerow(headers)

            for current_date in tqdm(self.date_range(),
                                     desc="Collecting from '%s'" %
                                     self.region):

                url = "https://spotifycharts.com/regional/ \
                        %s/daily/%s/download" % (self.region, current_date)

                csv_file = self.download_csv_file(url)
                if csv_file is None:
                    continue

                for row in self.extract_csv_rows(csv_file):
                    row.extend([current_date, self.region])
                    writer.writerow(row)

    @staticmethod
    def generate_final_file():
        final_filename = 'data.csv'

        with open(final_filename, 'w') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(
                ['Position', 'Track Name', 'Artist', 'Streams', 'URL'])
            for filename in tqdm(os.listdir(DATA_DIR),
                                 desc="Generating final file: %s" %
                                 final_filename):

                if filename.endswith(".csv"):
                    with open(os.path.join(DATA_DIR, filename)) as infile:
                        csv_reader = csv.reader(infile)
                        next(csv_reader)
                        for row in csv_reader:
                            csv_writer.writerow(row)


if __name__ == "__main__":

    one_day = timedelta(days=1)
    start_date = date(2017, 1, 1)
    end_date = datetime.now().date() - (2 * one_day)

    regions = ["global", "us", "gb", "ad", "ar", "at", "au", "be", "bg",
               "bo", "br", "ca", "ch", "cl", "co", "cr", "cy", "cz", "de",
               "dk", "do", "ec", "ee", "es", "fi", "fr", "gr", "gt", "hk",
               "hn", "hu", "id", "ie", "is", "it", "jp", "lt", "lu", "lv",
               "mc", "mt", "mx", "my", "ni", "nl", "no", "nz", "pa", "pe",
               "ph", "pl", "pt", "py", "se", "sg", "sk", "sv", "tr", "tw",
               "uy"]

    threads = []
    for region in regions:
        collector = Collector(region, start_date, end_date)
        collector.start()
        threads.append(collector)

    for thread in threads:
        thread.join()

    Collector.generate_final_file()
