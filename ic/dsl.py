import textx
import jinja2
import click
from os.path import dirname
import ic.filters

file_name = dirname(__file__)

def verbose_output(agents, envs):
    for agent in agents:
        click.echo(f'Agent: {agent.name}')
        click.echo('Beliefs:')
        for belief in agent.beliefs.list:
            click.echo(belief)

        click.echo('\nDesires:')
        for desire in agent.desires.list:
            click.echo(desire)

        click.echo('\nPlans:')
        for plan in agent.plans:
            click.echo(f'{plan.name}: {plan.conditions.condition} -> ', nl=False)
            if hasattr(plan.actions, 'action'):
                click.echo(plan.actions.action)
            else:
                click.echo('No action')

    for env in envs:
        click.echo('\n---------------------------')
        click.echo(f'Environment: {env.name}')
        click.echo('Perceptions:')
        for perception in env.perceptions.list:
            click.echo(perception)

        click.echo('\nActions:')
        for action in env.actions.list:
            click.echo(action)

def parse_file(file):
    # load the textx metamodel and system model
    system_metamodel = textx.metamodel_from_file(
        file_name=f'{file_name}/grammar/system.tx'
    )
    try:
        system_model = system_metamodel.model_from_file(file)
    except textx.TextXSyntaxError as e:
        click.echo(f'[ERROR] {e.message} at * position: "{e.context}"')
        exit()

    agents = system_model.agents
    envs = system_model.envs
         
    return (agents, envs)

def build_output_file(agents, envs, output_file):
    # set up jinja2 env and load templates
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(file_name),
        trim_blocks=True, lstrip_blocks=True
    )
    jinja_env.filters['contextType'] = ic.filters.context_type_to_str
    jinja_env.filters['conditionsStr'] = ic.filters.conditions_to_str
    jinja_env.filters['changeStr'] = ic.filters.change_to_srt

    agent_jinja_template = jinja_env.get_template('templates/agentTemplate.py.jinja')
    env_jinja_template = jinja_env.get_template('templates/envTemplate.py.jinja')
    main_jinja_template = jinja_env.get_template('templates/mainTemplate.py.jinja')

    with open(output_file, 'w') as f:
        f.write('from maspy import *\n')
        f.write(agent_jinja_template.render(agents=agents))
        f.write(env_jinja_template.render(envs=envs))
        f.write(main_jinja_template.render(agents=agents))