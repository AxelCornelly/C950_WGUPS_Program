class Truck:
    def __init__(self, truckID):
        self.truckID = truckID
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
            Options are: 'At Hub', 'Delivering'
        """
        return self.status