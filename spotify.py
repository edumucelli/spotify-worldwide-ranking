# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com

import os
from datetime import datetime, timedelta, date
import csv
import threading

from tqdm import tqdm
import requests

DATA_DIRECTORY = 'data'


class Collector(threading.Thread):
    def __init__(self, region, start_date, end_date):
        super(Collector, self).__init__()
        self.region = region
        self.start_date = start_date
        self.end_date = end_date
        self.base_headers = ['Position', 'Track Name', 'Artist', 'Streams', 'URL']

    def date_range(self):
        one_day = timedelta(days=1)
        current_date = self.start_date
        while current_date <= self.end_date:
            yield current_date
            current_date += one_day

    def is_csv_ok(self, download_content):
        csv_reader = csv.reader(download_content.splitlines()[1:], delimiter=',')
        headers = csv_reader.next()
        return set(headers) == set(self.base_headers)

    def download_csv_file(self, url):
        with requests.Session() as session:
            session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    'Accept-Encoding': 'gzip, deflate',
                                    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                                    'Connection': 'keep-alive',
                                    # 'Cookie': 'X-Mapping-jfgkgcmo=C2ECD7B19B260AB2D849DAB632033510; laravel_session=eyJpdiI6ImZFN2lLOEFNVmhndDFrUDc5QmVrdXc9PSIsInZhbHVlIjoiU21zYTFpQUljaTF1cmJnN1kzVm5mbVFJZldzTzQ5ZGZIWWNpZnJKRU1ubkZlU1FBOTRxSGpiaXljMGVcL3NObGF4Zm5VUjllQ0Yxb0R2RnJveXVDcktBPT0iLCJtYWMiOiI4MjY5MTdmMGMzNWIwMDU3OGYyY2Q0MjZlZmEzNmM0NjNlOGU1MTk0NmNjODU0M2I3MTc1NjEwNTJiZTEzOTQyIn0%3D; _ga=GA1.2.852419413.1501944945; _gid=GA1.2.288555599.1501944945; XSRF-TOKEN=eyJpdiI6IjNCY2tEakUwb28ycFVCUDFrYWtxTGc9PSIsInZhbHVlIjoiR05vS0lhalQ1WEtiejBGd1Z2cnZaREdlczlcLzNNdU1UdjI2b1FReGN6cFZEV1pnbmVlVHRURU9JVm40MDlmcDRpVTFmaGtQbG41UElcL0NJdjJueVlwdz09IiwibWFjIjoiNTcyOTI2NDczZjhiNjRkYTYxYzM0N2Y2ZGVmMWU4YjI0NTI3MDk4OThiNTkwNThiNDc0ODRiMTU4MjNjOTRhNyJ9; 9725eef18a75e1784d10b0949938c4d45f081300=eyJpdiI6InBicWZMQlRtZUoycUlKd0ZSQ05SM3c9PSIsInZhbHVlIjoib2o1VFJGSTdhakhtVDhyXC9xWVVuN0RobzhNOVBVT2crRmg0NFNrNGhTcEI4XC9qSEpuYUliVGdOZXZMU3JxRWxoS1d3UmpBRkRhR0EwMHRwSDE5MVA3U3dNbEZXSER6RHErTmlcL2tvbFZHNTN5XC9tQjBSb0JuQnFMdUJkZzNDTlZLeUdqeDRYaGRJXC92VG5qVTVyWkgxSGlweWlIM1JNbzBSSDZwQ0xXS1ZuUEZJTElpa3pPYnNOS1JSYXFCUXQ1MDduZVl5VHZhczJLaUNIVzVWYnMyWlwvQW1WdUJ3MWU3ek1pOU5ocEFYYjY4eUlabTNUWFUyWnRaVTFaZ0RWN0lYRm0zb0V4K2R4YklcLzdPdUY3eFg4elNKTGNSVDd5Skhicm1JQUN3NCt1MmQwVlhcL0xuOFVcL1lpMHk3bG1iTmFzWVN4dlU1Rk54dDJqOVdkSkozcmt1WU1CN3NjQm9KVnVLUmQxS1cxaGxtenhtNlljSmFaclNoeHROU1hWaCtNSGViZFRXcTJMallcL3ljNnpmNlJwRUJTWEE9PSIsIm1hYyI6Ijk1YWQ5NmVlYWI4MDA3ZTMwZTYyMjc3NjY5NDNmMzI5NjE0YmE5NzU2NDE0MzRjNDNmNjFjN2NhNmYwNzYzYWIifQ%3D%3D; _gat=1',
                                    'Host': 'spotifycharts.com',
                                    'Referer': 'https://spotifycharts.com/regional/ad/weekly/latest',
                                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'})
            retry = 3
            while True:
                download = session.get(url)
                if self.is_csv_ok(download.content):
                    return download.content
                print "Retrying for '%s'" % url
                retry -= 1
                if retry <= 0:
                    print "Retry failed for '%s'" % url
                    return None

    def extract_csv_rows(self, csv_file):
        csv_reader = csv.reader(csv_file.splitlines(), delimiter=',')
        # Skip headers
        csv_reader.next()
        for row in csv_reader:
            yield row

    def run(self):
        if not os.path.exists(DATA_DIRECTORY):
            os.makedirs(DATA_DIRECTORY)

        headers = self.base_headers + ["Date", "Region"]

        file_path = os.path.join(DATA_DIRECTORY, "%s.csv" % self.region)
        if os.path.exists(file_path):
            print "File '%s' already exists, skipping" % file_path

        with open(file_path, 'wb', 1) as out_csv_file:
            writer = csv.writer(out_csv_file)
            writer.writerow(headers)

            for current_date in tqdm(self.date_range(), desc="Collecting from '%s'" % self.region):
                url = "https://spotifycharts.com/regional/%s/daily/%s/download" % (self.region, current_date)
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
            csv_writer.writerow(['Position', 'Track Name', 'Artist', 'Streams', 'URL'])
            for filename in tqdm(os.listdir(DATA_DIRECTORY), desc="Generating final file: %s" % final_filename):
                if filename.endswith(".csv"):
                    with open(os.path.join(DATA_DIRECTORY, filename)) as infile:
                        csv_reader = csv.reader(infile)
                        csv_reader.next()
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
               "ph", "pl", "pt", "py", "se", "sg", "sk", "sv", "tr", "tw", "uy"]

    for region in regions:
        collector = Collector(region, start_date, end_date)
        collector.start()
    Collector.generate_final_file()
