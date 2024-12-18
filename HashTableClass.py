from PackageClass import Package
class HashTable:
    def __init__(self, size=10):
        """ Class constructor with an optional parameter for size of the hash table.
        By default, creates a hash table of size 10, filling each bucket with an empty list.
        
        Args:
            size (int): [Optional] The size of the hash table, or number of "buckets".
        """
        self.table = []
        for i in range(size):
            self.table.append([])
    
    def findBucket(self, key: int) -> int:
        """ Helper function to perform hashing on an item's key and apply modulus to the
        length of the table. Returns an integer that defines the bucket in the table.
        
        Args:
            key (int): The specified key (package ID).
        Returns:
            val (int): The modulus of the key and the length of the hash table.
        """
        val = key % len(self.table)
        return val
    
    def addPackage(self, package: Package):
        """ This function adds package objects into the hash table. Addresses collisions
        by using chaining.
        
        Args:
            package (Package): Package to add to the hash table."""
        
        # Search for bucket list to insert into
        key = package.getID()
        bucket = self.findBucket(key)
        bucketList = self.table[bucket]
        
        # Update value if already in bucket
        for keyval in bucketList:
            if keyval[0] == key:
                keyval[1] = package
                return True
        
        # If package isn't in the bucket, append to the bucket list
        key_val = [key, package]
        bucketList.append(key_val)
        return True
    
    def searchPackage(self, key: int) -> Package | None:
        """ This function searches the hash table for a package given a key. The search performed is linear
        and has a worst-case run time of *O*(*n*), *n* being the number of elements in the hash table. 
        Returns the package if a matching key is found, otherwise returns None.
        
        Args:
            key (int): The key of a package (Package ID).
        Returns:
            Package: The package with the corresponding key, otherwise *None*.
        """
        # Locate bucket
        bucket = self.findBucket(key)
        bucketList = self.table[bucket]

        # Look for the package within this bucket's list
        for keyval in bucketList:
            if keyval[0] == key:
                return keyval[1] # The Package
        return None # If not found
    
    def getAllPackages(self) -> list[Package]:
        """ Returns a list of all existing packages in the table. Does not include the package's key.
        
        Returns:
            vals (list[Package]): List of Package objects in the table.
        """
        vals = []
        if(len(self.table) == 0):
            return vals
        else:
            for bucket in self.table:
                for keyval in bucket:
                    vals.append(keyval[1])
        return vals
    
    def removePackage(self, key: int) -> None:
        """ This function removes a package given a key (package ID).
        
        Args:
            key (int): The key to look for and remove a package from.

        Returns:
            None: None if the Package is not found within the table.
        """
        # Locate bucket
        bucket = self.findBucket(key)
        bucketList = self.table[bucket]
        
        # Remove package if exists
        for keyval in bucketList:
            if keyval[0] == key:
                bucketList.remove([keyval[0],keyval[1]])
        return None

    def showContents(self):
        """ Helper function to print out contents of the hash table in a more legible way."""
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                p = self.table[i][j][1]
                print(f"Bucket {i}: {p.toString()}")
