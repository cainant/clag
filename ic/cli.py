import click

if __package__:
    from . import dsl
else:
    import dsl

@click.group
def cli():
    pass

@cli.command
@click.argument('file_name', type=click.STRING)
@click.option('--output_file', '-o', default='out.py', help='Change output file name.')
def build(file_name, output_file):
    agents, envs = dsl.parse_file(file_name)
    dsl.build_output_file(agents, envs, output_file)
    
# debug purposes
if __name__ == '__main__':
    cli()