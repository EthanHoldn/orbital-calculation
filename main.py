import math
import matplotlib.pyplot as plt

#
# All units are in meters, meters per second, or kilograms unless otherwise stated
#

#position of the moon in terms of the angle relative to earth in degrees
moon_a = 0

#list of orbital bodies
# "cord" is the x and y coordinates
# "gm" is the mass of the body in terms of the gravitational constant (kg*6.6743e-11)
# "r" is the radius. it is used for collision detection.
bodies = {"earth":{
            "cord":[0,0],
            "gm":3.986004418e14, 
            "r":6378140},
         "moon":{
            "cord":[math.cos(math.radians(moon_a))*384400000*1,math.sin(math.radians(moon_a))*384400000*1],
            "gm":4.90405745e12,
            "r":1737000}
        }
#initial position of the satellite
# "cord" is the x and y coordinates
# "v" is the velocity vector in terms of the x and y component
satellite = {"cord":[-6.378e6-80000,0],"v":[0,11004.3]}

# list of coordinates to plot the path of satellite (in kilometers)
plot_x=[]
plot_y=[]

stop = False
i = 0 #seconds since start of simulation

#does actual simulation; each simulation step is 1 second
while not stop:
    #calculates lunar orbit
    if False:
        moon_a += 0.000152502257033
        bodies["moon"]["cord"] = [math.cos(math.radians(moon_a))*384400000,math.sin(math.radians(moon_a))*384400000]

    #pull_vec is the gravitational pull on the satellite in terms of an x and y vector
    pull_vec = [0,0]

    #calculates physics for each body
    for name in bodies:
        body = bodies[name]

        #collision detection
        if math.dist(body["cord"],satellite["cord"]) < body["r"]: 
            stop = True
            print(i)
            plot_x.append(int(satellite["cord"][0])/1000)
            plot_y.append(int(satellite["cord"][1])/1000)
            break

        #calculate the pull of gravity
        pull_force = body["gm"]/math.dist(body["cord"],satellite["cord"])**2
        #calculate the direction of the pull
        pull_heading = math.atan2(body["cord"][1]-satellite["cord"][1],body["cord"][0]-satellite["cord"][0])
        #changes the directional vector to an x and y vector and adds it to the gravitational pulls of the other bodies
        pull_vec = [pull_vec[0]+(math.cos(pull_heading)*pull_force),pull_vec[1]+(math.sin(pull_heading)*pull_force)]

    #net_vec is the sum of gravitational pull and the velocity of the satellite
    net_vec = [pull_vec[0]+satellite["v"][0],pull_vec[1]+satellite["v"][1]]
    satellite["v"] = net_vec

    #add the net_vec to the satellites position
    satellite["cord"] = [satellite["cord"][0] + net_vec[0],satellite["cord"][1] + net_vec[1]]

    #stops the simulation after a specified number of seconds
    if i > 10000000:
        stop = True
        print(i)
        plot_x.append(int(satellite["cord"][0])/1000)
        plot_y.append(int(satellite["cord"][1])/1000)
        break

    #adds the current position to the path every 60 seconds
    if i%60 ==0: 
        plot_x.append(int(satellite["cord"][0])/1000)
        plot_y.append(int(satellite["cord"][1])/1000)

    i+=1

#removes points that dont add that much detail to the path
#if the line is strait-ish remove points
i = 2
while i < len(plot_y)-1:
    a1 = math.degrees(math.atan2(plot_y[i-1]-plot_y[i-2],plot_x[i-1]-plot_x[i-2]))
    a2 = math.degrees(math.atan2(plot_y[i]-plot_y[i-1],plot_x[i]-plot_x[i-1]))
    a3 = math.degrees(math.atan2(plot_y[i+1]-plot_y[i],plot_x[i+1]-plot_x[i]))
    da1 = abs(a1-a2)
    da2 = abs(a2-a3)
    if da1 < .5 and da2 < .5:
        plot_y.pop(i)
        plot_x.pop(i)
    else:
        i +=1

#creates a text file of satellite path as a list of coordinates separated by a space
f=open("plot.txt","w")
for i in range(len(plot_x)):
    f.write(str(int(plot_x[i]))+" "+str(int(plot_y[i]))+"\n")
f.close()

#plots the path of the satellite
#keep the scale of the x and y axis the same to prevent distortion
plt.plot(plot_x,plot_y)
plt.gca().set_aspect('equal', adjustable='box')
#plot the earth in km
plt.gca().add_artist(plt.Circle((0,0),6378,fill=False))
#plot the moon in km
plt.gca().add_artist(plt.Circle((bodies["moon"]["cord"][0]/1000,bodies["moon"]["cord"][1]/1000),1737,fill=False))
plt.show()
