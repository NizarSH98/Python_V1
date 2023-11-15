#run cmd as administrator
#install pygame using: pip install pygame
#install numpy using: pip install numpy
#pip install mazelib
#for a specific python
#py -3.6 -m pip install ...

import pygame

from search_agents import Search_Agent
from search_agents import Corners_Problem
import numpy as np
import copy
import time
#from mazelib import Maze
#from mazelib.generate.Prims import Prims
#from mazelib.generate.CellularAutomaton import CellularAutomaton
import search_mazes
from collections import deque
import heapq

class Board: 
    grid=[]
    def __init__(self,start,goal,maze,num_rows=8,num_cols=8,win_w=600,win_h=600,speed=0.2,margin=5):
            # Define some colors
        self.init=True
        
        self.SPEED = speed
        
        self.BLACK = (0, 0, 0)
        self.GREY = (75, 75, 75)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 150, 0)
        self.RED = (220, 0, 0)
        self.BLUE = (0, 150, 255)
        self.YELLOW = (150, 150, 0)
        
        #nb of rows and cols
        self.num_rows=num_rows
        self.num_cols=num_cols
        
        self.button_h=50
        self.button_w=100
        #windows width
        self.w=win_w-self.button_w
        self.h=win_h
               
        # This sets the margin between each cell
        self.margin=margin
        
        # This sets the WIDTH and HEIGHT of each grid location
        self.cell_w = int((self.w-(margin*(num_cols+1)))/num_cols)
        self.cell_h = int((self.h-(margin*(num_rows+1)))/num_rows)
         
        #chess piece max size
        max_peice_w=self.cell_w-5
        max_peice_h=self.cell_h-5
        
        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        
        
        self.start=start
        self.goal=goal
        if len(maze)==num_rows:
            self.grid=maze
        else:        
            self.grid=search_mazes.maze3
        
        
        """
        #initialize grid to zeros
        
        for row in range(num_rows):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(num_cols):
                self.grid[row].append(0)  # Append a cell
        """
        
        
        self.agent=Search_Agent(self.grid,self.start,self.goal)
        
        
        self.agent2=Corners_Problem(self.grid,self.start,self.goal)
        # Set row 1, cell 5 to one. (Remember rows and
        # column numbers start at zero.)
        #self.grid[1][5] = 1
 
        #initialize and scale the chess piece
        self.Queen_img = pygame.image.load('superman.png')
        self.Img_w = self.Queen_img.get_rect().size[0]
        self.Img_h = self.Queen_img.get_rect().size[1]
        self.Img_w = int(max_peice_h*self.Img_w/self.Img_h) if(self.Img_w<self.Img_h) else max_peice_w
        self.Img_h = int(max_peice_w*self.Img_h/self.Img_w) if(self.Img_w>self.Img_h) else max_peice_h
        self.Queen_img = pygame.transform.scale(self.Queen_img, (self.Img_w, self.Img_h))

        # Initialize pygame
        pygame.init()
         
        # Set the HEIGHT and WIDTH of the screen
        WINDOW_SIZE = [win_w, win_h]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
         
        # Set title of screen
        pygame.display.set_caption("Maze")
    
    def DrawButton(self,x,y,w,h,color,text):
        pygame.draw.rect(self.screen,color,(x,y,w,h));
        font = pygame.font.Font('freesansbold.ttf', 14)   
        b_text = font.render(text, True, self.WHITE, color) 
        textRect = b_text.get_rect()
        textRect.center = (x+w//2,y+h//2)
        self.screen.blit(b_text,textRect)
        
        return (x,y,w,h)
    
    def IsButtonClicked(self,b_rect,pos):
        x,y=pos
        if ((x>=b_rect[0])and(x<=(b_rect[0]+b_rect[2]))and(y>=b_rect[1])and(y<=(b_rect[1]+b_rect[3]))):
            return True
        return False
    def DrawGrid(self,character_location=(-1,-1)):
        screen = self.screen
        # Draw the grid
        is_odd=False
        for row in range(self.num_rows):
            is_odd=not is_odd
            for column in range(self.num_cols):
                if self.grid[row][column]==1:
                    color = self.BLACK
                elif self.grid[row][column]==0:
                    color = self.WHITE
                is_odd = not is_odd
                if self.grid[row][column] == -1:
                    color = self.RED
                    pygame.draw.rect(screen,
                                 color,
                                 [(self.margin + self.cell_w) * column + self.margin,
                                  (self.margin + self.cell_h) * row + self.margin,
                                  self.cell_w,
                                  self.cell_h])
                    #draw queen img
                    x,y=character_location
                    if (row==x)and(column==y):
                        screen.blit(self.Queen_img, ((self.margin + self.cell_w) * column + int((self.margin*2 + self.cell_w - self.Img_w)/2),(self.margin + self.cell_h) * row + int((self.margin*2 + self.cell_h - self.Img_h)/2)))
                elif self.grid[row][column] == 2:
                    color = self.RED
                    pygame.draw.rect(screen,
                                 color,
                                 [(self.margin + self.cell_w) * column + self.margin,
                                  (self.margin + self.cell_h) * row + self.margin,
                                  self.cell_w,
                                  self.cell_h])
                    if character_location[0]!=-1:
                        screen.blit(self.Queen_img, ((self.margin + self.cell_w) * column + int((self.margin*2 + self.cell_w - self.Img_w)/2),(self.margin + self.cell_h) * row + int((self.margin*2 + self.cell_h - self.Img_h)/2)))    
                    #screen.blit(self.Queen_img, ((self.margin + self.cell_w) * column + int((self.margin*2 + self.cell_w - self.Img_w)/2),(self.margin + self.cell_h) * row + int((self.margin*2 + self.cell_h - self.Img_h)/2))) 
                elif self.grid[row][column] == 3:
                    color = self.BLUE
                    pygame.draw.rect(screen,
                                 color,
                                 [(self.margin + self.cell_w) * column + self.margin,
                                  (self.margin + self.cell_h) * row + self.margin,
                                  self.cell_w,
                                  self.cell_h])
                    #screen.blit(self.Queen_img, ((self.margin + self.cell_w) * column + int((self.margin*2 + self.cell_w - self.Img_w)/2),(self.margin + self.cell_h) * row + int((self.margin*2 + self.cell_h - self.Img_h)/2)))
                else:
                   pygame.draw.rect(screen,
                                 color,
                                 [(self.margin + self.cell_w) * column + self.margin,
                                  (self.margin + self.cell_h) * row + self.margin,
                                  self.cell_w,
                                  self.cell_h])
                
        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
        
    
    def ResetGrid(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.grid[i][j]!=1:
                    self.grid[i][j]=0
        self.agent=Search_Agent(self.grid,self.start,self.goal)
        self.agent2=Corners_Problem(self.grid,self.start,self.goal)
        #self.frontiers,self.exploredStates=self.agent.init_dfs_bfs_1_step()
    def Launch(self):
        
        #goal=(size*2-1, size*2-1)
        
        assignment=self.grid
        step=0
        cell=(-1,-1)
        var_row=0
        value=-1
        screen = self.screen
       
        # Loop until the user clicks the close button.
        done = False
         
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        

        # -------- Main Program Loop -----------
        while not done:
            
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    #check for grid click
                    if (pos[0]<(self.w-3*self.margin) and (pos[1]>50)):
                        # Change the x/y screen coordinates to grid coordinates
                        column = pos[0] // (self.cell_w + self.margin)
                        row = (pos[1]-self.button_h) // (self.cell_h + self.margin)
                        
                        # Set that location to one
                        if self.grid[row][column] !=1:
                            self.grid[row][column] = 1
                        else:
                            self.grid[row][column] = -1
                        print("Click ", pos, "Grid coordinates: ", row, column)
                    else:   #check for button click
                        if self.IsButtonClicked(b_reset,pos):
                            self.ResetGrid()
                            self.DrawGrid()
                        elif self.IsButtonClicked(b_run_dfs,pos):                        
                            self.ResetGrid()
                            t1=time.time()
                            sol=self.agent.dfs()
                            exec_time=time.time()-t1                        
                            if sol!=False:                                
                                for state in sol[1]:    #color explored states
                                    i,j=state
                                    self.grid[i][j]=3
                                
                                i,j=self.start          #color solution states
                                self.grid[i][j]=2
                                for action in sol[0]:    
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=2
                                self.DrawGrid()
                            else:
                                print("no solution")
                            print("search time: ",exec_time)
                            
                        elif self.IsButtonClicked(b_run_bfs,pos):                           
                            self.ResetGrid()
                            t1=time.time()
                            sol=self.agent.bfs()
                            exec_time=time.time()-t1
                            if sol!=False:
                                for state in sol[1]:    #color explored states
                                    i,j=state
                                    self.grid[i][j]=3
                                
                                i,j=self.start          #color solution states
                                self.grid[i][j]=2
                                for action in sol[0]:    
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=2
                                self.DrawGrid()
                            else:
                                print("no solution")
                            print("search time: ",exec_time)
                        elif self.IsButtonClicked(b_run_ucs,pos):                           
                            self.ResetGrid()
                            t1=time.time()
                            
                            sol=self.agent.ucs()
                            exec_time=time.time()-t1
                            if sol!=False:
                                print("cost:",sol[2])
                                for state in sol[1]:    #color explored states
                                    i,j=state
                                    self.grid[i][j]=3
                                
                                i,j=self.start          #color solution states
                                self.grid[i][j]=2
                                for action in sol[0]:    
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=2
                                self.DrawGrid()
                            else:
                                print("no solution")
                            print("search time: ",exec_time)
                        elif self.IsButtonClicked(b_run_astar,pos):                           
                            self.ResetGrid()
                            t1=time.time()
                            sol=self.agent.astar("manhattan")
                            #sol=self.agent.astar("euclidean")
                            exec_time=time.time()-t1
                            if sol!=False:
                                print("cost:",sol[2])
                                for state in sol[1]:    #color explored states
                                    i,j=state
                                    self.grid[i][j]=3
                                
                                i,j=self.start          #color solution states
                                self.grid[i][j]=2
                                for action in sol[0]:    
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=2
                                self.DrawGrid()
                            else:
                                print("no solution")
                            print("search time: ",exec_time)
                        
                        elif self.IsButtonClicked(b_exe_sol,pos):
                            self.ResetGrid()
                            if sol!=False:
                                i,j=self.start
                                self.grid[i][j]=-1
                                for action in sol[0]:
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=-1
                                    self.DrawGrid((i,j))
                                   
                                    time.sleep(self.SPEED)

                        elif self.IsButtonClicked(b_run_corners_astar,pos):                           
                            self.ResetGrid()
                            t1=time.time()
                            sol=self.agent2.astar("manhattan")
                            #sol=self.agent.astar("euclidean")
                            exec_time=time.time()-t1
                            if sol!=False:
                                print("cost:",sol[2])
                                for state in sol[1]:    #color explored states
                                    i,j=state
                                    self.grid[i][j]=3
                                
                                i,j=self.start          #color solution states
                                self.grid[i][j]=2
                                for action in sol[0]:    
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=2
                                self.DrawGrid()
                            else:
                                print("no solution")
                            print("search time: ",exec_time)

                        
                        elif self.IsButtonClicked(b_run_corners_dfs,pos):                           
                            self.ResetGrid()
                            t1=time.time()
                            sol=self.agent2.dfs()
                            exec_time=time.time()-t1
                            if sol!=False:
                                for state in sol[1]:    #color explored states
                                    i,j=state
                                    self.grid[i][j]=3
                                
                                i,j=self.start          #color solution states
                                self.grid[i][j]=2
                                for action in sol[0]:    
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=2
                                self.DrawGrid()
                            else:
                                print("no solution")
                            print("search time: ",exec_time)

                        """
                        elif self.IsButtonClicked(b_run_corners_bfs,pos):                           
                            self.ResetGrid()
                            t1=time.time()
                            sol=self.agent2.dfs_bfs("bfs")
                            exec_time=time.time()-t1
                            if sol!=False:
                                for state in sol[1]:    #color explored states
                                    i,j=state[0]
                                    self.grid[i][j]=3
                                
                                i,j=self.start          #color solution states
                                self.grid[i][j]=2
                                for action in sol[0]:    
                                    if action=="n":
                                        i=i-1
                                    elif action=="w":
                                        j=j-1
                                    elif action=="s":
                                        i=i+1
                                    elif action=="e":
                                        j=j+1
                                    self.grid[i][j]=2
                                self.DrawGrid()
                            """
                        
                        
                        
                        """
                        elif self.IsButtonClicked(b_change_maze,pos):
                            self.m = Maze()
                            self.m.generator = Prims(int((self.num_rows-1)/2), int((self.num_cols-1)/2))
                            self.m.generate()
                            self.m.start = self.start
                            self.m.end = self.goal
                            self.grid=self.m.grid
                            print(self.grid)
                            self.ResetGrid()
                            self.DrawGrid()
                        """
            # Set the screen background
            screen.fill(self.GREY)
            
                                
                    
            b_w=self.button_w
            b_h=self.button_h
            b_x=self.w
            b_y=0
            b_y_margin=0
            b_gourp_margin=10
            
            b_reset=self.DrawButton(b_x,b_y,b_w,b_h,self.BLACK,"Reset")
            #b_next_dfs=self.DrawButton((b_x),b_y+b_h+b_y_margin+b_gourp_margin,b_w,b_h,self.RED,"1 step DFS")
            #b_sim_dfs=self.DrawButton((b_x),b_y+(2*(b_h+b_y_margin)+b_gourp_margin),b_w,b_h,self.GREEN,"sim DFS")
            b_run_dfs=self.DrawButton((b_x),b_y+(1*(b_h+b_y_margin)+b_gourp_margin),b_w,b_h,self.BLUE,"run DFS")
            
            #b_next_bfs=self.DrawButton((b_x),b_y+(4*(b_h+b_y_margin)+2*b_gourp_margin),b_w,b_h,self.RED,"1 step BFS")
            #b_sim_bfs=self.DrawButton((b_x),b_y+(5*(b_h+b_y_margin)+2*b_gourp_margin),b_w,b_h,self.GREEN,"sim BFS")
            b_run_bfs=self.DrawButton((b_x),b_y+(2*(b_h+b_y_margin)+2*b_gourp_margin),b_w,b_h,self.BLUE,"run BFS")
            
            b_run_ucs=self.DrawButton((b_x),b_y+(3*(b_h+b_y_margin)+3*b_gourp_margin),b_w,b_h,self.RED,"run UCS")
            
            b_run_astar=self.DrawButton((b_x),b_y+(4*(b_h+b_y_margin)+4*b_gourp_margin),b_w,b_h,self.RED,"run A*")
            
            b_run_corners_dfs=self.DrawButton((b_x),b_y+(9*(b_h+b_y_margin)+5*b_gourp_margin),b_w,b_h,self.RED,"Corners DFS")
            #b_run_corners_bfs=self.DrawButton((b_x),b_y+(10*(b_h+b_y_margin)+5*b_gourp_margin),b_w,b_h,self.GREEN,"Corners BFS")
            #b_run_corners_ucs=self.DrawButton((b_x),b_y+(11*(b_h+b_y_margin)+5*b_gourp_margin),b_w,b_h,self.BLUE,"Corners UCS")
            b_run_corners_astar=self.DrawButton((b_x),b_y+(12*(b_h+b_y_margin)+5*b_gourp_margin),b_w,b_h,self.YELLOW,"Corners A*")
            
            b_exe_sol=self.DrawButton((b_x),b_y+(5*(b_h+b_y_margin)+6*b_gourp_margin),b_w,b_h,self.GREEN,"EXE SOL")
            
            #b_change_maze=self.DrawButton((b_x),b_y+self.h-b_h,b_w,b_h,self.BLACK,"Change Maze")
            
            if self.init:
                self.DrawGrid()
                self.init=False
            
            # Limit to 60 frames per second
            clock.tick(60)
            
            
        
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()
        exit()
        



speed=0.01
width=1000
height=900
size=10
margin=0
start=(1,1)
goal=((size*2+1)-2, (size*2+1)-2)
maze=search_mazes.maze2
board=Board(start,goal,maze,size*2+1,size*2+1,width,height,speed,margin)
board.Launch()



