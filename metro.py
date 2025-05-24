import csv  # In order to read from the "processed_stations.csv".


# The Station class will take the role of the vertex.
class Station:
    def __init__(self, key):
        self.key = key
        self.data = None  # Can be later populated with data.
        self.edges = []  # An empty list of edges.
        self.parent = None  # We will need this for BFS.
        self.color = 'white'  # Initially every vertex will be white.
        # Initially the distance of vertices will be infinite.
        self.distance = float("inf")


# Line will signifie the lines/edges of the metro.
class Line:
    # When we create an edge we will pass a vertex that we want to connect it to.
    def __init__(self, vertex):
        self.connection = vertex  # A link to another vertex.


class Metro:
    def __init__(self):
        self.vertices = {}  # Initially, an empty dict.
        self.directed = False  # Default graph is undirected!
        # We will need this empty list to act as a queue for our BFS.
        self.queue = []
        self.start = None

    # Initialize BFS by making every parent none, 
    # distance to infinite and colors to white.
    def init_bfs(self):
        for key in self.vertices:
            v = self.vertices[key]
            v.parent = None
            v.distance = float("inf")
            v.color = "white"

    def bfs(self, start):  # Start will be the key.
        self.init_bfs()
        if start not in self.vertices:
            return False
        # V becomes `self.vertices` at position start.
        v = self.vertices[start]
        # Make distance 0.
        v.distance = 0
        # Make the color grey.
        v.color = "grey"
        # Append V into the Queue.
        self.queue.append(v)
        # While the Queue is not empty:
        while len(self.queue) > 0:
            # Pick V from the Queue.
            v = self.queue.pop(0)  # Get the 1st one:)
            # Make V black.
            v.color = "black"
            # For each white edge of V.
            for e in v.edges:
                con = e.connection  # The remote vertex.
                # Make it grey.
                if con.color == "white":
                    con.color = "grey"
                    # Update distance to V.dist + 1.
                    con.distance = v.distance + 1
                    # Update parent to V.
                    con.parent = v
                    # Put in the Queue.
                    self.queue.append(con)
        return True

    def bfs_shortest_path(self, dest):  # We give destination as a number.
        if dest in self.vertices:  # If the vertex exists in vertices.
            v = self.vertices[dest]  # V becomes self.vertices[at dest]
            if v.parent is None:
                # This path covers isolated islands. Vertices that are isolated 
                # from the rest.
                print("No path from", v.data)
                return False
            self.print_path(v)  # Call recursion, to print the path.
            print()
            return True
        else:
            return False

    def print_path(self, vertex):  # Recursive function.
        if vertex.parent is not None:  # As long as the parent is not None.
            # Do it again and again until we hit a base case.
            # When we hit a base case every other function 
            # that is waiting prints so we get the result.
            self.print_path(vertex.parent)
            print(" -> ", end="")
        print(vertex.data, end=".")

    # Add vertices function.
    def add(self, key):
        # Would be cool if people did not forget.
        # If we try to put duplicate keys.
        if key in self.vertices:
            return None
        # Otherwise, construct a new Vertex(key) with our key, named `new_vertex`
        # Also the key that we input DOES MORE.
        # It goes to `self.vertices[key]` and POINTS to the `new_vertex`.
        else:
            new_vertex = Station(key)
            self.vertices[key] = new_vertex
            return new_vertex

    # We give it 2 KEYS.. To connect them. Ok?
    def connect(self, key_a, key_b):
        # DID SOMEONE FORGET AGAIN?
        if key_a not in self.vertices or key_b not in self.vertices:
            return False, "Key not found, DUFUS"
        else:
            # We already have the vertices ready to MEDDLE THEM.
            # Vertex_a is at [key_a] -- Vertex_b is at [key_b].
            vertex_a = self.vertices[key_a]
            vertex_b = self.vertices[key_b]
            # Create an edge that refers to key_b.
            edge = Line(vertex_b)
            # Append it to key_a connections.
            vertex_a.edges.append(edge)
            if self.directed is False:  # If it is undirected the if clase also is fired.
                edge = Line(vertex_a)  # And the exact opposite also happens.
                vertex_b.edges.append(edge)
            return True, "Vertices are now connected."


def load_stations_from_csv(graph, filename):
    line_groups = {}  # Dict to group the stations of the metro.
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Open the CSV file.
        for row in reader:  # ieterated over each row.
            code = row['code']  # Unique code of the metro station.
            name = row['name']  # Station name of metro.
            line = row['line']  # Line of said station.
            num = int(row['num'])  # The position of the station on the line.

            # Here we add the station to the graph as a vertex(code as key).
            vertex = graph.add(code)
            if vertex:  # We store the name inside the data field of the Vertex.
                vertex.data = name

            # Here we add the station to the list of stations for its specific line.
            if line not in line_groups:
                line_groups[line] = []
            line_groups[line].append((num, code))

    # Adjacent stations on the same line need to be connected.
    for stations in line_groups.values():
        stations.sort()  # Sort them by  their number.
        # Connect the station (i) to the next one (i+1).
        for i in range(len(stations) - 1):
            graph.connect(stations[i][1], stations[i + 1][1])

    # Here we construct a dictionary to have a map with the names and codes.
    name_to_codes = {}
    for code, vertex in graph.vertices.items():
        name = vertex.data
        if name not in name_to_codes:
            name_to_codes[name] = []
        name_to_codes[name].append(code)

    # Lastly, we connect the codes for station sthat are sharing the same name.
    # This is done in order for the different lines to be connected at the interchanges.
    for codes in name_to_codes.values():
        if len(codes) > 1:
            for i in range(len(codes)):
                for j in range(i + 1, len(codes)):
                    graph.connect(codes[i], codes[j])


if __name__ == "__main__":
    # Create a new graph of the metro system.
    metro = Metro()
    # Put the stations into the graph from the file.
    load_stations_from_csv(
        metro, "C:/Users/kyass/OneDrive - New York College/Data Structures and Algorithms/Structures - Algorithms Workspace/Graphs/processed_stations.csv")

    # Start a BFS at station "NS10".
    metro.bfs("NS10")
    # Find the shortest path from "NS10" to "CC17" - includes line change.
    metro.bfs_shortest_path("CC17")
