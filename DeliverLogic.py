import datetime
import time

def deliverPackages(trucks, startTruck, startTime, packageHashTable):
    """ Initiates the delivery of packages for a given truck.
    
    Args:
        trucks (list(Truck)): A list of all Truck objects.
        startTruck (Truck): The starting Truck object to start delivering.
        startTime (str): A string of the starting delivery time (08:00am).
        packageHashTable (HashTable): HashTable object of packages.
    """
    timer = 0
    totalTravelDist = 0.0 # In miles
    start_Time = datetime.datetime.strptime(startTime, "%H:%M:%S").time()

    while timer < 20000:
        timer += 1
        # Set speed of the program
        time.sleep(0.1)

        # Continuously update current time while program runs, incrementing minutes
        currentTime = datetime.datetime.combine(datetime.date.today(), start_Time) + datetime.timedelta(minutes=timer)
        
        # When delayed packages arrive at 09:05 am, update statuses
        if currentTime.hour == 9 and currentTime.minute == 5:
            for p in trucks[2].packages:
                if p.getStatus() == "Delayed":
                    p.updateStatus("On Truck")
        
        # When 10:20am hits, update Package 9's address
        if currentTime.hour == 10 and currentTime.minute == 20:
            for p in trucks[2].packages:
                if p.getID() == 9:
                    p.updateAddress("410 S State St", "Salt Lake City", "UT", "84111")
        
        # Truck Delivery Process

        # Logic for Truck 1 and 2
        if startTruck.getTruckID() != 3:
            if startTruck.getTruckStatus() != "Finished Delivering" or startTruck.getTruckStatus() != "Delivering":
                # Find next nearest package and deliver it from current location
                
        
        # Logic for Truck 3 to start delivering
        if startTruck.getTruckStatus() ==
        