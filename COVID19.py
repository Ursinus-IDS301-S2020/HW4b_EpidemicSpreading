"""
Programmer: Chris Tralie
Purpose: To create a simple Monte Carlo simulation of a
spreading epidemic, using only arrays, methods, and loops.  A bunch
of people are placed uniformly at random on a square grid, and a single
one of them starts off infected.  Points that are moving then take
a random walk
"""
from vpython import *
import numpy as np
import matplotlib.pyplot as plt
import time

INFECTED = 0
UNINFECTED = 1
RECOVERED = 2
STATE_COLORS = [vector(1, 0, 0), vector(0, 0.5, 1), vector(1, 0, 1)]


def update_infections(X, states, time_sick, recovery_time, dist):
    """

    Parameters
    ----------
    X: ndarray(num_people, 2)
        An array of the positions of each person, with the x coordinate in the
        first column and the coordinate in the second column
    states: ndarray(num_people)
        A 1D array of all of the states
    time_sick: ndarray(num_people)
        The number of hours each person has been sick
    recovery_time: int
        The number of hours it takes an infected person to recover
    dist: float
        The distance an uninfected person has to be to an infected
        person in both the x and y coordinate to infect them
    """
    num_people = X.shape[0]
    ## TODO: Fill this in
    # Loop through the people, and apply the following rules:
    # 1) If a person is UNINFECTED but is within "dist" in its x coordinate
    #    and its y coordinate of an INFECTED person, their state changes to
    #    INFECTED
    # 2) If a person is INFECTED, add one hour to the amount of time
    #    that they have been infected in the timeSick array.  If they
    #    have been infected for recovery_time amount of time, then change
    #    their state to RECOVERED


def draw_points(cylinders, T, X, states, hour, res):
    """
    Parameters
    ----------
    cylinders: list of vpython clinder
        Cylinder markers for each person
    T: vpython text
        Text that's used to display the day
    X: ndarray(num_people, 2)
        An array of the positions of each person, with the x coordinate in the
        first column and the coordinate in the second column
    states: ndarray(num_people)
        A 1D array of all of the states
    hour: int
        The hour it is in the simulation
    res: int
        The size of the grid
    """
    for i in range(X.shape[0]):
        cylinders[i].pos = vector(X[i, 0]-res/2, 0, X[i, 1]-res/2)
        cylinders[i].color = STATE_COLORS[states[i]]
    T.text = "\n\nDay %i"%(hour/24)


def do_random_walks(X, is_moving, res):
    """
    Do a random walk on each point that's moving
    
    Parameters
    ----------
    X: ndarray(N, 2)
        An array of locations
    is_moving: ndarray(N)
        An array of booleans indicating whether each person is moving or not
    res: int
        The size of the grid
    """
    choices = np.random.randint(0, 4, X.shape[0])
    X[(choices == 0)*(is_moving == 1), 0] += 1 # Right
    X[(choices == 1)*(is_moving == 1), 0] -= 1 # Left
    X[(choices == 2)*(is_moving == 1), 1] += 1 # Up
    X[(choices == 3)*(is_moving == 1), 1] -= 1 # Down
    # Keep things in the square
    X[X < 0] = 0
    X[X >= res] = res


def simulate_pandemic(num_people, num_moving, num_hours, res, recovery_time, draw):
    """
    Parameters
    ----------
    num_people: int
        The number of people in the simulation
    num_moving: int
        The number of people who are moving
    num_hours: int
        The total number of hours in the simulation
    res: int
        The size of the grid
    recovery_time: int
        The number of hours it takes an infected person to recover
    draw: boolean
        If true, show the animation in vpython.  If false, simply
        run the animation and display plots of the people in different
        states over time
    """
    # Step 1: Setup initial positions of all people, initialize
    # the amount of time they've all been sick to zero, and set
    # them all to not be sick by default
    # Also set the first "num_moving" people to be moving, and the
    # rest to be stationary
    X = np.random.randint(0, res, (num_people, 2))
    states = np.ones(num_people, dtype=int)*UNINFECTED
    states[0] = INFECTED # Setup the first infection
    time_sick = np.zeros(num_people) # The time a person has been sick
    is_moving = np.ones(num_people)
    if num_moving < num_people:
        is_moving[num_moving::] = 0
    
    #Arrays for holding the results
    infected_count = np.zeros(num_hours)
    uninfected_count = np.zeros(num_hours)
    recovered_count = np.zeros(num_hours)

    # Step 2: Setup vpython for drawing
    cylinders = []
    T = None
    if draw:
        scene = canvas(title='Epidemic Simulation %i People %i Moving'%(num_people, num_moving),
            width=600, height=600) 
        for i in range(num_people):
            c = cylinder(pos=vector(X[i, 0]-res/2, 0, X[i, 1]-res/2), axis=vector(0, 8, 0), radius=0.5, color=STATE_COLORS[states[i]])
            cylinders.append(c)
        scene.camera.pos = vector(-res*0.07, res*0.84, res*0.54)
        scene.camera.axis = -scene.camera.pos
        # This text will store the elapsed time
        T = wtext(text='')
    
    
    # Step 3: Run the Monte Carlo Simulation
    for hour in range(num_hours):
        if draw:
            draw_points(cylinders, T, X, states, hour, res)
            time.sleep(1.0/24)
        do_random_walks(X, is_moving, res)
        update_infections(X, states, time_sick, recovery_time, 2)
        # Update counts for this hour
        infected_count[hour] = np.sum(states == INFECTED)
        uninfected_count[hour] = np.sum(states == UNINFECTED)
        recovered_count[hour] = np.sum(states == RECOVERED)

    # Plot the results
    plt.figure(figsize=(8, 5))
    days = np.arange(num_hours)/24
    plt.plot(days, uninfected_count)
    plt.plot(days, infected_count)
    plt.plot(days, recovered_count)
    plt.legend(["Uninfected", "Infected", "Recovered"])
    plt.xlabel("Day")
    plt.ylabel("Number of People")
    plt.title("Epidemic Simulation %i People, %.3g%s Moving, %i x %i Grid"%(num_people, num_moving*100.0/num_people, "%", res, res))
    plt.show()
    

num_people = 1000
num_moving = num_people
num_hours = 24*120
res = 200
recovery_time = 24*14
draw = True
simulate_pandemic(num_people, num_moving, num_hours, res, recovery_time, draw)