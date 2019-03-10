START_DATE := 2017-01-01
END_DATE := 2018-12-31

# LIST OF VALID REGION CODES:
#    1: "global", "us", "gb", "ad", "ar", "at", "au", "be", "bg", "bo", "br", "ca",
#    2: "ch", "cl", "co", "cr", "cy", "cz", "de", "dk", "do", "ec", "ee", "es",
#    3: "fi", "fr", "gr", "gt", "hk", "hn", "hu", "id", "ie", "is", "it", "jp",
#    4: "lt", "lu", "lv", "mc", "mt", "mx", "my", "ni", "nl", "no", "nz", "pa",
#    5: "pe", "ph", "pl", "pt", "py", "se", "sg", "sk", "sv", "tr", "tw", "uy"

# Change this variable
REGION := bg

#### Tasks
.PHONY: all download add_features install

all:
	# Dwnload csv files
	python3 spotify.py $(START_DATE) $(END_DATE) $(REGION)
	# Add audio features
	python3 add_audio_features.py data/$(REGION).csv
	# Convert to .arff
	Rscript csv_to_arff.r data/$(REGION)_waf.csv

install:
	sudo apt install r-base
	pip3 install -r requirements.txt
