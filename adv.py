from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.vertices = {}

    def dft(self, starting_vertex):
        visited = set()
        # create a stack and add starting_vertex
        s = Stack()
        s.push([starting_vertex])
        while s.size() > 0:
            # pop the last vertex that was added
            curr_node = s.pop()
            room = curr_node[-1]

            # next we need to see if room has been visited
            if room not in visited:
                # set vertices based  on id of room
                self.vertices[room.id] = {}
                # add connected room and direction
                for potential_dir in room.get_exits():
                    self.vertices[room.id][room.get_room_in_direction(
                        potential_dir).id] = potential_dir
                # mark this room as visited
                visited.add(room)

                exit_options = room.get_exits()
                while len(exit_options) > 0:
                    room_direction = exit_options[0]
                    # create neighbor path
                    neighbor_path = list(curr_node)
                    neighbor_path.append(
                        room.get_room_in_direction(room_direction))
                    # add to stack
                    s.push(neighbor_path)
                    # remove to go to next direction option
                    exit_options.remove(room_direction)
        return self.vertices

    def bfs(self, starting_vertex, destination_vertex):
        q = Queue()
        q.enqueue([starting_vertex])
        visited = set()
        while q.size() > 0:
            curr_path = q.dequeue()
            last_vert = curr_path[-1]
            if last_vert not in visited:
                if last_vert == destination_vertex:
                    return curr_path
                visited.add(last_vert)
                for room_id in self.vertices[last_vert].keys():
                    path_of_neighbors = list(curr_path)
                    path_of_neighbors.append(room_id)
                    q.enqueue(path_of_neighbors)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

graph = Graph()
# use DFT function to create a graphed map of the 'world'
rooms_dft = graph.dft(player.current_room)
# Extract all room id's into a list
rooms_list_dft = [id for id in rooms_dft.keys()]


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

while(len(rooms_list_dft) > 1):
    # set current position
    curr_room = rooms_list_dft[0]
    next_room = rooms_list_dft[1]
    curr_room_neighbors = rooms_dft[curr_room]
    # if they are a neighbor, add to path
    if next_room in curr_room_neighbors.keys():
        traversal_path.append(curr_room_neighbors[next_room])
    else:
        # if they're not a neighbor, then we need to use BFS to find shortest path
        shortest_path = graph.bfs(curr_room, next_room)
        while len(shortest_path) > 1:
            curr_room_neighbors = rooms_dft[shortest_path[0]]
            next_room = shortest_path[1]
            # if they are neighbor, add to traversal_path
            if next_room in curr_room_neighbors.keys():
                traversal_path.append(curr_room_neighbors[next_room])
            else:
                traversal_path.append('?')
            shortest_path.pop(0)
    rooms_list_dft.pop(0)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# ######
# UNCOMMENT TO WALK AROUND
# ######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")