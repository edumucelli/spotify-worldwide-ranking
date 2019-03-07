# spotify-worldwide-ranking
Automate data collection from Spotify's worldwide ranking in 50+ countries. The snapshot of the data collected by the code has been published at [Kaggle datasets](https://www.kaggle.com/edumucelli/spotifys-worldwide-daily-song-ranking).

## Install:
First, install the required package dependencies:
* Using Makefile __(recomended)__
```
make install
```
* Using pip
```
pip3 install -r requirements.txt
```
## Usage
### Using make __(recomended)__
The `Makefile` included with the script can be easily modified for execution. 

Modify the variables `START_DATE`, `END_DATE`, and `REGION` and execute with `make`

### Manually
The script can be executed with `python3 spotify.py start_date end_date region`
```
usage: spotify.py [-h] start_date end_date region

Spotify Charts Data Crawler. Automatically extract data from
https://spotifycharts.com

positional arguments:
  start_date  Start date. Format: (yyyy-mm-dd)
  end_date    End date. Format: (yyy-mm-dd)
  region      A valid region code
  
optional arguments:
  -h, --help  show this help message and exit
```

## Results
The collected data will be stored on the `data/` directory.

Additionally, all errors found while collecting the data will be stored in a `log.txt` file inside `log/`
