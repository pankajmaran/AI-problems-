from collections import deque


def BFS(waterCapacityOfJug1, waterCapacityOfJug2, target):
    visited = {}
    isSolvable = False
    path = []
    # Queue to maintain states
    queList = deque()
    # Initialing with initial state
    queList.append((0, 0))
    while (len(queList) > 0):
        # Current state
        curState = queList.popleft()
        # If this state is already visited
        if ((curState[0], curState[1]) in visited):
            continue
        # Doesn't met jug constraints
        if ((curState[0] > waterCapacityOfJug1 or curState[1] > waterCapacityOfJug2 or curState[0] < 0 or curState[1] < 0)):
            continue
        # Filling the vector for constructing the solution path
        path.append([curState[0], curState[1]])
        # Marking current state as visited
        visited[(curState[0], curState[1])] = 1
        # If we reach solution state, put ans=1
        if (curState[0] == target or curState[1] == target):
            isSolvable = True

            if (curState[0] == target):
                if (curState[1] != 0):
                    # Fill final state
                    path.append([curState[0], 0])
            else:
                if (curState[0] != 0):
                    # Fill final state
                    path.append([0, curState[1]])

            # Print the solution path
            size = len(path)
            print("\tJUG1 \t JUG2")
            for i in range(size):
                print("\t", path[i][0], "\t", path[i][1])
            break

        queList.append([curState[0], waterCapacityOfJug2])  # Fill Jug2
        queList.append([waterCapacityOfJug1, curState[1]])  # Fill Jug1

        for gallenOfWaterTransfer in range(max(waterCapacityOfJug1, waterCapacityOfJug2) + 1):
            # Pour amount ap from Jug2 to Jug1
            newStateOfJug1 = curState[0] + gallenOfWaterTransfer
            newStateOfJug2 = curState[1] - gallenOfWaterTransfer
            # Check if this state is possible or not
            if (newStateOfJug1 == waterCapacityOfJug1 or (newStateOfJug2 == 0 and newStateOfJug2 >= 0)):
                queList.append([newStateOfJug1,  newStateOfJug2])
            # Pour amount ap from Jug 1 to Jug2
            newStateOfJug1 = curState[0] - gallenOfWaterTransfer
            newStateOfJug2 = curState[1] + gallenOfWaterTransfer
            # Check if this state is possible or not
            if ((newStateOfJug1 == 0 and newStateOfJug1 >= 0) or newStateOfJug2 == waterCapacityOfJug2):
                queList.append([newStateOfJug1,  newStateOfJug2])
        # Empty Jug2
        queList.append([waterCapacityOfJug1, 0])
        # Empty Jug1
        queList.append([0, waterCapacityOfJug2])

    # No, solution exists if ans=0
    if (not isSolvable):
        print("No solution")


# Driver code
Jug1 = int(input("Enter the capacity of jug 1 "))
Jug2 = int(input("Enter the capacity of jug 2 "))
target = int(input("Enter the target capacity "))
print("Path from initial state to solution state :: ")
BFS(Jug1, Jug2, target)
