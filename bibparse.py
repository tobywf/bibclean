import string

class BibEntry(dict):
    """Represents a BibTeX entry
    """
    def __init__(self, entrytype, citekey=None, *args, **kwargs):
        super(dict, self).__init__(*args, **kwargs)
        self.entrytype = entrytype
        self.citekey = citekey

    def __str__(self):
        s = "@{} {{{},\n".format(self.entrytype, self.citekey)
        s += ",\n".join(["{} = {}".format(k, v) for k, v in sorted(self.iteritems())])
        s += "\n}\n"
        return s

    def __repr__(self):
        return self.__str__()

class BibParseError(Exception):
    """Exception for BibTeX parsing errors
    """
    def __init__(self, message, position, text):
        Exception.__init__(self, message)
        self.position = position
        self.text = text

class BibParser(object):
    """Parses BibTeX
    """
    def __init__(self, bibtext=None):
        if bibtext is not None:
            self.parse(bibtext)
    
    def skipwhitespace(self):
        """
        Advances through the parsing text until a non-whitespace character
        is found.

        Exceptions
        ----------
        BibParseError
            Thrown if the end of the text is reached before a non-whitespace
            is read.
        """
        while self.text[self.pos] in string.whitespace:
            self.pos += 1
            if self.pos == self.length:
                raise BibParseError("Unexpected end.", self.pos, self.text)
    
    def readuntil(self, delims, strip=True, append=False):
        """
        Advances through the parsing text until any string patterns in
        `delims` is found.

        Parameters
        ----------
        delims : list of strings
            The string patterns that terminate the read.
        strip : bool, optional
            `True` if the whitespace should be stripped from the read text;
            otherwise, `False`.
        append : bool, optional
            `True` if the delimiters should be appended to the read text;
            otherwise, `False`.

        Returns
        -------
        text : string
            The text until the matched delimiter.

        Exceptions
        ----------
        BibParseError
            Thrown if the end of the text is reached before a delimiter is read.

        Notes
        -----
        See also `matchatpos`.
        """
        if isinstance(delims, basestring):
            delims = [delims]
        j = self.pos
        while self.pos < self.length:
            self.pos += 1
            match = self.matchatpos(delims)
            if match:
                if append:
                    self.pos += len(match)
                text = self.text[j:self.pos]
                if not append:
                    self.pos += len(match)
                if strip:
                    return text.strip()
                return text
        raise BibParseError("Unexpected end.", self.pos, self.text)
    
    def matchatpos(self, matches):
        """
        Matches any string patterns in `matches` at the current position.

        Parameters
        ----------
        matches : list of strings
            The string patterns to match.

        Returns
        -------
        match : string or bool
            The matched pattern or `False` if no match was found.
        """
        for match in matches:
            n = len(match)
            if self.text[self.pos:self.pos+n] == match:
                return match
        return False
    
    def parse(self, bibtext):
        """
        Parses BibTeX. Resulting BibTeX entries are contained in `self.entries`.

        Parameters
        ----------
        bibtext : string
            The BibTeX string to parse.

        Exceptions
        ----------
        BibParseError
            Thrown if a parsing error occurred.
        """
        self.pos = 0
        self.text = bibtext
        self.length = len(self.text)
        self.entries = []
        
        curentry = None
        
        while self.pos < self.length:
            # skip whitespace, ignore end of text exception.
            try:
                self.skipwhitespace()
            except BibParseError:
                break
            if self.text[self.pos] == "@":
                # BibTeX entry
                self.pos += 1
                entrytype = self.readuntil("{")
                citekey = self.readuntil(",")
                curentry = BibEntry(entrytype, citekey)
                self.entries.append(curentry)
            else:
                # BibTeX entry item
                if curentry is None:
                    # no current entry
                    raise BibParseError("Entry expected.", self.pos, self.text)
                itemkey = self.readuntil("=")
                self.skipwhitespace()
                # several possibilities for item delimiters:
                # {{}}, {}, "" or simply delimited with a ',' or '}'
                # ('}' only occurs at the end of an entry)
                match = self.matchatpos(["{{", "{", "\""])
                if not match:
                    itemdata = self.readuntil([",", "}"])
                    self.pos -= 1
                else:
                    # closing delimiter
                    match = {
                        "{{": "}}",
                        "{": "}",
                        "\"": "\""
                    }.get(match)
                    itemdata = self.readuntil(match, append=True)
                curentry[itemkey] = itemdata
                self.skipwhitespace()
                if self.text[self.pos] == "}":
                    curentry = None
                elif self.text[self.pos] != ",":
                    raise BibParseError("Unexpected character", self.pos, self.text)
                self.pos += 1
        self.pos = 0
