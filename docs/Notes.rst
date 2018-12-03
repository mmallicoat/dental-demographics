Notes
=====

Todo
----

*   Tabulate these statistics for all census blocks in KS and MO,
    for the states of KS and MO, the Midwest division, and the entire US:
    median age, % of population above age of X, median household income.
*   Locate the offices L is aware of in the census blocks;
    show a table of the offices and the regional averages
*   Maybe try to build a map with outlines for each census block
    and color scales to show each variable, each one in a separate "layer."


Census Data
-----------

Decennial Census
````````````````

Last collected in 2010. Only aggregate data is available until 72
years after the census is taken. I'm not sure what the level of
aggregation is.

Wikipedia__ says that age and sex data are collected.

.. __: https://en.wikipedia.org/wiki/List_of_household_surveys_in_the_United_States

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

