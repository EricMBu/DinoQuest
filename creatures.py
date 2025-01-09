class Dinosaur:
    def __init__(self, species, level):
        self.species = species
        self.level = level
    
    def GetLevel(self):
        return self.level
    
    def GetSpecies(self):
        return self.species