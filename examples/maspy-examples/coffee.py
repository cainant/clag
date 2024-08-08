from maspy import *
# autogenerated
# (c) cainan - utfpr 2024
class CoffeeMachine(Agent):
    def __init__(self, name = None):
        super().__init__(name)
        self.add(Belief('HasWater'))
        self.add(Belief('HasFilter'))
        self.add(Goal('MakeCoffee'))

    @pl(gain, Belief("HasWater"), [Belief("HasCoffeeBean")])
    def ExpressoReady(self, src):
        self.add(Goal("MakeCoffee"))
        
    @pl(gain, Belief("HasCoffeeBean"))
    def BuyFilter(self, src):
        self.add(Belief("HasFilter"))
        
    @pl(gain, Belief("HasWater"), [Belief("HasFilter"), Belief("HasCoffeeBean")])
    def BlackReady(self, src):
        self.add(Goal("MakeCoffee"))
        
    @pl(gain, Goal("MakeCoffee"))
    def MakeCoffee(self, src):
        pass
        
    
# autogenerated
# (c) cainan - utfpr 2024
class CoffeeShop(Environment):
    def __init__(self, name):
        super().__init__(name)
        self.create(Percept('hasCoffee'))

    def buyCoffee(self, src):
        pass

if __name__ == '__main__':
    coffeemachine = CoffeeMachine()

    Admin().start_system()