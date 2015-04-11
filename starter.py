import gamestate as gs
import sys
import math

def closest(ent, entities):
    return min(entities, key=lambda x: dist(ent, x))

def dist(entity, other):
    # note this does not take wrap around into account
    return ((entity.x - other.x)**2 + (entity.y - other.y)**2)**(1/2)

def getAngle(entity, other):
    # needs adjusting
    x = entity.x - other.x
    y = entity.y - other.y
    return math.degrees(math.atan2(y, x))
    

r = gs.Response()
state = gs.GameState()

while True:
    # get game state
    state.read()

    close = closest(state.ship, state.asteroids)
    angle = getAngle(state.ship, close)
    #print >>sys.stderr, ((state.ship.x, state.ship.y), (close.x, close.y), angle(state.ship, close))

    # set command
    r.set_fire(False)
    r.set_thrust(False)
    r.set_no_turn()

    # send command
    r.send()
