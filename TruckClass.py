class Truck:
    def __init__(self, truckName):
        self.truckName = truckName
        self.packages = []
    
    def getTruckName(self) -> str:
        """ Returns the name of the truck.
        
        Returns:
            (str): The name of the truck."""
        return self.truckName