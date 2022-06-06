top=[]
def create_top_of_rooms():
    global top
    top=[[2,5,9,10],[1,1,1,1],[0,0,0,0]]
def restart_top_of_rooms():
    global top
    if top==[]:
        top=[[2,5,9,10],[1,1,1,1],[0,0,0,0]]
    else:
        for i in range (len(top[0])):
            top[2][i] = top[1][i]
            top[1][i] = 0
def get_top_of_rooms():
    global top
    return top
def update_top_of_rooms(room_id):
    global top
    t = 0
    for i in range (len(top[0])):
        if top[0][i] == room_id:
            top[1][i] += 1
            t = 1
    if t == 0:
        top[0].append(room_id)
        top[1].append(1)
        top[2].append(0)