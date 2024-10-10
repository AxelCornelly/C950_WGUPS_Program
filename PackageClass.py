class Package:
    def __init__(self, packageID, address, city, state, zip, deadline, weight, notes):
        """Class constructor function that defines a Package object
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
    
    def toString(self):
        return f"[Package {self.packageID}] | Destination: {self.address} {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weighs {self.weight} kilos | Special Notes: {self.notes}"

    def getID(self):
        return int(self.packageID)
    
    def getAddress(self):
        return self.address
    
    def getCity(self):
        return self.city
    
    def getState(self):
        return self.state
    
    def getZip(self):
        return self.zip
    
    def getDeadline(self):
        return self.deadline
    
    def getWeight(self):
        return self.weight
    
    def getNotes(self):
        return self.notes
    
    def updateAddress(self, newAddress, newCity, newState, newZip):
        self.address = newAddress
        self.city = newCity
        self.state = newState
        self.zip = newZip

    