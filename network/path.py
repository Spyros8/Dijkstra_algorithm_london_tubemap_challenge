from network.graph import NeighbourGraphBuilder
from math import inf


class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__ method (if needed)
    - completing the "get_shortest_path" method (don't hesitate to divide your code into several sub-methods)
    """


    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        


    def Dijkstra_algorithm(self, graph, start_station):
        """ Find ONE shortest path (in terms of duration) from start_station_name to end_station_name.

        If start_station_name or end_station_name does not exist, return None.

        You can use the Dijkstra algorithm to find the shortest path from start_station_name to end_station_name.

        See here for more information: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station 'str': name of the starting station
            graph {dict}: a dictionary of of all stations indexed by their id and their connections

        Returns:
            distances [list] : list of station distances in form [[1, 10000], [1, 10000]] where column 1 is station ids and column 2 their distances [time]
            previous_station [list] : list of the previous stations to the current station

        """
        #Define variables to use in Dijkstra algorithm
        unvisited_stations = set()
        distances = []
        previous_station = []  

        #intitialisation loop to set all distances to a very large number according to Dijkstra algorithm
        for station in graph:
            unvisited_stations.add(station)  
            distance = 100000000
            distances.append([station, distance])

        #set the distance of the starting station to zero
        for distance in distances:
            if  self.tubemap.stations[distance[0]].name == start_station: 
                distance[1] = 0
        # Need this while loop here. keeps visiting stations until all stations are visited
        while len(unvisited_stations) > 0:
            #Get the index of the station with the minimum distance to the previous station that has been visited 
            u = self.get_minimum__distance_to_unvisited_stations(distances, unvisited_stations) 
            #Remove this from the unvisited stations set
            unvisited_stations.remove(u)
            #Get the dictionary of neighbours that have not yet been visited
            neighbours = self.get_neighbours_still_in_Q(u, unvisited_stations)

            #For each unvisited neighbour and its distance
            for neighbour in neighbours:
                for distance in distances:
                    #If the distance is that of a visited station set it to its distance 
                    if distance[0] == u:
                        distance_of_u = distance[1]  
                    #If not set it to the distance of its neighbour
                    if distance[0] == neighbour:
                        distance_of_neighbour = distance[1]  
                #calculate the distance of the visited station to its neighbour
                distance_of_u_to_neighbour = self.get_distance(u, neighbour)
                #alternate distance = new distance of neighbour, equivalent to (distance_of_u + distance_of_u_to_neighbour)
                alternate_distance = distance_of_u_to_neighbour + distance_of_u
                #As in Dijkstra algorithm, update the distance to the neighbour of the previous station
                if alternate_distance < distance_of_neighbour:
                    #index returns a list index. Instead of looping through the list, you automatically find the index of what you are looking for
                    distances_list_index = distances.index([neighbour, distance_of_neighbour])  
                    distances[distances_list_index][1] = alternate_distance
                    if len(previous_station) > 0 :
                        start_stations = [v[1] for v in previous_station[:][0]]
                        if neighbour in start_stations:
                            index = start_stations.index(neighbour)
                            previous_station[index][1] = u
                        else:
                            previous_station.append([neighbour, u])
                    else:
                        previous_station.append([neighbour, u])
        return distances, previous_station

   

    def get_distance(self, u, neighbour):
        """ Get the distance of the current station to its neighbour.

        Args:
            u (int): Current station
            neighbour {dict}: a dictionary of of all neighbour stations to current station

        Returns:
            min_distance (int) : The minimum distance of current station to its neighbours

        """
        connections = self.graph[u][neighbour]
        #Set min_distance to large number so that it always gets the smaller one as in Dijkstra algorithm
        min_distance = 100000000
        for connection in connections:
            if connection.time < min_distance:
                min_distance = connection.time          
        return min_distance  



    def get_neighbours_still_in_Q(self, station, unvisited_stations):
        """ Get the neighbours that have not been visited yet.

        Args:
            station (int): Current station
            unvisited stations {set}: Set of unvisited stations to current station

        Returns:
            min_distance (int) : The minimum distance of current station to its neighbours

        """
        neighbours = self.graph[station]
        output_neighbours = {}
        for neighbour in neighbours:
            if neighbour in unvisited_stations:
                output_neighbours.update({neighbour: neighbours[neighbour]})   
        return output_neighbours



    def get_minimum__distance_to_unvisited_stations(self, distances, unvisited_stations):  
        """ Get the id of the stations with the minimum distance that has not been visited yet .

        Args:
            distances [list]: List of the ids of the stations and their distances
            unvisited stations {set}: Set of unvisited stations that match the ids in the distances list

        Returns:
            distance[0] (int) : The id of the station with the minimum distance from the previous station to the unvisited stations

        """
        # The sort() method sorts based on the first value of a list.
        # My distances list was [[key1, distance1]
        #                          [key2, distance2]
        #                          ....
        #                                           ]
        # so when I used sort(), I sorted the keys instead of the distances.
        # I switched it to [[distance, key]] so now it sorts the distances
        # Also removed the .items() after turning distances to a list
        distances_list = []
        for [key, val] in distances:
            distances_list.append([val, key])
        distances_list.sort() 
        for distance in distances_list:
            if distance[1] in unvisited_stations:
                return distance[1]  



    def get_previous_station(self, input_station, previous_station): 
        """ Get the id of the previous station to the current station.

        Args:
            input_station (str): The name of the previous station starting from the end destination
            previous_station [list]: List of previous stations from the end station stated

        Returns:
            stations[1] (int) : The id of the previous station to be appended in the path desired in the get_shortest_path function

        """
        for stations in previous_station:
            if stations[0] == input_station:
                return stations[1]  

     

    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path (in terms of duration) from start_station_name to end_station_name.

        For instance, get_shortest_path('Stockwell', 'South Kensington') should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.

        You can use the Dijkstra algorithm to find the shortest path from start_station_name to end_station_name.

        See here for more information: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not exist.
        """
        #Get the distances and previous stations from applying the Dijkstra algorithm
        distances, previous_stations = self.Dijkstra_algorithm(self.graph, start_station_name)
        # Given station names. Need to convert those names to ids
        for station_id in self.tubemap.stations:
            if self.tubemap.stations[station_id].name == start_station_name:
                start_station_id = self.tubemap.stations[station_id].id
            if self.tubemap.stations[station_id].name == end_station_name:
                end_station_id = self.tubemap.stations[station_id].id
        # Now set station as end station id
        station = end_station_id
        id_path = []
        #While loop to iterate backwards from end station and add it to the list of shortest id_path
        while station != start_station_id:
            station = self.get_previous_station(station, previous_stations)
            id_path.append(station)
        id_path.reverse()
        id_path.append(end_station_id)
        #Convert the station id path to station name path
        station_path = []
        for id in id_path:
            station = self.tubemap.stations[id]
            station_path.append(station)
        #return list of stations from start to finish with the minimum distance
        return station_path  



def test_shortest_path():
    from solution.tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)

    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
