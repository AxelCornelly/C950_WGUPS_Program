import csv
from PackageClass import Package

# HashTable data structure to hold package data
packageHash = []

def hash(packageID):
    """This is a helper hash function to assist in the insertion
    of items into our hash table.
    Args:
        packageID (int): The package's ID.
    """
    return (packageID % 10)

def searchPackageHash(key):
    stuff

def addToHash(package):
    """ This is a helper function to add package objects into our hash table
    data structure. It takes in a Package object. The
    insertion of the package depends on the table key, which will be 
    Package ID.
    Args:
        package (Package): The Package object to be inserted into the hash table.
    """
    if(searchPackageHash(package.getID()) == null):
        bucket = packageHash[hash(package.getID())]
        



def readPackages(packageFile):
    """ This function reads in a csv file containing package data and appends them
    to the packageHash data structure.
    Args:
        packageFile (str): A string of the csv file name.
    """
    with open(packageFile, mode='r') as file:
        csvFile = csv.reader(file)
        next(csvFile) # Skips Header Row
        for line in csvFile:
            p = Package(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7])
            packageHash.append([p.getID(), p])


if __name__ == "__main__":
    readPackages('WGUPS Package File.csv')
    for p in packageHash:
        print(p[1].toString())
