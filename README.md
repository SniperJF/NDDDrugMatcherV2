# NDDDrugMatcher
This repository contains code used to parse SQL query results (in csv) from ClinicalTrials.gov that are then processed to identify drugs used in separate trials dealing with separate Neuro Degenerate diseases (NDD) or drugs used in the same trial for different NDD

Note/Credit: Organization of this data follows the "Clinical Trials Transformation Initiative." http://www.ctti-clinicaltrials.org.
They have a relational database conversion of the XML raw data from ClinicaTtrials.gov
Check them out!

This Repository Continues the work of https://github.com/SniperJF/NDDDrugMatcher after completion of V1

#Before you RUN: insert query files into queries directory.

#RUN AS:

#First:
time python3 nddfilter.py

#Next:
time python3 drugmatcherv6.py

#Then look at output folder for results


