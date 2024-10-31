class Truck:
    def __init__(self, truckID: int, truckCapacity=16, mileage=0.0):
        self.truckID = truckID
        self.capacity = truckCapacity
        self.packages = []
        self.status = "At Hub"
        self.mileage = mileage
    
    def getTruckID(self) -> int:
        """ Returns the truck's ID.
        
        Returns:
            (int): The ID of the truck."""
        return self.truckID
    
    def getTruckStatus(self) -> str:
        """ Returns the truck's current status.
        
        Returns:
            (str): Status of the truck. 
            Options are: 'At Hub', 'Delivering', 'Finished Delivering', 'Heading back to Hub'
        """
        return self.status

    def setTruckStatus(self, newStatus: str):
        """ Updates the Truck object's status to the input.
        
        Args:
            newStatus (str): Status of the truck.
        """
        self.status = newStatus