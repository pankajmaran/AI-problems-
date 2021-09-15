class State:
    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None

    def isGameCompleted(self):
        if self.cannibalLeft == 0 and self.missionaryLeft == 0:
            return True
        else:
            return False

    def isValid(self):
        if self.missionaryLeft >= 0 and self.missionaryRight >= 0 and self.cannibalLeft >= 0 and self.cannibalRight >= 0 and (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) and (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight):
            return True
        else:
            return False


def successors(cur_state):
    children = []
    if cur_state.boat == 'left':
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft - 2,
                          'right', cur_state.cannibalRight, cur_state.missionaryRight + 2)
        # Two missionaries cross left to right.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft - 2, cur_state.missionaryLeft,
                          'right', cur_state.cannibalRight + 2, cur_state.missionaryRight)
        # Two cannibals cross left to right.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft - 1,
                          'right', cur_state.cannibalRight + 1, cur_state.missionaryRight + 1)
        # One missionary and one cannibal cross left to right.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft - 1,
                          'right', cur_state.cannibalRight, cur_state.missionaryRight + 1)
        # One missionary crosses left to right.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft - 1, cur_state.missionaryLeft,
                          'right', cur_state.cannibalRight + 1, cur_state.missionaryRight)
        # One cannibal crosses left to right.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
    else:
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft + 2,
                          'left', cur_state.cannibalRight, cur_state.missionaryRight - 2)
        # Two missionaries cross right to left.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft + 2, cur_state.missionaryLeft,
                          'left', cur_state.cannibalRight - 2, cur_state.missionaryRight)
        # Two cannibals cross right to left.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft + 1,
                          'left', cur_state.cannibalRight - 1, cur_state.missionaryRight - 1)
        # One missionary and one cannibal cross right to left.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft, cur_state.missionaryLeft + 1,
                          'left', cur_state.cannibalRight, cur_state.missionaryRight - 1)
        # One missionary crosses right to left.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
        new_state = State(cur_state.cannibalLeft + 1, cur_state.missionaryLeft,
                          'left', cur_state.cannibalRight - 1, cur_state.missionaryRight)
        # One cannibal crosses right to left.
        if new_state.isValid():
            new_state.parent = cur_state
            children.append(new_state)
    return children


def breadth_first_search():
    initial_state = State(3, 3, 'left', 0, 0)
    if initial_state.isGameCompleted():
        return initial_state
    queList = list()
    explored = set()
    queList.append(initial_state)
    while queList:
        state = queList.pop(0)
        if state.isGameCompleted():
            return state
        explored.add(state)
        children = successors(state)
        for child in children:
            if (child not in explored) or (child not in queList):
                queList.append(child)
    return None


def print_solution(solution):
    path = []
    path.append(solution)
    parent = solution.parent
    while parent:
        path.append(parent)
        parent = parent.parent

    for t in range(len(path)):
        state = path[len(path) - t - 1]
        print(" " +str(state.cannibalLeft) + "\t\t" + str(state.missionaryLeft) + "\t\t" +
              state.boat + "\t\t" + str(state.cannibalRight) + "\t\t" + str(state.missionaryRight))


solution = breadth_first_search()
print("\nMissionaries and Cannibals solution steps:\n")
print("cannibalLeft\tmissionaryLeft\tboat\tcannibalRight\tmissionaryRight")
print_solution(solution)
