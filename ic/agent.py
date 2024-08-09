import click


_belief_ctx_types = ['acreditar', 'desacreditar', 'acredita']
_goal_ctx_types = ['cumprir']

class NAGAgent:
    def __init__(self, parent, name, beliefs, desires, plans) -> None:
        self.name = name
        self.beliefs = beliefs
        self.desires = desires
        self.plans = plans

    @staticmethod
    def context_type_to_str(context, contextType):
        if contextType in _belief_ctx_types:
            return f'Belief("{context.name}")'
        if contextType in _goal_ctx_types:
            return f'Goal("{context.name}")'
        
        click.echo(f'[ERROR] Invalid operation: {contextType} {context.name}')
        exit()
        