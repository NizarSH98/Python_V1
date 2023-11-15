from collections import deque
import random
import tkinter as tk

goalstate = [
    1,2,3,
    4,5,6,
    7,8,0]

currentState = list(range(9))  # Create a list from 0 to 8
random.shuffle(currentState)  # Shuffle the list in place

def getSuccessors(currentState):
    zeroIndex = currentState.index(0)
    validMoves = []

    if zeroIndex % 3 > 0:  # Check if zero can move left
        validMoves.append("l")

    if zeroIndex % 3 < 2:  # Check if zero can move right
        validMoves.append("r")

    if zeroIndex >= 0 and zeroIndex <= 5:
        validMoves.append("d")

    if zeroIndex >= 3 and zeroIndex <= 8:
        validMoves.append("u")

    return validMoves

def isGoalState(currentState,goalState):
    return (currentState==goalState)

def bfs(currentState, goalState):
    frontier = deque([(currentState, [])])  # Initialize the frontier queue with the initial state and an empty path
    explored = set()  # Initialize the set of explored states

    while frontier:
        state, path = frontier.popleft()  # Get the first state and its path from the queue

        if isGoalState(state, goalState):
            return path  # If the goal state is reached, return the path

        explored.add(tuple(state))  # Add the state to the set of explored states

        for move in getSuccessors(state):
            nextState = getNewState(state, move)
            if tuple(nextState) not in explored:
                frontier.append((nextState, path + [move]))  # Add the next state and its path to the frontier

    return None  # If no solution is found, return None 


def getNewState(currentState, move):
    zeroIndex = currentState.index(0)
    newZeroIndex = zeroIndex

    if move == "l":
        newZeroIndex -= 1
    elif move == "r":
        newZeroIndex += 1
    elif move == "u":
        newZeroIndex -= 3
    elif move == "d":
        newZeroIndex += 3

    newState = list(currentState)
    newState[zeroIndex], newState[newZeroIndex] = newState[newZeroIndex], newState[zeroIndex]

    return newState

animating_moves = deque()

def make_move():
    global currentState, animating_moves
    if animating_moves:
        move = animating_moves.popleft()
        currentState = getNewState(currentState, move)  # Update the currentState
        update_gui()
        if animating_moves:
            root.after(500, make_move)


# Define a function to update the GUI with the current state
def update_gui():
    for i in range(3):
        for j in range(3):
            value = currentState[i*3+j]
            labels[i][j].config(text=str(value) if value != 0 else '', font=("Helvetica", 16, "bold"))

# Define a function to start the animation
def start_animation():
    global animating_moves
    animating_moves = deque(bfs(currentState, goalstate))
    make_move()


# Create the main window
root = tk.Tk()
root.title("8 Puzzle Game")

# Create labels for the puzzle tiles
labels = [[tk.Label(root, width=5, height=2, font=("Helvetica", 16, "bold"), relief="solid") for _ in range(3)] for _ in range(3)]

# Place the labels in the grid
for i in range(3):
    for j in range(3):
        labels[i][j].grid(row=i, column=j)

# Create a button to start the animation
start_button = tk.Button(root, text="Start Animation", command=start_animation)
start_button.grid(row=3, column=0, columnspan=3)

# Start the GUI event loop
root.mainloop()
