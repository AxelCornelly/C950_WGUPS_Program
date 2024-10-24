class Truck:
    def __init__(self, truckID, truckCapacity=16):
        self.truckID = truckID
        self.capacity = truckCapacity
        self.packages = []
        self.status = "At Hub"
    
    def getTruckID(self) -> int:
        """ Returns the truck's ID.
        
        Returns:
            (int): The ID of the truck."""
        return self.truckID
    
    def getTruckStatus(self) -> str:
        """ Returns the truck's current status.
        
        Returns:
            (str): Status of the truck. 
            Options are: 'At Hub', 'Delivering', 'Finished Delivering'
        """
        return self.status