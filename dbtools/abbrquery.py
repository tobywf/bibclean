import sqlite3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: abbrquery.py <journal name> [-f <database file>]")
    parser.add_argument(dest='query', help="The journal name to query.")
    parser.add_argument('-f', '--file', action='store_true', dest='db', default="abbr.db", help="The output database. Default is \"abbr.db\"")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()
    name = args.query.upper()
    cursor.execute("SELECT full, abbr FROM journals WHERE full=? LIMIT 1", [name])
    result = cursor.fetchone()
    if result is None:
        print "No results for {}".format(name)
    else:
        print "Query: {}. Matched: {}. Abbr: {}.".format(name, result[0], result[1])
    conn.commit()
    conn.close()
