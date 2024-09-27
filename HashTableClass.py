class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = []
        for i in range(size):
            self.table.append([])
            i += 1
    
    def hash(self, packageID):
        """This is a helper hash function to assist in the insertion
        of items into our hash table.
        Args:
            packageID (int): The package's ID.
        """
        return (int(packageID) % 10)

    def searchPackageHash(self, hashTable, key):
        index = hash(key)
        bucket = hashTable.table[index]
        for p in bucket:
            if p[0] == key:
                return p[1]
            else: 
                return None
        
    def addToHash(self, hashTable, package):
        """ This is a helper function to add package objects into our hash table
        data structure. It takes in a list and a Package object. The
        insertion of the package depends on the table key, which will be 
        Package ID. Utilizes chaining to handle collisions.
        Args:
            hashTable (list): The hash table list structure.
            package (Package): The Package object to be inserted into the hash table.
        """
        if(self.searchPackageHash(hashTable, package.getID()) is None):
            key = hash(package.getID())
            bucket = hashTable.table[key]
            packageNode = [package.getID(), package]
            bucket.append(packageNode)