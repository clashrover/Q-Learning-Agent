import numpy as np
import random

# north =1, east =2, south =3, west =4, no action = 0

def print_value(grid):
    for i in range(25):
        for j in range(50):
            print('%.1f'%grid[i][j][1], end = " ")
        print()
    print()
    print("-------------------------------------------")
    print()
    

def initialize_grid_world():
    grid = []
    for i in range(25):
        row = []
        for j in range(50):
            if i==0 or i==24 or j==0 or j==49:
                row.append(["wall",0,-1,"North"]) 
                # type of cell, value, reward upon landing on this cell
            elif j==48 and i==12:
                row.append(["cell",0,100,"North"])    
            elif ((j>=25 and j<=26) and (i<=11 or i>=13)):
                row.append(["wall",0,-1,"North"])
            else:
                row.append(["cell",0,0,"North"])

        grid.append(row)
        
    # grid[5][5][1]=100
    return grid

def solve_mdp(p,theta,y,run_length,grid,snapshot=[],anim_switch=0,use_criteria=1):
    grid_new = initialize_grid_world()
    animation_list  = []
    delta_list= []
    for k in range(run_length):
        delta = 0
        for i in range(25):
            for j in range(50):
                if i==0 or i==24 or j==0 or j==49:
                    continue    
                elif ((j>=25 and j<=26) and (i<=11 or i>=13)):
                    continue
                else:
                    v_north = 0
                    if(grid[i-1][j][0]=="wall"):
                        v_north += p * (grid[i-1][j][2]+ y*grid[i][j][1]) #north
                    else:
                        v_north += p * (grid[i-1][j][2]+ y*grid[i-1][j][1]) #north

                    if(grid[i][j+1][0]=="wall"):
                        v_north += ((1-p)/3) * (grid[i][j+1][2]+ y*grid[i][j][1]) #east
                    else:
                        v_north += ((1-p)/3) * (grid[i][j+1][2]+ y*grid[i][j+1][1]) #east

                    if(grid[i+1][j][0]=="wall"):
                        v_north += ((1-p)/3) * (grid[i+1][j][2]+ y*grid[i][j][1]) #south
                    else:
                        v_north += ((1-p)/3) * (grid[i+1][j][2]+ y*grid[i+1][j][1])
                    
                    if(grid[i][j-1][0]=="wall"):
                        v_north += ((1-p)/3) * (grid[i][j-1][2]+ y*grid[i][j][1]) #west
                    else:
                        v_north += ((1-p)/3) * (grid[i][j-1][2]+ y*grid[i][j-1][1])

                    v_east = 0
                    if(grid[i-1][j][0]=="wall"):
                        v_east += ((1-p)/3) * (grid[i-1][j][2]+ y*grid[i][j][1]) #north
                    else:
                        v_east += ((1-p)/3) * (grid[i-1][j][2]+ y*grid[i-1][j][1]) #north

                    if(grid[i][j+1][0]=="wall"):
                        v_east += p * (grid[i][j+1][2]+ y*grid[i][j][1]) #east
                    else:
                        v_east += p * (grid[i][j+1][2]+ y*grid[i][j+1][1]) #east

                    if(grid[i+1][j][0]=="wall"):
                        v_east += ((1-p)/3) * (grid[i+1][j][2]+ y*grid[i][j][1]) #south
                    else:
                        v_east += ((1-p)/3) * (grid[i+1][j][2]+ y*grid[i+1][j][1])
                    
                    if(grid[i][j-1][0]=="wall"):
                        v_east += ((1-p)/3) * (grid[i][j-1][2]+ y*grid[i][j][1]) #west
                    else:
                        v_east += ((1-p)/3) * (grid[i][j-1][2]+ y*grid[i][j-1][1])


                    v_south = 0
                    if(grid[i-1][j][0]=="wall"):
                        v_south += ((1-p)/3) * (grid[i-1][j][2]+ y*grid[i][j][1]) #north
                    else:
                        v_south += ((1-p)/3) * (grid[i-1][j][2]+ y*grid[i-1][j][1]) #north

                    if(grid[i][j+1][0]=="wall"):
                        v_south += ((1-p)/3) * (grid[i][j+1][2]+ y*grid[i][j][1]) #east
                    else:
                        v_south += ((1-p)/3) * (grid[i][j+1][2]+ y*grid[i][j+1][1]) #east

                    if(grid[i+1][j][0]=="wall"):
                        v_south += p * (grid[i+1][j][2]+ y*grid[i][j][1]) #south
                    else:
                        v_south += p * (grid[i+1][j][2]+ y*grid[i+1][j][1])
                    
                    if(grid[i][j-1][0]=="wall"):
                        v_south += ((1-p)/3) * (grid[i][j-1][2]+ y*grid[i][j][1]) #west
                    else:
                        v_south += ((1-p)/3) * (grid[i][j-1][2]+ y*grid[i][j-1][1])

                    v_west = 0
                    if(grid[i-1][j][0]=="wall"):
                        v_west += ((1-p)/3) * (grid[i-1][j][2]+ y*grid[i][j][1]) #north
                    else:
                        v_west += ((1-p)/3) * (grid[i-1][j][2]+ y*grid[i-1][j][1]) #north

                    if(grid[i][j+1][0]=="wall"):
                        v_west += ((1-p)/3) * (grid[i][j+1][2]+ y*grid[i][j][1]) #east
                    else:
                        v_west += ((1-p)/3) * (grid[i][j+1][2]+ y*grid[i][j+1][1]) #east

                    if(grid[i+1][j][0]=="wall"):
                        v_west += ((1-p)/3) * (grid[i+1][j][2]+ y*grid[i][j][1]) #south
                    else:
                        v_west += ((1-p)/3) * (grid[i+1][j][2]+ y*grid[i+1][j][1])
                    
                    if(grid[i][j-1][0]=="wall"):
                        v_west += p * (grid[i][j-1][2]+ y*grid[i][j][1]) #west
                    else:
                        v_west += p * (grid[i][j-1][2]+ y*grid[i][j-1][1])

                    
                    mxv = max(v_north,v_east,v_south,v_west)
                    grid_new[i][j][0] = grid[i][j][0]
                    grid_new[i][j][1] = mxv
                    grid_new[i][j][2] = grid[i][j][2]
                    if(mxv==v_north):
                        grid_new[i][j][3] = "North"
                    elif mxv==v_east:
                        grid_new[i][j][3] = "East"
                    elif mxv==v_south:
                        grid_new[i][j][3] = "South"
                    elif mxv==v_west:
                        grid_new[i][j][3] = "West"

                    delta = max(delta, abs(grid[i][j][1]-mxv))
        
        for i in range(25):
            for j in range(50):
                grid[i][j][0] = grid_new[i][j][0]
                grid[i][j][1] = grid_new[i][j][1]
                grid[i][j][2] = grid_new[i][j][2]
                grid[i][j][3] = grid_new[i][j][3]
                
        
        # if(k==19 or k==49 or k==99):
            # plot_grid(grid)
        
        g = []
        for i in range(25):
            g1 = []
            for j in range(50):
                g1.append(grid[i][j][1])
            g.append(g1)

        m = np.max(g)
        g=(g/m)*255
        
        animation_list.append(g)
        if(anim_switch==1):
            plot_grid(grid,switch=1)

        # taking snapshots
        for i in snapshot:
            if k==i:
                plot_grid(grid,switch=1)

        delta_list.append(delta)
        if delta<theta and use_criteria==1:
            # print(delta)
            break

    return animation_list, delta_list
                     


def plot_grid(grid,switch=0, path=[], state_vc=[]):

    # Draw the board ------------------------------------
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 6))

    for i in range(25):
        plt.axhline(i+0.5, lw=0.2, color='w', zorder=5)

    for i in range(50):
        plt.axvline(i+0.5, lw=0.2, color='w', zorder=5)

    plt.axis('off')
    plt.plot([0.5,0.5],[0.5,23.5], color = 'r',lw=1.5)
    plt.plot([48.5,48.5],[0.5,23.5], color = 'r',lw=1.5)
    plt.plot([0.5,48.5],[0.5,0.5], color = 'r',lw=1.5)
    plt.plot([0.5,48.5],[23.5,23.5], color = 'r',lw=1.5)
    plt.plot([24.5,26.5],[11.5,11.5],color = 'r',lw=1.5)
    plt.plot([24.5,26.5],[12.5,12.5],color = 'r',lw=1.5)
    plt.plot([24.5,24.5],[0.5,11.5],color = 'r',lw=1.5)
    plt.plot([24.5,24.5],[12.5,23.5],color = 'r',lw=1.5)
    plt.plot([26.5,26.5],[0.5,11.5],color = 'r',lw=1.5)
    plt.plot([26.5,26.5],[12.5,23.5],color = 'r',lw=1.5)

    plt.plot([47.5,48.5],[11.5,11.5],color = 'g',lw=3)
    plt.plot([47.5,48.5],[12.5,12.5],color = 'g',lw=3)
    plt.plot([47.5,47.5],[11.5,12.5],color = 'g',lw=3)
    plt.plot([48.5,48.5],[11.5,12.5],color = 'g',lw=3)

    #-------------------------------------------------------

    if len(state_vc)>0:
        m1 = np.max(state_vc)
        m2 = np.min(state_vc)
        for i in range(25):
            for j in range(50):
                state_vc[i][j] = (state_vc[i][j]-m2)/(m1-m2)
                state_vc[i][j] = state_vc[i][j]*255
        

        plt.imshow(state_vc,cmap='gray', vmin=0, vmax=255)

        plt.colorbar(orientation='vertical')
        plt.show()
        return

    g = []
    for i in range(25):
        g1 = []
        for j in range(50):
            g1.append(grid[i][j][1])
        g.append(g1)
    
    m1 = np.max(g)
    m2 = np.min(g)
    for i in range(25):
        for j in range(50):
            g[i][j] = (g[i][j]-m2)/(m1-m2)
            g[i][j] = g[i][j]*255
    
    

    plt.imshow(g,cmap='gray', vmin=0, vmax=255)
    
    if switch == 1:
        for i in range(25):
            for j in range(50):
                if i==0 or i==24 or j==0 or j==49:
                    continue    
                elif ((j>=25 and j<=26) and (i<=11 or i>=13)):
                    continue
                else:
                    action = grid[i][j][3]
                    if(action=="North"):
                        drawNorth(j,i,plt)
                    elif action == "East":
                        drawEast(j,i,plt)
                    elif action == "South":
                        drawSouth(j,i,plt)
                    else:
                        drawWest(j,i,plt)
    # plt. scatter(1,23)

    if len(path)>0:
        x =[]
        y = []
        for p in path:
            x.append(p[0])
            y.append(24-p[1])
        plt.plot(x,y,color='r',lw=2)
    
    plt.show()
    


def drawEast(x,y,plt):
    plt.plot([x-0.25,x+.25],[y,y],color = 'b',lw=1)
    plt.plot([x+0.125,x+0.25],[y+0.25,y],color = 'b',lw=1)
    plt.plot([x+0.125,x+0.25],[y-0.25,y],color = 'b',lw=1)

def drawWest(x,y,plt):
    plt.plot([x-0.25,x+.25],[y,y],color = 'b',lw=1)
    plt.plot([x-0.125,x-0.25],[y+0.25,y],color = 'b',lw=1)
    plt.plot([x-0.125,x-0.25],[y-0.25,y],color = 'b',lw=1)

def drawSouth(x,y,plt):
    plt.plot([x,x],[y-0.25,y+.25],color = 'b',lw=1)
    plt.plot([x+0.25,x],[y+0.125,y+0.25],color = 'b',lw=1)
    plt.plot([x-0.25,x],[y+0.125,y+0.25],color = 'b',lw=1)

def drawNorth(x,y,plt):
    plt.plot([x,x],[y-0.25,y+.25],color = 'b',lw=1)
    plt.plot([x+0.25,x],[y-0.125,y-0.25],color = 'b',lw=1)
    plt.plot([x-0.25,x],[y-0.125,y-0.25],color = 'b',lw=1)


def plot_animation(g):
    imagelist = g

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    fig = plt.figure(figsize=(12, 6))
    plt.axis('off')
    im = plt.imshow(imagelist[0], cmap='gray', vmin=0, vmax=255)

    # function to update figure
    def updatefig(j):
        # set the data in the axesimage object
        im.set_array(imagelist[j])
        # return the artists set
        return [im]
        
    ani = animation.FuncAnimation(fig, updatefig, frames=range(len(g)), 
                                interval=200, blit=True)
    
    # plt.colorbar(orientation='vertical')
    plt.show()
    # Writer = animation.writers['ffmpeg']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    # ani.save('mdp_y_0p9.mp4', writer=writer)

def get_next_pos(pos,grid):
    policy_action = grid[24-pos[1]][pos[0]][3]
    r = random.uniform(0,1)
    next_pos = None
    action = None
    la = ["North","East","West","South"]
    la.remove(policy_action)

    if(r<=0.8):
        action = policy_action
    elif (r<=(0.8+(0.2/3))):
        action = la[0]
    elif (r<=(0.8+(0.4/3))):
        action = la[1]
    elif (r<=1):
        action = la[2]
    
    if(action == "North"):
        next_pos = (pos[0],pos[1]+1)
    
    elif action == "South":
        next_pos = (pos[0],pos[1]-1)
    
    elif action == "East":
        next_pos = (pos[0]+1,pos[1])
    
    elif action == "West":
        next_pos = (pos[0]-1,pos[1])
    
    if grid[24-next_pos[1]][next_pos[0]][0] == "wall":
        next_pos = (pos[0],pos[1])
    
    # print(action)
    return next_pos


def sample_execution(grid,init_pos,l):
    count_grid = []
    for i in range(25):
        cg = []
        for j in range(50):
            cg.append(0)
        count_grid.append(cg)
    
    path = [init_pos]
    pos = init_pos
    count_grid[24-pos[1]][pos[0]]+=1
    for i in range(l):
        pos = get_next_pos(pos,grid)
        path.append(pos)
        count_grid[24-pos[1]][pos[0]]+=1
        if pos[0]==48 and pos[1]==12:
            break
        # print(pos)
    
    return path,count_grid

def plot_delta(delta_list):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 6))
    x=[]
    for i in range(1,len(delta_list)+1):
        x.append(i)
    plt.plot(x,delta_list)
    plt.show()

def main():
    prob_intention = 0.8 # probability of intentional action
    theta = 0.1
    y=0.01
    run_length=100

    #part 1
    grid = initialize_grid_world()
    
    animation_list, delta_list =  solve_mdp(prob_intention,theta,y,run_length,grid,use_criteria=0)
    # plot_animation(animation_list)
    plot_grid(grid,switch=1)
    # print_value(grid)
    
    #part 2
    y=0.99
    grid1 = initialize_grid_world()

    animation_list1, delta_list1 = solve_mdp(prob_intention,theta,y,run_length,grid1,snapshot=[19,49,99])
    # plot_grid(grid1,switch=1)
    
    #part 3_1
    episode_length = 200
    init_pos = (1,1)
    sample_path,count_grid = sample_execution(grid1, init_pos,episode_length)
    plot_grid(grid1,switch=1,path=sample_path)

    # part 3_2
    count_grid = []
    for i in range(25):
        cg = []
        for j in range(50):
            cg.append(0)
        count_grid.append(cg)
    
    for k in range(200):
        init_pos = (1,1)
        sample_path,cg = sample_execution(grid1, init_pos,episode_length)
    
        for i in range(25):
            for j in range(50):
                count_grid[i][j]+= cg[i][j]

    # for row in count_grid:
    #     for col in row:
    #         print("{: >5}".format(col), end="")
    #     print()

    plot_grid(grid1,state_vc = count_grid)
    

    # part 4
    plot_delta(delta_list1)
    y=0.01
    grid1 = initialize_grid_world()

    animation_list1, delta_list1 = solve_mdp(prob_intention,theta,y,run_length,grid1)
    plot_delta(delta_list1)
    # plot_grid(grid1,switch=1)
    

main()