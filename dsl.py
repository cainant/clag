from textx import metamodel_from_file
import jinja2
from os import mkdir
from os.path import exists, dirname, join

def contextType(context, agent):
    for plan in agent.plans:
        if context == plan.name:
            return f'Goal("{context}")'
    
    return f'Belief("{context}")'

agent_meta = metamodel_from_file('agentGrammar.tx')
agent_model = agent_meta.model_from_file('examples/coffee.agent')

print('Beliefs:')
for belief in agent_model.beliefs.list:
    print(belief)

print('\nDesires:')
for desire in agent_model.desires.list:
    print(desire)

print('\nPlans:')
for plan in agent_model.plans:
    print(f'{plan.name}: {plan.conditions.condition} -> ', end='')
    if hasattr(plan.actions, 'action'):
        print(plan.actions.action)
    else:
        print('No action')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dirname(__file__)),
    trim_blocks=True, lstrip_blocks=True
)
jinja_env.filters['contextType'] = contextType
jinja_template = jinja_env.get_template('agentTemplate.py.jinja')

if not exists('out'):
    mkdir('out')
with open('out/debug.py', 'w') as f:
    f.write(jinja_template.render(agent=agent_model))