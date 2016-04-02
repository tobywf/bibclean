"""Web of Knowledge dump functionality and CLI entry point"""
import string
import time
from urllib.request import urlopen
import click
from bibclean.config import Config


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    pass


@cli.command()
@click.option(
    '--db', type=click.Path(exists=True),
    help='The journal abbreviations database to use.')
@click.option(
    '--no-fuzzy', is_flag=True, default=False,
    help='Disable time intensive fuzzy search for journals.')
@click.argument('journal_name')
@click.pass_context
def query(ctx, db, no_fuzzy, journal_name):
    """Query journal abbreviations database."""
    config = Config(db, not no_fuzzy)
    abbr = config.lookup(journal_name)
    if abbr:
        click.echo(abbr)
    else:
        ctx.exit(1)


@cli.command()
@click.argument('output', type=click.File('w'))
def dump(output):
    """Dump abbreviations from Web of Knowledge."""
    page_list = list(string.ascii_uppercase)
    page_list.append('0-9')
    for page_key in page_list:
        url = (
            'http://images.webofknowledge.com/WOK46/help/WOS/'
            '{}_abrvjt.html'
        ).format(page_key)
        print('Retrieving', url)
        html = urlopen(url).read().decode('cp1252')
        # the HTML is so bad that both LXML and BeautifulSoup can't handle it
        # before first definition
        start = html.find('<DT>')
        # after last definition
        end = html.find('</DL>')
        html = html[start:end]
        # get rid of tags and other stuff
        substitutions = [
            ('<DT>', ''),
            ('<DD>', ''),
            ('<B>', ''),
            ('</B>', ''),
            ('&amp;', '&'),
            ('\n\t', '\t'),
        ]
        for old, new in substitutions:
            html = html.replace(old, new)
        output.write(html)
        time.sleep(2)


@cli.command()
def write_config():
    """Create a user config file with default values."""
    path = Config.create_user_config()
    click.echo('Config written to {}'.format(path))
