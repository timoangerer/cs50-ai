import heapq
#############################################
# Here's the set of actions. They have the following meaning:
# - plug_in_toaster will connect the toaster to the socket, if it isn't already connected
# - unplug_toaster will disconnect the toaster from the socket.
#        If toaster is on, it switches to off automatically.
# - put_in_bread will move the bread from plate to toaster. 
#        This is only possible if the toaster is switched off.
# - take_out_brad will move the bread from toaster to plate. 
#        This is only possible if the toaster is switched off.
# - switch_on_toaster will switch the toaster on, if it is not on already.
# - wait will wait for a while. 
#       If the toaster is switched on, it will switch off.
#       If the toaster is switched on and contains bread, the bread will be toasted afterwards
#
# Each action will take one time unit to execute. Except for wait. That takes 10 time units
##############################################
actions=(
    "plug_in_toaster",
    "unplug_toaster",
    "put_in_bread",
    "take_out_bread",
    "switch_on_toaster",
    "wait"
)

##############################################
# Heres the model of the state. 
# It contains two variables that describe the toaster:
# - toaster_has_power: indicates whether the toaster is connected to the socket
# - toaster_is_on: Indicates whether the toaster is currently on or off
# It contains two variables that describe the bread:
# - bread_location: whether the bread is currently on the plate or in the toaster
# - bread_state: untoasted or toasted?
# In addition, we have one variable time which measures how long the process takes. This is an additional quality measure, as we may want to toast the bread in as little time as possible. 
#
# note that this is just an example of one start state. We will test your function with different start states.
##############################################
state={
    "toaster_has_power":False,
    "toaster_is_on":False,
    "bread_location":"plate",
    "bread_state":"untoasted",
    "time":0
    }

##############################################
# This function implements the goal.
# The toasting process is considered successfull, if the bread is on the plate and toasted.
##############################################
def goal(state):
    return state["bread_location"] == "plate" and state["bread_state"] == "toasted"

##############################################
# The state transition function. 
# It implements the meaning of actions, as described for the action variable.
##############################################
def state_transition(state, action):
    newState = state.copy()
    if action =="plug_in_toaster":
        # toaster now has power
        newState["toaster_has_power"] = True
        newState["time"] += 1
    elif action =="unplug_toaster":
        # unpower toaster and stop toasting process
        newState["toaster_has_power"] = False
        newState["toaster_is_on"] = False
        newState["time"] += 1
    elif action == "put_in_bread":
        # move bread into toaster. Only possible if toaster is not on (casue it locks)
        if not newState["toaster_is_on"]:
            newState["bread_location"] = "toaster"
        newState["time"] += 1
    elif action == "take_out_bread":
        # move bread from toaster to plate. Only possible if toaster is not on (casue it locks)
        if not newState["toaster_is_on"]:
            newState["bread_location"]="plate"
        newState["time"] += 1
    elif action == "switch_on_toaster": 
        # switch on the toaster
        if(newState["toaster_has_power"]):
            newState["toaster_is_on"]=True
        newState["time"] += 1
    elif action == "wait":
        # wait for ten steps
        newState["time"] += 10
        # if toaster is on, it is switched off, if bread was in toaster, it is toasted now.
        if newState["toaster_is_on"]:
            if newState["bread_location"] == "toaster":
                newState["bread_state"] = "toasted"
            else:
                pass
                #print(newState["bread_location"])
            newState["toaster_is_on"] = False
    return newState

####################################################
# This is the function you should be implementing for this exercise.
# The function gets a start state as input and should output a python list of actions that fulfill the goal
# I recommend implementing it the three following ways (with rising difficulty:)
# 1) Implement breadth first search first.
# 2) Implement a function that also optimizes the final value of the parameter "time"
# 3) Implement a function that fulfills 2) and is as fast as possible!
###################################################

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    def __lt__(self, nxt): 
        return self.state["time"] < nxt.state["time"] 

    def __str__(self):
        return f"Node(state: {self.state}, parent: {self.parent}, action: {self.action})\n"


def plan(algorithm, start_state):
    if algorithm == 0:
        return bfs(start_state)
    if algorithm == 1:
        return a_star(start_state)
    elif algorithm == 2:
        return oone(start_state)
    elif algorithm == 3:
        return greedy_dfs(start_state)
    elif algorithm == 4:
        return greedy_dfs_none_stop(start_state)

# Algorithms
def bfs(start_state):
    # this is an example output that will fulfill the first test, but no others.
    # Substitute this by your planning result
    # return ["plug_in_toaster","put_in_bread","switch_on_toaster","wait","take_out_bread"]

    frontier = []
    checked = []

    frontier.append(Node(start_state, None, None))

    while len(frontier) > 0:
        node = frontier.pop(0)
        checked.append(node)
        state = node.state

        if goal(state):
            break
        else:
            neighbors = [Node(state_transition(state, action), node, action) for action in actions]
            checked_states = [node.state for node in checked]
            frontier_states = [node.state for node in frontier]
            filtered_neighbors = list(filter(lambda node: node.state not in checked_states and node.state not in frontier_states, neighbors))
            frontier.extend(filtered_neighbors)

    seq = []
    currentNode = checked.pop()
    while True:
        if not currentNode:
            break
        else:
            if currentNode.action:
                seq.append(currentNode.action)
                currentNode = currentNode.parent
            else:
                break

    seq.reverse()
    return seq

def a_star(start_state):
    # TODO in progress
    frontier = []
    checked = []

    frontier.append((0, Node(start_state, None, None)))

    while len(frontier) > 0:
        node_with_steps = pick_best_node(frontier)
        
        steps = node_with_steps[0]
        node = node_with_steps[1]

        checked.append(node)
        state = node.state

        if goal(state):
            break
        else:
            neighbors = [Node(state_transition(state, action), node, action) for action in actions]
            neighbors_with_steps_count = [(steps + 1, n) for n in neighbors]

            frontier.extend(neighbors_with_steps_count)
            
    seq = []
    currentNode = checked.pop()
    while True:
        if not currentNode:
            break
        else:
            if currentNode.action:
                seq.append(currentNode.action)
                currentNode = currentNode.parent
            else:
                break

    seq.reverse()
    return seq

def oone(start_state):
    seq = []
    if start_state["toaster_is_on"] and start_state["toaster_has_power"]:
        seq.append("unplug_toaster")
        seq.append("plug_in_toaster")
    elif start_state["toaster_is_on"] and not start_state["toaster_has_power"]:
        seq.append("plug_in_toaster")
        seq.append("unplug_toaster")
        seq.append("plug_in_toaster")

    if not start_state["toaster_has_power"]:
        seq.append("plug_in_toaster")
        
    
    if start_state["bread_location"] == "plate":
        seq.append("put_in_bread")
    
    seq.append("switch_on_toaster")
    seq.append("wait")
    seq.append("take_out_bread")

    return seq

def greedy_dfs(start_state):
    frontier = []
    checked = []

    frontier.append(Node(start_state, None, None))

    while len(frontier) > 0:
        node = frontier.pop()
        checked.append(node)
        state = node.state

        if goal(state):
            break
        else:
            action_count = calc_action_count(node)
            neighbors = [Node(state_transition(state, action), node, action) for action in action_count if action_count[action] < 1 or action == "plug_in_toaster" and action_count["plug_in_toaster"] < 2]
            neighbors.sort()
            frontier.extend(neighbors)

    seq = []
    currentNode = checked.pop()
    while True:
        if not currentNode:
            break
        else:
            if currentNode.action:
                seq.append(currentNode.action)
                currentNode = currentNode.parent
            else:
                break

    seq.reverse()
    return seq

def greedy_dfs_none_stop(start_state):
    frontier = []
    checked = []
    goal_nodes = []

    frontier.append(Node(start_state, None, None))

    while len(frontier) > 0:
        node = frontier.pop()
        checked.append(node)
        state = node.state

        if goal(state):
            goal_nodes.append(node)
        else:
            action_count = calc_action_count(node)
            neighbors = [Node(state_transition(state, action), node, action) for action in action_count if action_count[action] < 1 or action == "plug_in_toaster" and action_count["plug_in_toaster"] < 2]
            neighbors.sort()
            frontier.extend(neighbors)


    seq = []
    currentNode = min(goal_nodes, key= lambda x: x.state["time"])
    while True:
        if not currentNode:
            break
        else:
            if currentNode.action:
                seq.append(currentNode.action)
                currentNode = currentNode.parent
            else:
                break

    seq.reverse()
    return seq


def calc_action_count(node):
    action_counter = {
        "plug_in_toaster": 0,
        "unplug_toaster": 0,
        "put_in_bread": 0,
        "take_out_bread": 0,
        "switch_on_toaster": 0,
        "wait": 0
    }
    while True:
        if node is None:
            break
        else:
            if node.action:
                action_counter[node.action] += 1
                node = node.parent
            else:
                break

    return action_counter

def pick_best_node(frontier):
    best = min(frontier, key=lambda x: x[0] + x[1].state["time"])
    frontier.remove(best)
    return best

# this is a test function. It tests your plan function 
def test(algorithm, start_state):
    print("\n\n testing:",start_state)

    # call plan function
    sequence = plan(algorithm, start_state)
    print("\t found sequence:",sequence)

    # apply plan to start state
    state = start_state
    for action in sequence:
        state = state_transition(state,action)
    
    # check whether result fulfills the goal
    print("\t fulfills goal?", goal(state))
    print("\t in world time",state["time"])

# execute the test for a few test cases
ALGORITHM = 4 # 0=BFS, 1=A*(TODO), 2=oone, 3=greedy_bfs 4=greedy none stop


test(ALGORITHM, state)
test(ALGORITHM, {'toaster_has_power': True, 'toaster_is_on': False, 'bread_location': 'toaster', 'bread_state': 'untoasted', 'time': 0})
test(ALGORITHM, {'toaster_has_power': True, 'toaster_is_on': True, 'bread_location': 'plate', 'bread_state': 'untoasted', 'time': 0})
test(ALGORITHM, {'toaster_has_power': False, 'toaster_is_on': True, 'bread_location': 'plate', 'bread_state': 'untoasted', 'time': 0})