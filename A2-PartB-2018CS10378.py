# A=0,1,2,3 or North,East,South,West
import random
import numpy as np

def initialize_grid_world():
    grid = []
    for i in range(25):
        row = []
        for j in range(50):
            if i==0 or i==24 or j==0 or j==49:
                row.append([-1,[0,0,0,0]]) 
                # reward upon landing on this cell, q values
            elif j==48 and i==12:
                row.append([100,[0]]) # only stay action possible at goal state    
            elif ((j>=25 and j<=26) and (i<=11 or i>=13)):
                row.append([-1,[0,0,0,0]])
            else:
                l = [10*random.uniform(0,1),10*random.uniform(0,1),10*random.uniform(0,1),10*random.uniform(0,1)]
                row.append([0,l])

        grid.append(row)
        
    return grid

def chooseAction(grid,pos,epsilon):
    r = random.uniform(0,1)
    if(r<=epsilon):
        a = random.randint(0,3)
        return a
    
    l = grid[24-pos[1]][pos[0]][1]
    # print(l)
    a = l.index(max(l))
    # print(a)
    return a

def applyAction(pos,A,grid):
    next_pos = None
    x = random.uniform(0,1)
    if A ==0:
        if (x<=0.8):
            next_pos = (pos[0],pos[1]+1)
        elif x<= (0.8+(0.2/3)):
            next_pos = (pos[0]+1,pos[1])
        elif x<= (0.8+(0.4/3)):
            next_pos = (pos[0],pos[1]-1)
        else:
            next_pos = (pos[0]-1,pos[1])
    if A ==1:
        if (x<=0.8):
            next_pos = (pos[0]+1,pos[1])
        elif x<= (0.8+(0.2/3)):
            next_pos = (pos[0],pos[1]+1)
        elif x<= (0.8+(0.4/3)):
            next_pos = (pos[0],pos[1]-1)
        else:
            next_pos = (pos[0]-1,pos[1])
    if A ==2:
        if (x<=0.8):
            next_pos = (pos[0],pos[1]-1)
        elif x<= (0.8+(0.2/3)):
            next_pos = (pos[0]+1,pos[1])
        elif x<= (0.8+(0.4/3)):
            next_pos = (pos[0],pos[1]+1)
        else:
            next_pos = (pos[0]-1,pos[1])
    if A ==3:
        if (x<=0.8):
            next_pos = (pos[0]-1,pos[1])
        elif x<= (0.8+(0.2/3)):
            next_pos = (pos[0]+1,pos[1])
        elif x<= (0.8+(0.4/3)):
            next_pos = (pos[0],pos[1]-1)
        else:
            next_pos = (pos[0],pos[1]+1)
    
            
    r=grid[24-next_pos[1]][next_pos[0]][0]
    if r==-1:
        next_pos = (pos[0],pos[1])
    
    return next_pos,r
        

def q_learn(grid,y,alpha,epsilon,num_epsiodes,episode_length):
    count=0
    animation_list = []
    reward_list = []
    for k in range(num_epsiodes):
        reward_sum=0
        pos = (random.randint(1,48),random.randint(1,23))
        while((pos[0]<=26 and pos[0]>=25) and (pos[1]<=11 or pos[1]>=13)) or (pos[0]==48 and pos[1]==12) :
            pos = (random.randint(1,48),random.randint(1,23))
        
        if (pos[0]==0 or pos[0]==49 or pos[1]==0 or pos[1]==24) or (pos[0]==48 and pos[1]==12) or (pos[0]>=25 and pos[0]<=26 and (pos[1]<=11 or pos[1]>=13)):
            print("error in init pos of episode")

        for i in range(episode_length):
            # print(pos)
            A = chooseAction(grid,pos,epsilon)
            # A=1,2,3,4 or North,East,South,West
            next_pos,r = applyAction(pos,A,grid) #remember transition prob
            
            v = max(grid[24-next_pos[1]][next_pos[0]][1])
            v1 = grid[24-pos[1]][pos[0]][1][A]

            grid[24-pos[1]][pos[0]][1][A] = v1 + alpha*((r+y*v)-v1) 

            pos = (next_pos[0],next_pos[1])

            reward_sum+=r
            if pos[0]==48 and pos[1]==12:
                # count+=1
                break

        
        # if(k<1000):
        reward_list.append(reward_sum)

        if k%10 == 0:
            # reward_list.append(reward_sum)

            g = []
            for i in range(25):
                g1 = []
                for j in range(50):
                    v = max(grid[i][j][1])
                    g1.append(v)
                    # print('%.1f'%v,end=" ")
                # print()
                g.append(g1)
            
            m1 = np.max(g)
            m2 = np.min(g)
            for i in range(25):
                for j in range(50):
                    g[i][j] = (g[i][j]-m2)/(m1-m2)
                    g[i][j] = g[i][j]*255
            
            
            animation_list.append(g)

    # print(count)
    return animation_list, reward_list


def plot_grid(grid,switch=0):
    g = []
    for i in range(25):
        g1 = []
        for j in range(50):
            v = max(grid[i][j][1])
            g1.append(v)
            # print('%.1f'%v,end=" ")
        # print()
        g.append(g1)
    
    m1 = np.max(g)
    m2 = np.min(g)
    for i in range(25):
        for j in range(50):
            g[i][j] = (g[i][j]-m2)/(m1-m2)
            g[i][j] = g[i][j]*255
    
    
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 6))
    plt.imshow(g,cmap='gray', vmin=0, vmax=255)
    # plt.colorbar(orientation='vertical')
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
    
    if switch == 1:
        for i in range(25):
            for j in range(50):
                if i==0 or i==24 or j==0 or j==49:
                    continue    
                elif ((j>=25 and j<=26) and (i<=11 or i>=13)):
                    continue
                elif j==48 and i==12:
                    continue
                else:
                    l = grid[i][j][1]
                    action = l.index(max(l))
                    if(action==0):
                        drawNorth(j,i,plt)
                    elif action == 1:
                        drawEast(j,i,plt)
                    elif action == 2:
                        drawSouth(j,i,plt)
                    else:
                        drawWest(j,i,plt)
    # plt. scatter(1,23)
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
                                interval=50, blit=True)
    
    # plt.colorbar(orientation='vertical')
    plt.show()
    # Writer = animation.writers['ffmpeg']
    # writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    # ani.save('ql_e_0p5.mp4', writer=writer)

def plot_reward(reward_list):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(12, 6))
    plt.plot(reward_list)
    plt.show()

def main():
    y=0.99
    alpha = 0.25
    epsilon = 0.05
    num_epsiodes = 4000
    episode_length = 1000
    
    grid = initialize_grid_world()

    animation_list, reward_list = q_learn(grid,y,alpha,epsilon,num_epsiodes,episode_length)

    plot_grid(grid,switch=1)

    # plot_animation(animation_list)

    plot_reward(reward_list)

    epsilon = 0.005
    
    grid = initialize_grid_world()

    animation_list, reward_list = q_learn(grid,y,alpha,epsilon,num_epsiodes,episode_length)

    plot_grid(grid,switch=1)

    # plot_animation(animation_list)

    plot_reward(reward_list)

    epsilon = 0.5
    
    grid = initialize_grid_world()

    animation_list, reward_list = q_learn(grid,y,alpha,epsilon,num_epsiodes,episode_length)

    plot_grid(grid,switch=1)

    # plot_animation(animation_list)

    plot_reward(reward_list)


main()