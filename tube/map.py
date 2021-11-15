import json

from tube.components import Station, Line, Connection

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json" method (don't hesitate to divide your code into several sub-methods, if needed)

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id (key=id, value=Station)
    - lines: a dictionary that indexes Line instances by their id (key=id, value=Line)
    - connections: a list of Connection instances for the tube map (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id, value: Station
        self.lines = {}  # key: id, value: Line
        self.connections = []  # list of Connections

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During that import, the `stations`, `lines` and `connections` attributes should be updated.

        You can use the `json` python package to easily load the JSON file at `filepath`

        Note: when the indicated zone is not an integer (for instance: 2.5), 
            it means that the station is in two zones at the same time. 
            For example, if the zone of a station is "2.5", 
            it means that station is in zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to import

        Returns:
            None

        Note:
            If the filepath is invalid, no attribute should be updated, and no error should be raised.
        """
        #Check if filename is invalid
        try:
            with open(filepath, "r") as jsonfile: 
                data = json.load(jsonfile)
        except FileNotFoundError:
            print("Invalid filename")
            return
        connections = data["connections"]
        #Create dictionary of stations that indexes Station instances by their id
        for station in data["stations"]:       
            id = station["id"]
             #Check if the set zone is integer. If non-integer, then create a new set of 2 integers
            if not float(station["zone"]).is_integer():
                if float(station["zone"]) < round(float(station["zone"]), 0):
                    zones = {int(round(float(station["zone"]), 0) - 1), int(round(float(station["zone"]), 0))}
                elif float(station["zone"]) > round(float(station["zone"]), 0):
                    zones = {int(round(float(station["zone"]), 0)), int(round(float(station["zone"]), 0) + 1)}
            else:
                zones = {station["zone"]}      
            #create instances of Station and update the stations dictionary accordingly
            new_station = Station(id, station["name"], zones)
            self.stations.update({new_station.id : new_station})
           #Create instances of Line and update the lines dictionary accordingly
        for line in data["lines"]:
            new_line = Line(line["line"], line["name"])  
            self.lines.update({new_line.id : new_line})
            #Get connected stations by getting the station ids from connections 
        for connection in data["connections"]:
            station1 = self.stations[connection["station1"]]           
            station2 = self.stations[connection["station2"]]
            line = self.lines[connection["line"]]
            #Create connection instances and update connections list
            new_connection = Connection({station1, station2}, line, int(connection["time"]))
            self.connections.append(new_connection)
        return 


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
