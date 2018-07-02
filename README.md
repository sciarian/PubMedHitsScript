# PubMedHitsScript

About
------
This script will search queries for the pub med data bases for a cell lines primary name and each one of its alias
in combination with a list of search terms based on the Site Primary of the cell line.

Query Example
--------------
Say we were making queries the cell line 143B
with aliases : 143b, 143 B, 143B TK-, 143BTK-, 143TK-, HOS-143B, HOS-143b, GM05887
primary site : bone
and related search terms (As a result of having bone as the primary site) : bone , sarcoma

Resulting queries for the cell line name and for each alias...

(143B and bone) and (143B and sarcoma)
...

Running The Script
------------------
Download the following files and place them in the same directory:
- pub_med_script.py
- cell_lines.csv

To run the script use the following command
"python pub_med_script.py"

To save the output of the script simply pipe the output of it to a .csv file
"python pub_med_script.py > output_file.csv"
