#!/bin/bash
echo "Sorting Files Alphabetically"
sort -u biomarkers.txt -o biomarkers.txt
sort -u devices.txt -o devices.txt
sort -u drugs.txt -o drugs.txt
sort -u non-drugs.txt -o non-drugs.txt
