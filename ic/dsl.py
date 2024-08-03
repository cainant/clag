from textx import metamodel_from_file
import jinja2
from os import mkdir
from os.path import exists, dirname

def contextType(context, agent):
    for plan in agent.plans:
        if context == plan.name:
            return f'Goal("{context}")'
    
    return f'Belief("{context}")'

def main():
    system_meta = metamodel_from_file('grammar/system.tx')
    system_model = system_meta.model_from_file('../examples/coffee.maspy')

    agents = system_model.agents
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

    envs = system_model.envs
    for env in envs:
        print('\n---------------------------')
        print(f'Environment: {env.name}')
        print('Perceptions:')
        for perception in env.perceptions.list:
            print(perception)

        print('\nActions:')
        for action in env.actions.list:
            print(action)
            
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(dirname(__file__)),
        trim_blocks=True, lstrip_blocks=True
    )
    jinja_env.filters['contextType'] = contextType
    jinja_agent_template = jinja_env.get_template('templates/agentTemplate.py.jinja')
    jinja_env_template = jinja_env.get_template('templates/envTemplate.py.jinja')
    #jinja_main_template = jinja_env.get_template('templates/mainTemplate.py.jinja')

    if not exists('../out'):
        mkdir('../out')
    with open('../out/debug.py', 'w') as f:
        f.write('from maspy import *\n')
        f.write(jinja_agent_template.render(agents=agents))
        f.write(jinja_env_template.render(envs=envs))
        #f.write(jinja_main_template.render())