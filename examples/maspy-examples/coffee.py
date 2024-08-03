from maspy import Admin, Agent, gain, pl
from maspy.agent import Belief, Goal

class CoffeeMachine(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.add(Belief('has_water'))

    @pl(gain, Belief('has_water'), Belief('coffee_beans'))
    def expressoReady(self, src):
        self.print('Expresso Machine ready!')
        self.add(Goal('make_coffee'))
        self.get

    @pl(gain, Belief('filter'), Belief('has_water'))
    def machineReady(self, src):
        self.print("Black Machine Ready!")
        self.add(Goal('make_coffee'))

    @pl(gain, Goal('make_coffee'))
    def makeCoffee(self, src):
        self.print('Make coffee!')
        self.stop_cycle()

expresso = CoffeeMachine('Expresso')
black = CoffeeMachine('Black')

expresso.add(Belief('coffee_beans'))
black.add(Belief('filter'))

Admin().connect_to
Admin().start_system()