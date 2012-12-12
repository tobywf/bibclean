import sqlite3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: abbradd.py <input> [-d <delim>] [-f <database file>]")
    parser.add_argument(dest='input', help="The input file. One journal full name and abbreviation per line, separated by the delimiter specified.")
    parser.add_argument('-d', '--delim', action='store_true', dest='delim', default="\t", help="The delimiter for abbreviations. Default is a tab \"\\t\"")
    parser.add_argument('-f', '--file', action='store_true', dest='db', default="abbr.db", help="The output database. Default is \"abbr.db\"")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS journals (full TEXT, abbr TEXT)")

    with open(args.input, "r") as f:
        lines = f.readlines()

    values = [line.upper().split(args.delim) for line in lines]
    cursor.executemany("INSERT INTO journals VALUES (?,?)", values)

    conn.commit()
    conn.close()
