"""Main CLI entry points"""
import click
import bibtexparser
from bibclean.config import Config


def filter_entry(config, entry):
    entry_id = entry['ID']
    entry_tp = entry['ENTRYTYPE']
    keys = set(entry.keys())
    for key in keys - config.allowed:
        del entry[key]
    for key in keys & config.remove:
        del entry[key]
    entry['ID'] = entry_id
    entry['ENTRYTYPE'] = entry_tp


# pylint: disable=too-many-arguments,redefined-builtin
@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option()
@click.option(
    '--db', type=click.Path(exists=True),
    help='The journal abbreviations database to use.')
@click.option(
    '--fuzzy/--no-fuzzy', is_flag=True, default=None,
    help='Perform a fuzzy search for journals. Time intensive.')
@click.option(
    '--no-abbr', is_flag=True, default=False,
    help='Do not abbreviate journal names.')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.pass_context
def cli(ctx, db, fuzzy, no_abbr, input, output):
    config = Config(db, fuzzy)

    with open(input, 'r', encoding='utf-8') as fp:
        bib = bibtexparser.load(fp)

    failed = False
    for entry in bib.entries:
        filter_entry(config, entry)

        if no_abbr:
            continue
        try:
            journal_name = entry['journal']
        except KeyError:
            continue
        else:
            abbr = config.lookup(journal_name)
        if abbr:
            entry['journal'] = abbr
        else:
            failed = True

    with open(output, 'w', encoding='utf-8') as fp:
        bibtexparser.dump(bib, fp)

    if failed:
        ctx.exit(1)
