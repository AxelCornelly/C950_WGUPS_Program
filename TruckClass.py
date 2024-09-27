class Truck:
    def __init__(self):
        self.packages = []
    
    def loadPackage(self, package):
        self.packages.append(package)