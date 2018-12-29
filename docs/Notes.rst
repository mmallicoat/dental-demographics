Notes
=====

Todo
----
*   Check practice_stats.py for near-misses in address collision
*   Add PUMA descriptions from shapefiles to combined_stats.csv

Won't Do
````````
*   Estimate dentists per practice and add pop to dentist ratio

Maybe
`````
*   Maybe try to build a map with outlines for each census block
    and color scales to show each variable, each one in a separate "layer."
    (Search Census sites for info on "shape files" and GIS.)
*   Interpolate median age calculate: assume people are on average halfway
    through their age-year? Check against FactFinder.

Done
````
*   Collect additional dental location lat/long; and re-run PUMA lookup
*   Count practices, not dentists; use address (including suite number)
*   Join this number with other PUMA statistics;
    calculate the pop to practice ratio
*   Calculate number of practices for each PUMA
*   Add to state reports a column for "State" with two-letter state code [actually used the state code instead]
*   Get lat-long coordinates of each dental practice scraped
*   Find which PUMA they fall into using polygon coordinates from shapefile
*   Adjust income figures for inflation; check median income against Fact Finder
*   Locate the offices L is aware of in the census blocks / PUMAs;
    send L a table of the offices and the regional averages
*   Compile statistics into table
*   Tabulate these statistics for all PUMAs in KS and MO using ACS:
    median age, % of population above age of X, median household income.
*   Get statistics for Midwest and US total from FactFinder

Won't Do
````````
*   Repeat statistics at the lower grain of census block/tract using Census data?
*   Maybe redo household income calculations using Household records
    instead of Person records. My estimates do not match FactFinder.

Lists of Dentists
-----------------

*   https://www.healthgrades.com

GIS Libraries
-------------

*   `GeoPandas <http://geopandas.org/>`__: depends on ``shapely`` and ``fiona``
*   `Shapely <https://shapely.readthedocs.io/en/stable/>`__
*   `Fiona <https://fiona.readthedocs.io/en/latest/>`__
*   `pyshp <https://github.com/GeospatialPython/pyshp>`__
*   `geo_interface <https://gist.github.com/sgillies/2217756>`__
*   `GDAL/OGR <https://gdal.org>`__

Census Data
-----------

Decennial Census
````````````````

Last collected in 2010. Only aggregate data is available until 72
years after the census is taken. I'm not sure what the level of
aggregation is.

Wikipedia__ says that age and sex data are collected.

.. __: https://en.wikipedia.org/wiki/List_of_household_surveys_in_the_United_States

Datasets are `here <https://www.census.gov//programs-surveys/decennial-census/data/datasets.2010.html>`__.
Documentation `here <https://www.census.gov/programs-surveys/decennial-census/technical-documentation/complete-technical-documents.html>`__.

The census data is more granular than PUMS, I think, going down
to the census tract/block level. However, it does not collect
as much information on each person; e.g., I think income is not
collected.

Based on the data dictionary in the documentation for the Summary
File 1 (SF1), it seems that only population, housing counts, and
area are collected, coded by geography, Congressional district,
and other info. However, the abstract says that age, race, and
other info (but not income) are collected.

The census also releases a 10% sample of the data through PUMS.
The lowest granularity is the PUMA: "The Public Use Microdata
Sample (PUMS) files contain geographic units known as Public Use
Microdata Areas (PUMAs). To maintain the confidentiality of the
PUMS data, a minimum population threshold of 100,000 is set for
PUMAs."

Census - Demographic Profile
````````````````````````````

The Demographic Profile Summary File has demographic information,
including age and race.

The summary level 040 files do not include ZIP code. I think
summary level 871 does. However, census blocks *do* roll up to ZIP
codes.

Data includes the geographic center of the area (e.g. census
block), I think. does to the ZIP code level, perhaps. I don't know
where to get explicit boundaries of a census block. The "Tiger"
viewer lets you see them, though.

In the geographic header file, if a field is not included for a
record, blanks are placed.

This file is joined with a CSV by the logical record number. The
documentation also describes what the fields in the CSV are.

American Community Survey
`````````````````````````

This replacted the census "long form" in 2010. It contains more
detail than the census, but only for a sample of the population
rather than it entire. The data is aggregated and published annually.

Wikipedia__ says that it is collected at the *geographic summary
levels* of "states, counties, cities, and congressional districts,
as well as statistical entities such as metropolitan statistical
areas, tracts, block groups, and census designated places" but not
census blocks.

.. __: https://en.wikipedia.org/wiki/American_Community_Survey

Per the `Census site`_, all levels are available in the five-year surveys,
including the census blocks. It is also coded with "5-Digit ZIP Code Tabulation Area."

.. _`Census site`: https://www.census.gov/programs-surveys/acs/geography-acs/areas-published.html

ACS data can be downloaded by FTP here__.

.. __: https://www.census.gov/programs-surveys/acs/data/data-via-ftp.html

Downloaded:

*   ftp://ftp2.census.gov/programs-surveys/acs/summary_file/2016/data/5_year_seq_by_state/Kansas/All_Geographies_Not_Tracts_Block_Groups/g20165ks.txt
*   ftp://ftp2.census.gov/programs-surveys/acs/summary_file/2016/data/5_year_seq_by_state/Kansas/All_Geographies_Not_Tracts_Block_Groups/g20165ks.csv
*   ftp://ftp2.census.gov/programs-surveys/acs/summary_file/2016/data/2016_5yr_Summary_FileTemplates.zip
*   ftp://ftp2.census.gov/programs-surveys/acs/data/pums/2016/5-Year/csv_pks.zip
*   ftp://ftp2.census.gov/programs-surveys/acs/data/pums/2016/5-Year/csv_hks.zip
*   ftp://ftp2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_entire_sf/All_Geographies.zip

Geographic layout of counties, PUMAs, census tracks, etc. can be
viewed on TigerWeb_.

I think census tracks may be subdivisions of PUMAs, without any
crossing PUMA borders. PUMAs can cross county borders.

.. _TigerWeb: https://tigerweb.geo.census.gov/tigerweb/

PUMS documentation:
*   https://www.census.gov/programs-surveys/acs/technical-documentation/pums/documentation.2016.html
*   https://www.census.gov/programs-surveys/acs/technical-documentation/pums/documentation.html
*   https://www.census.gov/programs-surveys/acs/technical-documentation/pums/about.html

These contain a document "PUMS Estimates for User Verification"
with values for checking calculations. See chapters 11 and 12
of the "ACS Design and Methodology" report for mroe technical
details, such as to the weighting of the samples.

The presentation "Introduction to the American Community Survey
Public Use Microdata Sample (PUMS) Files" says that the microdata
(PUMS) has "[n]o geographies smaller than PUMAs." "PUMS is **not**
designed for statistical analysis of small geographic areas."

