Bibclean
=============================================

About
-----

Bibclean is a crude BibTeX parser and processing script written in Python. I wrote this utility because my reference manager (Mendeley) includes a lot of information in BibTeX export files. The script can strip undesired entries as well as convert long journal names to abbreviated names using the provided sqlite database.

Licence
-------

This project may be distributed and/or modified under the GNU Public License, specifically v3 (see the file `LICENCE`).

Usage
-----

Simply run `python bibclean.py <file.bib>`, or see the script for more command line options.

FAQ
---

Q: Can I use my own or modify the abbreviation database?

A: Yes you can. The are several helper scripts for updating the database in the folder `dbtools`. Let me start the database itself, usually called `abbr.db`. It is a simple sqlite database with the following table:

	CREATE TABLE IF NOT EXISTS journals (full TEXT, abbr TEXT)

You can insert your own entries. For consistency, entries are stored in upper case, as BibTeX will ensure correct capitalisation. his also comes from the fact that I wrote a script to scrape the abbreviation names from the Web of Knowledge listing, more on that later.

### `abbradd.py`

This script allows you to insert new names and abbreviations into the database. It loads a text file containing one full name and abbreviation per line, separated by a delimiter (usually a tab, but this can be altered via the `-d` option). These are split and inserted into the database, which is created if it doesn't exist.

### `abbrdump.py`

The script that was used to scrape all the journal names from WoK. **PLEASE**, do not run this script. The included database already contains all the abbreviations and we don't want to get banned by Thomson Reuters. It is also hacked together very shoddily. 

### `abbrquery.py`

This script can be used to query the database and check that a given journal is in the database and what it's abbreviation is.

