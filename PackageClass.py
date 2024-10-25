import datetime


class Package:
    def __init__(self, packageID="-1", address="", city="", state="", zip="", deadline="", weight="", notes="", status="Undelivered"):
        """Class constructor function that defines a Package object.
        Attributes have defaults if no values are entered.

        Args:
            packageID (int): The ID of the package.
            address (str): The delivery address the package must be delivered to.
            city (str): The city where the address is located.
            state (str): The state where the address is located.
            zip (str): The zipcode of the address.
            deadline (str): The time of day that the package must be delivered by.
            weight (int): The weight of the package in kilos.
            notes (str): The additional notes that are attached to the package.
            status (str): The status of the package. Defaults to 'Undelivered'. Options include: "Undelivered", "Delayed", "On Truck", "Delivered".
        """
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.requiresTruck = False
        self.requiresPackage = False
        self.deliveredTime = None

        # Checks for any Special Notes and applies restriction
        if (self.notes != ""): # Check if there even is a note
            keywords = ["truck 2", "Delayed", "Must be delivered with"]
            for keyword in keywords:
                if (keyword in self.notes) and keyword == "truck 2": # Check for truck requirement
                    self.requiresTruck = True
                elif (keyword in self.notes) and keyword == "Delayed": # Check if delayed
                    self.status = "Delayed"
                elif (keyword in self.notes) and keyword == "Must be delivered with": # Check if needs to be with another package
                    self.requiresPackage = True
                else:
                    # Do nothing
                    print("")
    
    def toString(self) -> str:
        """ Helper function to display package information in a legible format.
        
        Returns:
            str: String value in the format of [Package ID] | Address | Deadline | Weight | Special Notes
        """
        return f"[Package {self.packageID}] | Destination: {self.address} {self.city}, {self.state} {self.zip} | Deadline: {self.deadline} | Weighs {self.weight} kilos | Special Notes: {self.notes} | Status: {self.status}"

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
    
    def getNotes(self) -> str | None:
        """ Returns any special notes attached to the package."""
        return self.notes

    def getStatus(self) -> str:
        """ Returns the delivery status of the package."""
        returnedStatus = ""
        if self.deliveredTime == None:
            returnedStatus = self.status
            return returnedStatus
        returnedStatus = f"{self.status} at {datetime.datetime.strftime(self.deliveredTime, "%H:%M %p")}"
        return returnedStatus
    
    def updateStatus(self, newStatus: str):
        """ Updates the delivery status of the package.
        
        Args:
            newStatus (str): The new status of the package (Undelivered or Delivered).
        """
        self.status = newStatus
    
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

    def setDeliveredTime(self, deliveredTime: datetime.datetime):
        self.deliveredTime = deliveredTime
    