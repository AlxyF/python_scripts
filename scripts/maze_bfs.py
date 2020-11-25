import copy
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import multiprocessing
import time
import random
from tkinter import *

obstacles = ['W','w','#']

fig, axis, im, canvas = [],[],[],[]
maze_v = []

maze = "\n".join([
  "....w.....",
  "W...w..w..",
  "W...w..w..",
  "W...W..w..",
  ".......w..",
  "..W......."
])

maze = [list(x) for x in maze.split('\n')]
maze_size_x = len(maze)
maze_size_y = len(maze[0])
visited = copy.deepcopy(maze)

directions_x = [0, 1, 0 , -1]
directions_y = [1, 0, -1, 0]

start_x = 0
start_y = 0

end_x = maze_size_x - 1
end_y = maze_size_y - 1

window=Tk()
window.geometry("{0}x{1}".format(maze_size_x* 90, maze_size_y * 50 )) 
window.title('Maze Solver')

reached_exit = False
steps = 0

simulate = ""

def main():
    global fig, axis, im, maze_v, maze, simulate
    
    #Create a queue to share data between process
    q = multiprocessing.Queue()

    #Create the base plot
    visualize_init()
    path_finder_bfs()
    #Create and start the simulation process
    simulate=multiprocessing.Process(None,retrace_path,args=(q,))
    simulate.start()

    #Call a function to update the plot when there is new data
    visualize_update(q)

    window.mainloop()
    print ('Done')


def visualize_init():
    global fig, axis, im, maze_v, canvas
    for line in maze:
        row = []
        for c in line:
            if c in obstacles:
                row.append(0) # 
            else:
                row.append(1) # 
        maze_v.append(row)

    maze_v[start_x][start_y]= -1
    maze_v[end_x][end_y]= -2

    fig, axis = plt.subplots()                              
    im = axis.imshow(maze_v)   
    axis.set_xticks([]) 
    axis.set_yticks([]) 

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().place(x= -60,y= 20)  
    canvas.set_window_title('Maze')
    canvas.draw()
    

def visualize_update(q):
    global fig, im, canvas, window, axis, simulate
    
    try:    #Try to check if there is data in the queue
        result=q.get_nowait()

        if result !='Q':
            print (result)
            #here get crazy with the plotting, you have access to all the global variables that you defined in the plot function, and have the data that the simulation sent.
            
            im = axis.imshow(result)
    
            window.after(1000,visualize_update,q)
            canvas.draw()
        else:
            print ('done')
    except:
        window.after(500,visualize_update,q)
    


def path_finder_bfs():
    global fig, ax, im, maze_v, maze, maze_size, reached_exit, steps, visited

    queue_x = []
    queue_y = []

    steps = 0

    queue_x.append(start_x)
    queue_y.append(start_y)

    x = start_x
    y = start_y

    node_left = 1
    node_next = 0

    reached_exit = False

    def go_directions(x, y):
        nonlocal node_next, queue_x, queue_y
        for i in range(len(directions_x)):
            xx = x + directions_x[i]
            yy = y + directions_y[i]
            if     xx > maze_size_x - 1 \
                or yy > maze_size_y - 1 \
                or xx < 0 \
                or yy < 0 \
                or maze[xx][yy] in obstacles \
                or visited[xx][yy] == True:
                continue
            queue_x = [xx] + queue_x
            queue_y = [yy] + queue_y
            visited[xx][yy] = True
            
            node_next += 1

    while len(queue_x) > 0:
        x = queue_x.pop()
        y = queue_y.pop()
        maze[x][y] = steps
        visited[x][y] = True
        if x == end_x and y == end_y:
            reached_exit = True
        go_directions(x, y)
        node_left -= 1
        if node_left == 0:
            node_left = node_next
            node_next = 0
            if not reached_exit:
                steps += 1

    print("Reached exit: {} in steps: {}" .format(reached_exit, steps))
    return reached_exit

def retrace_path(q):
    global simulate
    maze_changed = copy.deepcopy(maze_v)
    x = end_x
    y = end_y

    if reached_exit == True:
        path = steps
        while path > 0:
            for i in range(len(directions_x)):
                xx = x + directions_x[i]
                yy = y + directions_y[i]
                if     xx > maze_size_x - 1 \
                    or yy > maze_size_y - 1 \
                    or xx < 0 \
                    or yy < 0 \
                    or maze[xx][yy] in obstacles:
                    continue
                if maze[xx][yy] == path - 1:
                    x = xx;
                    y = yy;
                    path -= 1
                    maze_changed[x][y] = -1
                    q.put(maze_changed)
    q.put('Q')
if __name__ == '__main__':
    main()