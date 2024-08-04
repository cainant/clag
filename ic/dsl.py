from textx import metamodel_from_file
import jinja2
from os.path import dirname

def context_type_to_str(context, agent):
    for plan in agent.plans:
        if context == plan.name:
            return f'Goal("{context}")'
    
    return f'Belief("{context}")'

def verbose_output(agents, envs):
    for agent in agents:
        print(f'Agent: {agent.name}')
        print('Beliefs:')
        for belief in agent.beliefs.list:
            print(belief)

        print('\nDesires:')
        for desire in agent.desires.list:
            print(desire)

        print('\nPlans:')
        for plan in agent.plans:
            print(f'{plan.name}: {plan.conditions.condition} -> ', end='')
            if hasattr(plan.actions, 'action'):
                print(plan.actions.action)
            else:
                print('No action')

    for env in envs:
        print('\n---------------------------')
        print(f'Environment: {env.name}')
        print('Perceptions:')
        for perception in env.perceptions.list:
            print(perception)

        print('\nActions:')
        for action in env.actions.list:
            print(action)

def parse_file(file, verbose):
    system_meta = metamodel_from_file(f'{dirname(__file__)}/grammar/system.tx')
    system_model = system_meta.model_from_file(file)

    agents = system_model.agents
    envs = system_model.envs
    if verbose:
        verbose_output(agents, envs)
            
    return (agents, envs)

def build_output(agents, envs, output_file):
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(dirname(__file__)),
        trim_blocks=True, lstrip_blocks=True
    )
    jinja_env.filters['contextType'] = context_type_to_str
    jinja_agent_template = jinja_env.get_template('templates/agentTemplate.py.jinja')
    jinja_env_template = jinja_env.get_template('templates/envTemplate.py.jinja')

    with open(output_file, 'w') as f:
        f.write('from maspy import *\n')
        f.write(jinja_agent_template.render(agents=agents))
        f.write(jinja_env_template.render(envs=envs))