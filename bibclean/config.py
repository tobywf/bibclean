"""Bibclean config object, wraps journal abbreviation database functions"""
import json
import os
import os.path
import pkg_resources
import click
import fuzzywuzzy.process


class Config(object):
    USER_SETTINGS = os.path.join(click.get_app_dir('bibclean'), 'config.json')

    @staticmethod
    def create_user_config():
        # os.open and os.makedirs only use mode for create
        # so if the user changes the mode, don't clobber mode via clumsy chmod
        os.makedirs(
            os.path.dirname(Config.USER_SETTINGS),
            mode=0o700,
            exist_ok=True)
        descriptor = os.open(
            Config.USER_SETTINGS,
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            mode=0o600)
        with os.fdopen(descriptor, 'w') as f:
            f.write(Config.get_resource('defaults.json'))
        return Config.USER_SETTINGS

    @staticmethod
    def get_resource(resource):
        return pkg_resources.resource_string(
            __name__, 'data/' + resource).decode('utf-8')

    def __init__(self, db, fuzzy):
        self._config = json.loads(self.get_resource('defaults.json'))
        try:
            with open(self.USER_SETTINGS, 'r', encoding='utf-8') as fp:
                self._config.update(json.load(fp))
        except FileNotFoundError:
            pass

        if fuzzy is not None:
            self.fuzzy = fuzzy
        else:
            self.fuzzy = self._config.get('default_fuzzy', False)
        self.allowed = set(self._config.get('allowed', []))
        self.remove = set(self._config.get('remove', []))

        self._lookup = {}
        self._reverse = []
        try:
            if db is None:  # no CLI override?
                db = self._config.get('abbreviations', None)
            if db:
                fp = open(db, 'r', encoding='utf-8')
            else:
                fp = self.get_resource('abbr.txt').splitlines()
            for line in fp:
                name, abbr = line.split('\t')
                abbr = abbr.rstrip()
                self._lookup[name] = abbr
                self._reverse.append(abbr)
        finally:
            if db:
                fp.close()

    def lookup(self, journal_name):
        journal_name = journal_name.upper()
        if journal_name in self._reverse:
            return journal_name  # already abbreviated
        try:
            abbr = self._lookup[journal_name]
        except KeyError:
            click.echo('{} not found'.format(journal_name), nl=False)
            if self.fuzzy:
                click.echo(', did you mean:')
                bests = fuzzywuzzy.process.extractBests(
                    journal_name,
                    self._lookup.keys(),
                    limit=5
                )
                for best, _ in bests:
                    click.echo(best)
            else:
                click.echo()
            return None
        else:
            return abbr
