"""
WARNING: the following classes should remain unchanged!
"""

class Station:
    def __init__(self, id, name, zones):
        """ A class representing a Tube station.
        
        Args:
            id (str) : Station ID
            name (str) : Station name
            zones (Set[int]) : Set of zone numbers for station
        """
        self.id = id
        self.name = name
        self.zones = zones

    def __repr__(self):
        return f"Station({self.id}, {self.name}, {self.zones})"


class Line:
    def __init__(self, id, name):
        """ A class representing a Tube line.
        
        Args:
            id (str) : Line ID
            name (str) : Line name
        """
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Line({self.id}, {self.name})"


class Connection:
    def __init__(self, stations, line, time):
        """ A connection between two stations on a specific Tube line.
        
        Args:
            stations (Set[Station]) : stations associated with the connection
            line (Line) : the line for the connection
            time (int) : time needed (in minutes) to transit between the stations
        """
        self.stations = stations
        self.line = line
        self.time = time

    def __repr__(self):
        station_names = [station.name for station in self.stations]
        return f"Connection({'<->'.join(station_names)}, {self.line.name}, {self.time})"


if __name__ == '__main__':
    # Some examples of Station, Line and Connection
    station_1 = Station(id="131",
                        name="Some Station Name",
                        zones={1, 2})

    station_2 = Station(id="42",
                        name="Some Other Station Name",
                        zones={3})

    line = Line(id="2",
                name="Line Name")

    connection = Connection(stations={station_1, station_2},
                            line=line,
                            time=4)
