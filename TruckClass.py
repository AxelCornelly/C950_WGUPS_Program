from PackageClass import Package
class Truck:
    def __init__(self):
        self.packages = []
    
    def loadPackage(self, package: Package):
        self.packages.append(package)