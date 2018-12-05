# Download KS data
data/raw/ss16pks.csv:
	curl ftp://ftp2.census.gov/programs-surveys/acs/data/pums/2016/5-Year/csv_pks.zip -o data/raw/ACS/csv_pks.zip
	unzip data/raw/ACS/csv_pks.zip
	mv data/raw/ACS/csv_pks/ss16pks.csv data/raw

# Download MO data
data/raw/ss16pmo.csv:
	curl ftp://ftp2.census.gov/programs-surveys/acs/data/pums/2016/5-Year/csv_pmo.zip -o data/raw/ACS/csv_pmo.zip
	unzip data/raw/ACS/csv_pmo.zip -d data/raw/ACS/csv_pmo
	mv data/raw/ACS/csv_pmo/ss16pmo.csv data/raw

# Stats for KS
models/ks_puma_stats.csv:
	python src/state_stats.py data/raw/ss16pks.csv models/ks_puma_stats.csv

# Stats for MO
models/mo_puma_stats.csv:
	python src/state_stats.py data/raw/ss16pmo.csv models/mo_puma_stats.csv
