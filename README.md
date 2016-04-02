Bibclean
========

About
-----

Bibclean processes BibTeX bibliographies to remove/strip unwanted entries, and
abbreviate long journal names. I wrote this utility because my reference
manager (Mendeley) includes a lot of extra information in exported BibTeX
files, and because I find bibliographies using "P Roy Soc A–Math Phy" much more
readable than "Proceedings of the Royal Society A: Mathematical and Physical
Sciences". Long journal names can quickly bloat any bibliography.

Installation
------------

A virtualenv is recommended.

```shell
python setup.py install
```

This will install two executables: `bibclean` and `bibextra`.

bibclean
--------

`bibclean` provides the main functionality.

### Fuzzy search

If the exact full journal name wasn't found in the abbreviations database,
`bibclean` can perform a fuzzy search and report the top five matches. By
default, fuzzy search is disabled, because it is very time intensive.

bibextra
--------

`bibextra` contains the following utility functions:

* `dump`: scrape all the journal abbreviations from the Web of Knowledge site.
  **PLEASE** do not run this without reason. The included database already
  contains all the abbreviations already.

* `query`: query the journal abbreviations database. By default, this will
  perform a fuzzy search if the exact journal name wasn't found.

* `write_config`: writes a copy of the default configuration to the default
  user configuration directory (the exact path is printed on success).

The precedent of settings is `default` < `user` < `command-line`.
