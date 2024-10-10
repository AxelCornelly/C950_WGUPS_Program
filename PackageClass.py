class Package:
    def __init__(self, packageID: str, address: str, city:str, state: str, zip:str, deadline: str, weight: str, notes: str):
        """Class constructor function that defines a Package object.
        Args:
            packageID (int): The ID of the package.
            address (str): The delivery address the package must be delivered to.
            city (str): The city where the address is located.
            state (str): The state where the address is located.
            zip (str): The zipcode of the address.
            deadline (DateTime): The time of day that the package must be delivered by.
            weight (int): The weight of the package in kilos.
            notes (str): The additional notes that are attached to the package.
        """
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
    
    def toString(self) -> str:
        """ Helper function to display package information in a legible format.
        Returns:
            str: String value in the format of [Package ID] | Address | Deadline | Weight | Special Notes
        """
        return f"[Package {self.packageID}] | Destination: {self.address} {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weighs {self.weight} kilos | Special Notes: {self.notes}"

    def getID(self) -> int:
        """ Returns the package's ID in the form of an *int*."""
        return int(self.packageID)
    
    def getAddress(self) -> str:
        """ Returns package's destination address."""
        return self.address
    
    def getCity(self) -> str:
        """ Returns package's destination city."""
        return self.city
    
    def getState(self) -> str:
        """ Returns package's destination state."""
        return self.state
    
    def getZip(self) -> str:
        """ Returns package's destination zip code."""
        return self.zip
    
    def getDeadline(self) -> str:
        """ Returns package's delivery deadline."""
        return self.deadline
    
    def getWeight(self) -> int:
        """ Returns package's weight in kilos."""
        return int(self.weight)
    
    def getNotes(self) -> str:
        """ Returns any special notes attached to the package."""
        return self.notes
    
    def updateAddress(self, newAddress: str, newCity: str, newState: str, newZip: str):
        """ Updates the address of a package.
        Args:
            newAddress (str): Package's new destination street address.
            newCity (str): Package's new destination city.
            newState(str): Package's new destination state.
            newZip (str): Package's new destination zipcode.
        """
        self.address = newAddress
        self.city = newCity
        self.state = newState
        self.zip = newZip

    