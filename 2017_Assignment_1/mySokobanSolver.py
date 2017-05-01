
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
        
        if initial is not None:
            self.initial = initial
        else:
            self.initial = self.warehouse.boxes
            
        if goal is not None:
            self.goal = goal
        else: 
            self.goal = warehouse.targets
        assert set(self.goal) == set(warehouse.targets)
        
        x,y = zip(*warehouse.walls)
        self.x_length = 1 + max(x)
        self.y_length = 1 + max(y)
        
            
        self.initial = tuple(self.initial)
        self.goal = tuple(self.goal)
        
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
        
        # Iterate throguh the moves and make sure they satify constraints
        for move in possible_moves:
            if (move_coords(self.warehouse.worker, move) not in self.warehouse.walls):
                if (move_coords(self.warehouse.worker, move) in self.warehouse.boxes):
                    if taboo_check(move_coords(move_coords(self.warehouse.worker, move), move), taboo_cells(self.warehouse)):
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
        self.warehouse.worker = move_coords(self.warehouse.worker, action)
        
        newState = []
        
        for box in state:
            print("Worker:", self.warehouse.worker)
            if self.warehouse.worker == box:
                print("It's in my space")
                newBox = move_coords(box, action)
                newState.append(newBox)
            else:
                newState.append(box)
                
        newState = tuple(newState)
        self.warehouse = self.warehouse.copy(newState, self.warehouse.worker)
        print(self.warehouse)
        
                  
        return newState

        


    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return (set(state) == set(self.goal))
        

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
        for box in node:
            close_target = closest_target(box, self.goal)
            dist += (abs(close_target[0] - box[0]) + abs(close_target[1] - box[1]))
                
        total_h += dist
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
    wh = SokobanPuzzle(warehouse)
    
    current_state = []
    
    if action_seq[0] in wh.actions(wh.initial):
        current_state = wh.result(action_seq[0], action_seq[0])
        for i in range(1, len(action_seq)):
            if action_seq[i] in wh.actions(current_state):
                current_state = wh.result(current_state, action_seq[i])
            else:
                return 'Failure'
        return wh.__str__()
    else:
        return 'Failure'
            
 
    
               
    
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
    
    solution = search.breadth_first_tree_search(puzzle#, lambda n:puzzle.h(n))
    )
    
    return puzzle.return_path(solution.path())

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
    
    x,y = zip(*warehouse.walls)
    x_length = 1 + max(x)
    y_length = 1 + max(y)
    
    for box in warehouse.boxes:
        #Check if the destination is out of bounds
        if dst[0] > x_length or dst[0] < 0:
            return False
        elif dst[1] > y_length or dst[1] < 0:
            return False
        #Check if the worker is being blocked(x), check aginst y of box and worker
        elif box[0] in range(warehouse.worker[0],dst[0]) and box[1] is warehouse.worker[1]:
            return False
        #Check if the worker is being blocked(y), check aginst x of box and worker
        elif box[1] in range(warehouse.worker[1],dst[1]) and box[0] is warehouse.worker[0]:
            return False
        #Check if the worker is being blocked(both)
        elif box[1] in range(warehouse.worker[0], dst[0]) and box[1] in range(warehouse.worker[1], dst[1]):
            return False
        else:
            return True

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
    ##         "INSERT YOUR CODE HERE"
    
    
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


### - - - - - - < < < < HELPER METHODS > > > > - - - - - - ###
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
    
def taboo_check(coords, taboo_string):
    '''
    Check if a given coordinate is taboo or not by calling taboo_cells
    
    '''
    taboo_list = extract_taboo(taboo_string.split(sep='\n'))
    #return taboo_list
    if coords in taboo_list:
        return True
    else:
        return False
    
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
wh.read_warehouse_file("./warehouses/warehouse_03.txt")
print(wh)
t = SokobanPuzzle(wh)
print(t.h(t.initial))


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
