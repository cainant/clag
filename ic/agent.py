class NAGAgent:
    def __init__(self, parent, name, beliefs, desires, plans) -> None:
        self.name = name
        self.beliefs = beliefs
        self.desires = desires
        self.plans = plans

    @staticmethod
    def context_type_to_str(context, agent):
        # check if context is a belief or a goal
        if context in agent.desires:
            return f'Goal("{context}")'
        
        return f'Belief("{context}")'