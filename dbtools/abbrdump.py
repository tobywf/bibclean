import urllib
import string
import re
import argparse

def fetch_html():
    pages = list(string.ascii_uppercase)
    pages.append("0-9")
    #pages = "A"
    for page in pages:
        url = "http://images.webofknowledge.com/WOK46/help/WOS/{}_abrvjt.html".format(page)
        print "Retrieving {}...".format(url)
        yield urllib.urlopen(url).read()

def strip_html(html, delim):
    whitespace = re.compile("[^\S ]+")
    #wordchars = re.compile("[A-Z0-9 \-\t\n&,:'+./?*;!\"]+")
    
    # find definition list start
    start = html.find("<DL>")
    # find first definition term (skip misplaced anchor)
    start = html.find("<DT>", start)
    # find definition list end
    end = html.find("</DL>")
    # cut out dl markup
    strip = html[start+4:end-5]
    # normalise HTML
    strip = strip.replace("&amp;", "&").replace("<D>", "")
    # replace bold tags (these are oddly placed and wrap the DT elements)
    strip = strip.replace("<B>", "").replace("</B>", "")
    # replace whitespace characters (not spaces)
    strip = whitespace.sub("", strip)
    # replace "<DD>" with delimiter
    strip = strip.replace("<DD>", delim)
    # split lines
    strip = strip.replace("<DT>", "\n")
    # strip whitespace, add newline at end
    strip = strip.strip() + "\n"
    #print wordchars.sub("", strip)
    return strip

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: abbrdump.py [-d <delim>] [-o <output>]")
    parser.add_argument('-o', '--output', action='store_true', dest='output', default="dump.txt", help="The output file. Default is \"dump.txt\"")
    parser.add_argument('-d', '--delim', action='store_true', dest='delim', default="\t", help="The delimiter for abbreviations. Default is a tab \"\\t\"")
    args = parser.parse_args()

    with open(args.output, "w") as f:
        for html in fetch_html():
            f.write(strip_html(html, args.delim))
