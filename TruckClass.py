class Truck:
    def __init__(self, truckID):
        self.truckID = truckID
        self.packages = []
    
    def getTruckID(self) -> int:
        """ Returns the truck's ID.
        
        Returns:
            (int): The ID of the truck."""
        return self.truckID