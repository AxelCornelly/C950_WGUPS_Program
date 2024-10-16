from PackageClass import Package
from HashTableClass import HashTable

class Truck:
    def __init__(self):
        self.packages = []
    
    def loadPackages(self, packages: HashTable):
        """ Loads a maximum of 16 packages on to the truck. Performs checks to
        satisfy program assumptions such as:
        Max num of packages = 16
        Loading time is instant
        Complies with any and all Special Notes on packages
        
        Args:
            packages (HashTable): The HashTable object of packages to load from.
        """
        for bucket in packages.table: # [[Bucket0], [Bucket1], [Bucket2], [Bucket3], ...]
            for items in bucket: # [[Package ID, Package], [Package ID, Package], ...]
                currPackage = items[1]
                # Perform checks here
                