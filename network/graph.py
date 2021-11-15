class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def build(self, tubemap):
        # key: id, value: Station
        # key: id, value: Line
        # list of Connections
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building the graph.

        Return:
            graph (dict) : as described above.

        Note:
            If the input data (tubemap) is invalid, the method should return an empty dict.
        """
        graph = {}        
        try:
            #Get each station instance
            for station_id in tubemap.stations:                
                parent_station = tubemap.stations[station_id]
                connection_list = []
                #Check if the station in each connection instance is the same as the stationin the station instance indexed by its id
                #Then create a list of these connections
                for connection in tubemap.connections:
                    #Iterate #through all connections that exist in the parent_station and find them
                    if parent_station in connection.stations: #through all connections that exist and find all
                        #Append all connections to the parent station
                        connection_list.append(connection)
                neighbour_dict = {}
                #For each connection to the entering parent station get its neighbouring station subtracting the parent station wherever it appears
                for connection in connection_list:                    
                    neighbour = list(connection.stations - {parent_station})   
                    #If neighbour exists it returns a none empty existing_connection variable
                    existing_connection = neighbour_dict.setdefault(neighbour[0].id, [connection])
                    if existing_connection != [connection]:
                        existing_connection.append(connection)
                        neighbour_dict.update({neighbour[0].id: existing_connection})
                graph.update({station_id: neighbour_dict})
            return graph    


        except FileNotFoundError:            
            print("Invalid filename")          
            return {}



        return dict()  


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph)


if __name__ == "__main__":
    test_graph()
