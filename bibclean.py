
if __name__ == "__main__":
    import os
    import argparse
    
    parser = argparse.ArgumentParser(description="Usage: bibclean.py <input.bib> [-o <output.bib>] [-j/-a/-r/-s/-d]")

    allowedkeys = "address,arxivId,author,eprint,isbn,journal,publisher,month,number,pages,primaryClass,title,volume,year"

    parser.add_argument(dest='input', help="The input BibTeX file.")
    parser.add_argument('-j', '--journalabbr', action='store_true', dest='journalabbr', default=False, help="Journal abbreviations should be used.")
    parser.add_argument('-a', '--allowed', action='store_true', dest='allowedkeys', default=allowedkeys, help="List of BibTeX keys in entries to allow, comma separated.")
    parser.add_argument('-r', '--remove', action='store_true', dest='removekeys', default=None, help="List of BibTeX keys in entries to remove, comma separated.")
    #parser.add_argument('-s', '--sub', action='store_true', dest='journalsub', default=False, help="Journal abbreviations should be used.")
    parser.add_argument('-d', '--database', action='store_true', dest='database', default='abbr.db', help="Database with journal abbreviations.")
    parser.add_argument('-o', '--output', action='store_true', dest='outputfile', default=None, help="The output BibTeX file")

    args = parser.parse_args()

    with open(args.input, "r") as f:
        text = f.read()

    from bibparse import BibParser

    parser = BibParser(bibtext=text)

    if not args.allowedkeys is None:
        allowedkeys = args.allowedkeys.split(",")
        for entry in parser.entries:
            for k in entry.keys():
                if k not in allowedkeys:
                    del entry[k]

    if not args.removekeys is None:
        removekeys = args.removekeys.split(",")
        for entry in parser.entries:
            for k in entry.keys():
                if k in removekeys:
                    del entry[k]

    if args.journalabbr:
        import sqlite3
        conn = sqlite3.connect(args.database)
        cursor = conn.cursor()

        for entry in parser.entries:
            if not "journal" in entry:
                continue
            journal = entry["journal"]
            if (journal[0] == "{" and journal[-1] == "}") or (journal[0] == "\"" and journal[-1] == "\""):
                journal = journal[1:-1]
            journal = journal.replace(".", "").replace("\&", "AND").replace(": ", "-").upper()
            cursor.execute("SELECT full, abbr FROM journals WHERE full=? LIMIT 1", [journal])
            result = cursor.fetchone()
            if result is None:
                cursor.execute("SELECT full, abbr FROM journals WHERE full LIKE ? LIMIT 1", [journal[:20] + "%"])
                result = cursor.fetchone()
                if result is None:
                    print "WARN: No abbreviation results for {}.".format(journal)
                else:
                    print "WARN: Found similar journal {} for {}.".format(result[0], journal)
            if result is not None:
                entry["journal"] = "{{" + result[1].title() + "}}"
        conn.close()

    if args.outputfile is None:
        output = args.inputfile
    else:
        output = args.outputfile
    
    with open(output, "w") as f:
        for entry in parser.entries:
            f.write(entry.__str__())
