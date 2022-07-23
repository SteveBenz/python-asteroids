# All sizes are basically a fraction of the size of the screen
class Sizes:
    PLAYER = 0.02
    BIG_ALIEN = 0.04
    SMALL_ALIEN = 0.02

    ASTEROID_BIG = 0.04
    ASTEROID_MEDIUM = 0.02
    ASTEROID_SMALL = 0.01

    LINE_DEBRIS = .003

class Balance:

    # In degrees per TICK
    TURN_RATE = 2

    # This is a cheesed form of deceleration.  It peels this fraction of the ship's speed off every TICK

    PLAYER_FRICTION = 0.995

    # This is in ScreenSize/tick/tick
    PLAYER_ACCELERATION_RATE = 0.00002

    # In units of ScreenSize
    PLAYER_BULLET_SPEED = 0.005
    ALIEN_BULLET_SPEED = 0.005

    # In units of ScreenSize/tick
    ALIEN_SPEED = .001

    ASTEROID_SPEED = 0.0005
    ASTEROID_BREAK_SPEED = .0003

    ASTEROIDS_IN_STARTING_WAVE = 8

    # Bullet lifetime in ticks
    BULLET_LIFETIME = 300

class Scoring:
    BIG_ALIEN = 300
    SMALL_ALIEN = 500
    ASTEROID_BIG = 10
    ASTEROID_MEDIUM = 15
    ASTEROID_SMALL = 20

class Colors:
    PLAYER_BULLET = (128,255,128)
    ALIEN_BULLET = (255,255,128)
    ALIEN_SHIP = (255,165,0)
    PLAYER_SHIP = (255,255,255)