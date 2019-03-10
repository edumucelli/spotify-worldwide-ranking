# spotify-worldwide-ranking
Automate data collection from Spotify's worldwide ranking in 50+ countries. The snapshot of the data collected by the code has been published at [Kaggle datasets](https://www.kaggle.com/edumucelli/spotifys-worldwide-daily-song-ranking).

## Install
First, install the required package dependencies:
* Using Makefile
```
make install
```

## Usage
### Using make __(recommended)__
The `Makefile` included with the script can be easily modified for execution. 

Modify the variables `START_DATE`, `END_DATE`, and `REGION` and execute with `make`

## Results
The extracted data will be stored on the `data/` directory.
The following files will be generated:
* __region_code.csv__: Top 100 ranking
* __region_code_waf.csv__: Ranking with audio features for each song
* __region_code_waf.arff__: Same but in .arff format

Additionally, all errors found while extracting the data will be stored in a `log.txt` file inside `log/`
