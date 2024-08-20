import click

import ic.dsl

@click.group
def cli():
    pass

@cli.command
@click.argument('file_name', type=click.STRING)
@click.option('--output_file', '-o', default='out.py', help='Change output file name.')
def build(file_name, output_file):
    agents, envs = ic.dsl.parse_file(file_name)
    ic.dsl.build_output_file(agents, envs, output_file)
    
# debug purposes
if __name__ == '__main__':
    cli()