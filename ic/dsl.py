import textx
import jinja2
from os.path import dirname

file_name = dirname(__file__)

def context_type_to_str(context, agent):
    # check if context is a belief or a goal
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
    # load the system textx model
    system_meta = textx.metamodel_from_file(f'{file_name}/grammar/system.tx')
    system_model = system_meta.model_from_file(file)

    agents = system_model.agents
    envs = system_model.envs
    if verbose:
        verbose_output(agents, envs)
            
    return (agents, envs)

def build_output_file(agents, envs, output_file):
    # load the jinja2 templates
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(file_name),
        trim_blocks=True, lstrip_blocks=True
    )
    jinja_env.filters['contextType'] = context_type_to_str
    jinja_agent_template = jinja_env.get_template('templates/agentTemplate.py.jinja')
    jinja_env_template = jinja_env.get_template('templates/envTemplate.py.jinja')
    jinja_main_template = jinja_env.get_template('templates/mainTemplate.py.jinja')

    with open(output_file, 'w') as f:
        f.write('from maspy import *\n')
        f.write(jinja_agent_template.render(agents=agents))
        f.write(jinja_env_template.render(envs=envs))
        f.write(jinja_main_template.render(agents=agents))