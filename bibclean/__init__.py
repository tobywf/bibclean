import click

# monkey-patch click to show more verbose usage message every time
click.Context.get_usage = click.Context.get_help
