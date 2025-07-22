import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

#define the 2x2 enviornment 

envioronment = {
    "Room1":"Clean",
    "Room2":"Dirty",
    "Room3":"Clean",
    "Room4":"Clean"
}

#mapping  for grid postions
room_positions={
    "Room1":(0,1),
    "Room2":(1,1),
    "Room3":(0,0),
    "Room4":(1,0)
}

rooms=list(envioronment.keys())
agent_index=0


def reflex_agent(state):
    if state=="Dirty":
        return "Clean"
    else:
        return "Move"
    
def draw_enviornment(env,agent_pos,step):
    fig,ax=plt.subplots()
    ax.set_xlim(0,2)
    ax.set_ylim(0,2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Step {step} - Agent in {rooms[agent_pos]}")
    
    for room,pos in room_positions.items():
        x,y=pos
        color='red' if env[room]=="Dirty" else 'green'
        rect=patches.Rectangle((x,y),1,1,facecolor=color,edgecolor='black')
        ax.add_patch(rect) 
        ax.text(x+0.5,y+0.5,room,ha='center',va='center',color='white')
    #draw agent
    agent_x,agent_y=room_positions[rooms[agent_pos]]
    agent_patch=patches.Circle((agent_x+0.5,agent_y+0.5),0.1,color='blue')
    ax.add_patch(agent_patch)
    
    plt.pause(1)     
    plt.close()     
#Run simulation


plt.ion()
steps=8

for step in range(steps):
    current_room=rooms[agent_index]
    state=envioronment[current_room]
    action= reflex_agent(state)
    
    draw_enviornment(envioronment,agent_index,step+1)
    
    if action =="Clean":
        envioronment[current_room]='Clean'
    else:
        agent_index=(agent_index+1)%len(rooms)
        
plt.ioff()
print("✅ Simulation Complete")            