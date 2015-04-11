import gamestate as gs
import sys
import math

def closest(ent, entities):
    return min(entities, key=lambda x: dist(ent, x))

def dist(entity, other):
    # note this does not take wrap around into account
    return ((entity.x - other.x)**2 + (entity.y - other.y)**2)**(1.0/2)

def getAngle(entity, other):
    # gives the angle of the vector from entity to other
    # wrt to the positive x axis (but clockwise, counter intuitive but coords are upside down)
    # e.g.
    #               315
    #             .
    #           .
    #  180 . . x . . 0
    #           .
    #             .
    #               45
    x = other.x - entity.x
    y = other.y - entity.y
    return (math.degrees(math.atan2(y, x)) + 360) % 360
    

r = gs.Response()
state = gs.GameState()

while True:
    # get game state
    state.read()

    if(state.asteroids):
        close = closest(state.ship, state.asteroids)
        angle = getAngle(state.ship, close)
        thresh = 15
        if(state.ship.angle > angle):
            r.set_ccw()
        elif(state.ship.angle < angle):
            r.set_cw()

        r.set_fire(abs(state.ship.angle - angle) < thresh)


    r.set_thrust(False)

    # send command
    r.send()
