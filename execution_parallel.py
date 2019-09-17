import time
import logging
import requests
from shapely.geometry import Point,shape, mapping
from shapely.ops import unary_union
import fiona
from fiona import collection
 
# datasets (Turn this into a function)
accidents = fiona.open('C:\\Users\\Coleman.Shepard.ctr\\DOT\\Work Zone Data Exchange\\WorkZoneData\\Code\\Proof_of_Concept\\HPMS\\ggez.shp', 'r')
roadway = fiona.open('C:\\Users\\Coleman.Shepard.ctr\\DOT\\Work Zone Data Exchange\\WorkZoneData\\Code\\Proof_of_Concept\\Alabama_Count.shp', 'r')




def process_road(road):
    # There are some records with a NoneType for geometry, but this can be passed over
    if road['geometry'] != None:

        # Buffers geometry
        geom = shape(road['geometry']).buffer(0.001)

        # Loops through every accident
        for accident in accidents:
            lat = accident['geometry']['coordinates'][1]
            lon = accident['geometry']['coordinates'][0]
            bounds = roadway.bounds

            # filter based on bounding box of roads
            if lat > bounds[1] and lat < bounds[3]:
                if lon > bounds[0] and lon < bounds[2]:
                    # Shapely contains to see if accidents fall within the buffer
                    if geom.contains(shape(accident['geometry'])) == True:
                        road['properties']['Count'] += 1

        return road


# Change this function to another one and give main a new standalone function
def main():

    # Move these up
    import time
    import socket
    import multiprocessing

    # Make sure the function is using all the cores.
    NUM_WORKERS = multiprocessing.cpu_count()
    
    start_time = time.time()
    
    with multiprocessing.Pool(processes=NUM_WORKERS) as pool:
        # Results 
        results = pool.map(process_road, roadway)
        a = 0

        # Make an argument to choose the file name that pulls the date and time
        with fiona.open('Intersected_Roads_09162019_430pm.shp', 'w', driver='ESRI Shapefile', schema=roadway.schema) as output:
            for i in results:
                try:
                    if i['properties']['Count'] >= 1:
                        a+=1
                        # write to the File
                        output.write(i)
                except:
                    print('Nah')

                

    print('Count of Roads with more than Incident', a)
    end_time = time.time()        
    
    print("Time for MultiProcessingSquirrel: %ssecs" % (end_time - start_time))
   


# Line needed for multiprocessing in Windows.
if __name__ == "__main__":
    main()