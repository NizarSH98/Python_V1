#install numpy using: pip install numpy

from collections import deque
import heapq
import math


class Search_Agent:
    
    def __init__(self,grid,startState,goalState):
    
        self.grid=grid
        self.num_rows=len(self.grid)
        self.num_cols=len(self.grid)
        self.startState=startState #[1][1]
        self.goalState=goalState #[19][19]
        
        self.actions=["n","w","s","e"]
    
    def pushPriorityQueue(self,pq,node):  
        updated=False

        for n in pq:
            if n[1]==node[1]:
                updated=True
                if node[0]<n[0]:
                    pq[pq.index(n)]=node
                    break

        if not updated:
            heapq.heappush(pq,node)    


    def getDirectionFromAction(self,action):
        if action=="n":
            return (-1,0)
        elif action=="w":
            return (0,-1)
        elif action=="s":
            return (1,0)
        elif action=="e":
            return (0,1)
        
    def isWall(self,x,y):
        if x==-1 or y==-1 or x==self.num_rows or y==self.num_cols:
            return True
        elif self.grid[x][y]==1:
            return True
        else:
            return False
        
    def getSuccessor(self,state):
        successors=[]
        x,y=state
        
        for action in self.actions:
            dx,dy=self.getDirectionFromAction(action)
            nextX=x+dx
            nextY=y+dy
            if not self.isWall(nextX,nextY):
                cost=1
                successors.append((action,(nextX,nextY),cost))       
            
        return successors


    def getHeuristics(self,state,heuristic="euclidean"):
        x1,y1=state
        x2,y2=self.goalState
        d=math.sqrt((x2-x1)*(x2-x1) +(y2-y1)*(y2-y1))
        return d

 
    def isGoalState(self,state):
        return (state==self.goalState)
    
    def dfs(self):
        frontiers = deque()
        exploredStates = []
        startNode=(self.startState,[])
        s=self.getSuccessor(self.startState)
        print("start node:",startNode)
        print("successor:",s)
        frontiers.append(startNode)
        while frontiers:
            node=frontiers.pop()
            currState,currActions=node
            print("X:" ,currState)
            if(self.isGoalState(currState)):
                return currActions,exploredStates
            else:
                if currState not in exploredStates:
                    successors=self.getSuccessor(currState)
                    exploredStates+=[currState]
                    for s in successors:
                        action, (nextX, nextY), cost = s
                        nextActions=currActions+[action]
                        nextNode=((nextX, nextY), nextActions)
                        frontiers.append(nextNode)
                    
                    
        
            print("Frontiers", frontiers)
            print("Explored States: ",exploredStates,"\n")
   
            
        return False

   
    def bfs(self):
        frontiers = deque()
        exploredStates = set()
        startNode = (self.startState, [])
        frontiers.append(startNode)
        while frontiers:
            node = frontiers.popleft()
            currState, currActions = node
            if self.isGoalState(currState):
                return currActions,exploredStates
            else:
                if currState not in exploredStates:
                    successors = self.getSuccessor(currState)
                    exploredStates.add(currState)
                    for action, (nextX, nextY), cost in successors:
                        nextActions = currActions + [action]
                        nextNode = ((nextX, nextY), nextActions)
                        frontiers.append(nextNode)
        return False       
   
    def ucs(self):        
        frontiers = []
        exploredStates = set()
        startNode = (0, self.startState, [])
        heapq.heappush(frontiers, startNode)
        while frontiers:
            cost, currState, currActions = heapq.heappop(frontiers)

            if self.isGoalState(currState):
                return currActions,exploredStates,cost
            else:
                if currState not in exploredStates:
                    successors = self.getSuccessor(currState)
                    exploredStates.add(currState)
                    for action, (nextX, nextY), action_cost in successors:
                        nextActions = currActions + [action]
                        nextCost = cost + action_cost
                        nextNode = (nextCost, (nextX, nextY), nextActions)
                        heapq.heappush(frontiers, nextNode)
        return False
    
    def astar(self, heuristic="manhattan"):
        frontiers = []
        exploredStates = set()
        startNode = (0, self.startState, [], 0 )
        heapq.heappush(frontiers, startNode)
        while frontiers:
            _, currState, currActions, g = heapq.heappop(frontiers)

            if self.isGoalState(currState):
                return currActions,exploredStates,f
            else:
                if currState not in exploredStates:
                    successors = self.getSuccessor(currState)
                    exploredStates.add(currState)
                    for action, (nextX, nextY), action_cost in successors:
                        nextActions = currActions + [action]
                        nextG = g + action_cost
                        h = self.getHeuristics((nextX, nextY), heuristic)
                        f = nextG + h
                        nextNode = (f, (nextX, nextY), nextActions, nextG)
                        heapq.heappush(frontiers, nextNode)
        return False













class Corners_Problem:


    def __init__(self,grid,startState,goalState):
    
        self.grid=grid
        self.num_rows=len(self.grid)
        self.num_cols=len(self.grid)
        self.startState=startState #[1][1]
        self.goalState=goalState #[19][19]
        
        self.actions=["n","w","s","e"]
    
    def pushPriorityQueue(self,pq,node):  
        updated=False

        for n in pq:
            if n[1]==node[1]:
                updated=True
                if node[0]<n[0]:
                    pq[pq.index(n)]=node
                    break

        if not updated:
            heapq.heappush(pq,node)    


    def getDirectionFromAction(self,action):
        if action=="n":
            return (-1,0)
        elif action=="w":
            return (0,-1)
        elif action=="s":
            return (1,0)
        elif action=="e":
            return (0,1)
        
    def isWall(self,x,y):
        if x==-1 or y==-1 or x==self.num_rows or y==self.num_cols:
            return True
        elif self.grid[x][y]==1:
            return True
        else:
            return False
        
    def getSuccessor(self,state):
        successors=[]
        x,y=state
        
        for action in self.actions:
            dx,dy=self.getDirectionFromAction(action)
            nextX=x+dx
            nextY=y+dy
            if not self.isWall(nextX,nextY):
                cost=1
                successors.append((action,(nextX,nextY),cost))       
            
        return successors


    def getHeuristics(self,state,heuristic="euclidean"):
        x1,y1=state
        x2,y2=self.goalState
        d=math.sqrt((x2-x1)*(x2-x1) +(y2-y1)*(y2-y1))
        return d

 
    def isGoalState(self,state):
        return (state==self.goalState)


    def dfs(self):
        frontiers = deque()
        exploredStates = []
        startNode=(self.startState, [], [False, False, False, False])
        s=self.getSuccessor(self.startState)
        #print("start node:",startNode)
        #print("successor:",s)
        frontiers.append(startNode)
        while frontiers:
            
            currState, currActions, visited_corners=frontiers.pop()
            
            print("X:" ,currState)
            print(visited_corners)
            if visited_corners == [True,True,True,True]:
                return currActions,exploredStates

            else:
                if currState not in exploredStates:
                    successors=self.getSuccessor(currState)
                    exploredStates+=[currState]
                    for s in successors:
                        action, (nextX, nextY), cost = s
                        nextActions=currActions+[action]
                        if (currState[0], currState[1]) == (1, 1) and visited_corners[0]==False:
                            visited_corners[0] = True
                            exploredStates =[(1, 1)]
                        if (currState[0], currState[1]) == (1, 19) and visited_corners[1]==False:
                            visited_corners[1] = True
                            exploredStates =[(1, 19)]
                        if (currState[0], currState[1]) == (19, 1) and visited_corners[2]==False:
                            visited_corners[2] = True
                            exploredStates =[(19, 1)]
                        if (currState[0], currState[1]) == (19, 19) and visited_corners[3]==False:
                            visited_corners[3] = True
                            exploredStates =[(19, 19)]
                        nextNode=((nextX, nextY), nextActions, visited_corners)
                        frontiers.append(nextNode)
                    
            
                    
        
   
            
        return False




















    def astar(self, heuristic="manhattan"):
        frontiers = []
        exploredStates = []
        totalExplored = []
        startNode = (0, self.startState, [], [False, False, False, False], 0)
        heapq.heappush(frontiers, startNode)

        while frontiers:
            _, currState, currActions, visited_corners, g = heapq.heappop(frontiers)

            print("X:" ,currState)
            print(visited_corners)
            if visited_corners == [True,True,True,True]:
                return currActions, totalExplored, f

            if currState not in exploredStates:
                successors = self.getSuccessor(currState)
                exploredStates+=[currState]

                for action, (nextX, nextY), action_cost in successors:
                    nextActions = currActions + [action]
                    nextG = g + action_cost
                    h = self.getHeuristics((nextX, nextY), heuristic)
                    f = nextG + h

                    if (currState[0], currState[1]) == (1, 1) and visited_corners[0]==False:
                        visited_corners[0] = True
                        totalExplored = totalExplored + exploredStates
                        exploredStates =[(1, 1)]
                    if (currState[0], currState[1]) == (1, 19) and visited_corners[1]==False:
                        visited_corners[1] = True
                        totalExplored = totalExplored + exploredStates
                        exploredStates =[(1, 19)]
                    if (currState[0], currState[1]) == (19, 1) and visited_corners[2]==False:
                        visited_corners[2] = True
                        totalExplored = totalExplored + exploredStates
                        exploredStates =[(19, 1)]
                    if (currState[0], currState[1]) == (19, 19) and visited_corners[3]==False:
                        visited_corners[3] = True
                        totalExplored = totalExplored + exploredStates
                        exploredStates =[(19, 19)]

                    nextNode = (f, (nextX, nextY), nextActions, visited_corners, nextG)
                    heapq.heappush(frontiers, nextNode)

        return False
