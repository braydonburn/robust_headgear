
'''

The partially defined functions and classes of this module 
will be called by a marker script. 

You should complete the functions and classes according to their specified interfaces.
 

'''

import search

import sokoban

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -




def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (9715894, 'Braydon', 'Burn'), (9665021, 'Michael', 'Blair') ]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell is called 'taboo' 
    if whenever a box get pushed on such a cell then the puzzle becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
              
    tabooCoords = []
    
    #   Create a master list of walls and targets (so that these space don't
    #   become taboo cells)
    walls_targets = []
    for wall in warehouse.walls:
        walls_targets.append(wall)
        
    for target in warehouse.targets:
        walls_targets.append(target)
        
        
    # Testing for corners can be done by testing for diagonal relationships
    # between wall cells
    for wall in warehouse.walls:
        topLeft = move_coords(move_coords(wall, "Up"), "Left")
        topRight = move_coords(move_coords(wall, "Up"), "Right")
        bottomLeft = move_coords(move_coords(wall, "Down"), "Left")
        bottomRight = move_coords(move_coords(wall, "Down"), "Right")
        
        if (topLeft in warehouse.walls) and \
           (move_coords(wall, "Left") not in walls_targets):
            tabooCoords.append(move_coords(wall, "Left"))
            
        if topRight in warehouse.walls and \
            (move_coords(wall, "Right") not in walls_targets):
            tabooCoords.append(move_coords(wall, "Right"))
            
        if bottomLeft in warehouse.walls and \
            (move_coords(wall, "Left") not in walls_targets):
            tabooCoords.append(move_coords(wall, "Left"))
            
        if bottomRight in warehouse.walls and \
            (move_coords(wall, "Right") not in walls_targets):
            tabooCoords.append(move_coords(wall, "Right"))
            
#    print(tabooCoords)
    newCells = []
    #print(newCells)
    
    # Check to see if there are paths between taboo cells along walls
    for coord in tabooCoords:
        for secondcoord in tabooCoords:
            cellsToAdd = taboo_along_wall(warehouse,coord, secondcoord) 
            if cellsToAdd is not None:
                for cell in cellsToAdd:
                    newCells.append(cell)
                
    for coord in newCells:
        tabooCoords.append(coord)
                
    # Remove any multiples in the list of taboo cells
    cleanTaboo = list(set(tabooCoords))
    tabooCoords = []
    for coord in cleanTaboo:
        if coord not in warehouse.walls:
            tabooCoords.append(coord)
        

    '''
    Return a string representation of the warehouse
    '''

    X,Y = zip(*warehouse.walls)
    x_size, y_size = 1+max(X), 1+max(Y)
    
    vis = [[''' '''] * x_size for y in range(y_size)]
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in tabooCoords:
        vis[y][x] = "X"
           
    vis = vis[1:]
    
    vis = "\n".join(["".join(line) for line in vis])
    vis = "\n" + vis
    return vis 
        
    


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.
    
    	Use the sliding puzzle and the pancake puzzle for inspiration!
    
    '''    
    def __init__(self, warehouse, initial=None, goal=None):
        
        self.warehouse = warehouse
        self.taboo = list(sokoban.find_2D_iterator(taboo_cells(warehouse).split(sep='\n'), "X"))
        self.walls = warehouse.walls
        self.targets = warehouse.targets
        

        if initial is not None:
            self.initial = initial
        else:
            self.initial = (self.warehouse.worker,tuple(self.warehouse.boxes))
            
        if goal is not None:
            self.goal = goal
        else: 
            self.goal = self.warehouse.targets
        assert set(self.goal) == set(warehouse.targets)
        
        x,y = zip(*warehouse.walls)
        self.x_length = 1 + max(x)
        self.y_length = 1 + max(y)
        
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state 
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']        
        """
        MovementList = []
        #Check if the agent is able to move a box (Left, Down, Right, Up) 
        #without moving it into a taboo cell or pushing two blocks (Invalid move)
        #then move the box in the given direction.
        
        possible_moves = ["Up", "Down", "Left", "Right"]
        
        worker = state[0]
        boxes = state[1]
        
        # Iterate throguh the moves and make sure they satify constraints
        for move in possible_moves:
            if (move_coords(worker, move) not in self.walls):
                if (move_coords(worker, move) in boxes):
                    if move_coords(move_coords(worker, move), move) in self.taboo:
                        pass
                    else: 
                        MovementList.append(move)
                else:
                    MovementList.append(move)
                
        return MovementList
    
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        applying action a to state s results in
        s_next = s[:a]+s[-1:a-1:-1]        """
        
        assert action in self.actions(state)
        worker = state[0]
        boxes = state[1]
        newBoxes = []
        
        worker = move_coords(worker, action)
        
        for box in boxes:
            if worker == box:
                newBox = move_coords(box, action)
                newBoxes.append(newBox)
            else:
                newBoxes.append(box)
                
        newState = ((worker), tuple(newBoxes))
        return newState

        


    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return (set(state[1]) == set(self.goal))
        

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        # This should probably just be 1 every state....
        return c + 1


    def h(self, node):
        '''
        Heuristic for goal state of the form range(k,-1,1) where k is a positive integer. 
        h(n) = distance of 
        '''     
        # for each box, summ the distance to the closes target space
        total_h = 0
        dist = 0
        
        #worker = node.state[0]
        boxes = node.state[1]
        for box in boxes:
            close_target = closest_target(box, self.goal)
            dist += (abs(close_target[0] - box[0]) + abs(close_target[1] - box[1]))
                
        total_h += dist
        print(total_h)
        return total_h
                
            

        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''    
    temp_wh = warehouse

    for direction in action_seq:
        if move_coords(temp_wh.worker, direction) in temp_wh.walls:
            return 'Failure'
        elif (move_coords(temp_wh.worker, direction) in temp_wh.boxes) and \
             (move_coords(move_coords(temp_wh.worker, direction), direction) in \
             temp_wh.boxes):
            return 'Failure'
        else:
            temp_wh.worker = move_coords(temp_wh.worker, direction)
            for box in temp_wh.boxes:
                if (temp_wh.worker == box) and (move_coords(move_coords(box, direction), direction) not in temp_wh.walls):
                    box = move_coords(box, direction)
                    
    string = temp_wh.__str__()
                    
    return string

            
 
    
               
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        A list of strings.
        If puzzle cannot be solved return ['Impossible']
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    #Implement check to see if impossible.
    
    puzzle = SokobanPuzzle(warehouse)
    
    solution = search.astar_graph_search(puzzle, puzzle.h)#lambda n:puzzle.h(n))
    
    if solution == None:
        return 'Impossible'
    else:
        return search.Node.solution(solution)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,col) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,col) without pushing any box
      False otherwise
    '''
    
    ## MINI SEARCH!! 
    new_wh = warehouse.copy()
    
    
    not_free = new_wh.walls.copy()
    for box in new_wh.boxes:
        not_free.append(box)
        
    dst = dst
        
    wk = new_wh.worker
    old_worker = wk    
    backtrack = 0
    tries = 0
    going = True
    
    moves = ['Left', 'Right', 'Down', 'Up']
    
    if dst in not_free:
        return False
    
    if dst == wk:
        return True
    
    while going:
#        print(wk)
        for move in moves:
            if move_coords(wk, move) not in not_free:
                not_free.append(wk)
                old_worker = wk
                wk = move_coords(wk, move)
#                print(not_free)
                if wk == dst:
                    going = False
                    return True
                tries = 0
                break
            else:
                tries += 1
            
        if tries > 3:
            backtrack += 1
            wk = old_worker
        if backtrack > 3:
            going = False
            return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return ['Impossible']
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    puzzle = SokobanMacro(warehouse)
    
    if puzzle.goal_test(puzzle.initial):
        return []
    
    solution = search.astar_tree_search(puzzle, puzzle.h)
    
    if solution == None:
        return ['Impossible']
    else:
        return search.Node.solution(solution)
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
class SokobanMacro(search.Problem):
    
    def __init__(self, warehouse, initial=None, goal=None):
        
        self.warehouse = warehouse
        self.taboo = list(sokoban.find_2D_iterator(taboo_cells(warehouse).split(sep='\n'), "X"))
        self.walls = warehouse.walls
        self.targets = warehouse.targets
        

        if initial is not None:
            self.initial = initial
        else:
            self.initial = (self.warehouse.worker,tuple(self.warehouse.boxes))
            
        if goal is not None:
            self.goal = goal
        else: 
            self.goal = self.warehouse.targets
        assert set(self.goal) == set(warehouse.targets)
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state 
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']        
        """
        MovementList = []
        #Check if the agent is able to move a box (Left, Down, Right, Up) 
        #without moving it into a taboo cell or pushing two blocks (Invalid move)
        #then move the box in the given direction.
        
        
        moves = ["Up", "Down", "Left", "Right"]
        opposite_moves = ["Down", "Up", "Right", "Left"]
        worker = state[0]
        boxes = state[1]
        temp_warehouse = self.warehouse.copy(worker, boxes)
        no_go = self.taboo.copy()
        for wall in self.walls:
            no_go.append(wall)
        print("No go: ", no_go)
        print(boxes)
        for box in boxes:
            for move in moves:
                if (move_coords(box, move) not in no_go) and (move_coords(box, move)\
                               not in boxes):
                    if can_go_there(temp_warehouse, \
                    move_coords(box, opposite_moves[moves.index(move)])):
                        MovementList.append((box, move))
        
        
        print(MovementList)
        return MovementList
    
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        applying action a to state s results in
        s_next = s[:a]+s[-1:a-1:-1]        """
        
        assert action in self.actions(state)
        worker = state[0]
        boxes = state[1]
        if len(action[0]) > 2:
            move = action[0][1]
            coord = action[0][0]
        else:
            move = action[1]
            coord = action[0]
        
        newBoxes = []
        
        worker = coord
        
        for box in boxes:
            if box == coord:
                newBox = move_coords(box, move)
                newBoxes.append(newBox)
            else:
                newBoxes.append(box)
        
        newState = ((worker), tuple(newBoxes))
        return newState

        


    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return (set(state[1]) == set(self.goal))
        

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        # This should probably just be 1 every state....
        return c + 1


    def h(self, node):
        '''
        Heuristic for goal state of the form range(k,-1,1) where k is a positive integer. 
        h(n) = distance of 
        '''     
        # for each box, summ the distance to the closes target space
        total_h = 0
        dist = 0
        print(node)
        worker = node.state[0]
        boxes = node.state[1]
        for box in boxes:
            close_target = closest_target(box, self.goal)
            dist += manhattan_distance(box, close_target)
        
        # add the manhattan distance for each action in the node.state
        NodeActions = self.actions(node.state)
        for action in NodeActions:
            dist += manhattan_distance(action[0], node.state[0])
                
        total_h += dist
        print(total_h)
        return total_h
        
    
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


### - - - - - - < < < < HELPER METHODS > > > > - - - - - - ###
def manhattan_distance(tup, tup2):
    return abs(tup[0] - tup2[0])+ abs(tup[1]-tup2[1])

def move_coords(tup, action):
    '''
    By reading in an action, augment the tuple of coords by the correct amount
    
    @param (x,y): a set of coordinates as a tuple
    @param action: a string representing a one space move either;
                                            Up, Down, Left, Right

    @return
        New coordinates as a tuple
    '''    
    x2 = tup[0]
    y2 = tup[1]
    if (action is 'Up'):
        y2 -= 1
    elif (action is 'Down'):
        y2 += 1
    elif (action is 'Left'):
        x2 -= 1
    elif (action is 'Right'):
        x2 += 1
    return (x2, y2)
        
def taboo_along_wall(warehouse, tup1, tup2):
    '''
    Performs a test to see if there is a direct line from one taboo corner to
    another
    
    @param warehouse: a state of a Warehouse object
    @param tup1: first set of taboo coordinates
    @param tup2: second set of taboo coordinates

    @return
        List of new taboo cells to be added
    '''   
    x1 = tup1[0]
    x2 = tup2[0]
    y1 = tup1[1]
    y2 = tup2[1]
    
    #print(x1, y1, 'to', x2, y2)
    
    newCells = []
        
    if (x1 == x2):
        for i in range(min(y1, y2), max(y1, y2)+1):
           #print(x1, i)
            if (x1, i) in warehouse.targets:
                return None
            
            if (x1, i)  == (x1, max(y1, y2)):
                return newCells
           
            if ((x1-1, i) in warehouse.walls) or ((x1+1, i) in warehouse.walls):
                newCells.append((x1, i))
    
    elif (y1 == y2):
        for i in range(min(x1, x2), max(x1, x2)+1):
            if (i, y1) in warehouse.targets:
                return None
            
            if (i, y1) == (max(x1, x2), y1):
                return newCells
           
            if ((i, y1-1) in warehouse.walls) or ((i, y1+1) in warehouse.walls):
                newCells.append((i, y1))
                #print(newCells)
                
    else:
        return newCells
    
#def taboo_check(coords, taboo_string):
#    '''
#    Check if a given coordinate is taboo or not by calling taboo_cells
#    
#    '''
#    taboo_list = extract_taboo(taboo_string.split(sep='\n'))
#    #return taboo_list
#    if coords in taboo_list:
#        return True
#    else:
#        return False
    
def extract_taboo(lines):
    taboo =  list(sokoban.find_2D_iterator(lines, "X"))  # taboo_cells
    return taboo

def closest_target(box, targets):
    distance = ((0,0),1000000)
    target_holder = targets
#    print("Length before ", len(target_holder))
    
#    while len(target_holder) > 1:
    
    for i in range(len(target_holder)):
        target_dist = abs(target_holder[i][0] - box[0]) + abs(target_holder[i][1] - box[1])
        if target_dist <= distance[1]:
            distance = (target_holder[i], target_dist)
        
#        temp_box = []
#        for target in target_holder:
#            if target != distance[0]:
#                temp_box.append(target)
#        target_holder = temp_box
#        print("Length after ", len(target_holder))
    
    #print(box, distance[0], temp_box)
    return distance[0]
    


wh = sokoban.Warehouse()
wh.read_warehouse_file("./warehouses/warehouse_01.txt")
print(wh)
t = SokobanPuzzle(wh)
l = SokobanMacro(wh)
#print(can_go_there(wh, (5,5)))


#              CODE GRAVEYARD!
#
#                    .
#                   -|-
#                    |
#                .-'~~~`-.
#              .'         `.
#              |  R  I  P  |
#              |           |
#              |           |
#            \\|           |//
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#    # Remove any taboo cells placed on top of targets
#    for coord in tabooCoords:
#        if coord in warehouse.targets:
#            tabooCoords.remove(coord)
#    #Define Left movement
#            if ((x_position-1, y_position) not in self.warehouse.walls):
#                if ((x_position-1, y_position) in self.warehouse.boxes):
#                    if ((x_position-2, y_position) not in self.warehouse.walls)\
#                    and ((x_position-2, y_position) not in self.warehouse.boxes)\
#                    and ((x_position-2, y_position) not in self.taboo_check):
#                            MovementList.append("Left")
#            
#            #Define Down movement
#            if ((x_position, y_position+1) not in self.warehouse.walls):
#                if ((x_position, y_position+1) in self.warehouse.boxes):
#                    if ((x_position, y_position+2) not in self.warehouse.walls)\
#                    and ((x_position, y_position+2) not in self.warehouse.boxes)\
#                    and ((x_position, y_position+2) not in self.taboo_check):
#                            MovementList.append("Down")
#                            
#            #Define Right movement
#            if ((x_position+1, y_position) not in self.warehouse.walls):
#                if ((x_position+1, y_position) in self.warehouse.boxes):
#                    if ((x_position+2, y_position) not in self.warehouse.walls)\
#                    and ((x_position+2, y_position) not in self.warehouse.boxes)\
#                    and ((x_position+2, y_position) not in self.taboo_check):
#                            MovementList.append("Right")
#            
#            #Define Up movement
#            if ((x_position, y_position-1) not in self.warehouse.walls):
#                if ((x_position, y_position-1) in self.warehouse.boxes):
#                    if ((x_position, y_position-2) not in self.warehouse.walls)\
#                    and ((x_position, y_position-2) not in self.warehouse.boxes)\
#                    and ((x_position, y_position-2) not in self.taboo_check):
#                            MovementList.append("Up") 
