from pygame import Vector2

from wargame.engine import Engine
from wargame.scene import Scene
from wargame.nodes import GridMap


single_gridmap = GridMap(Vector2(0, 0), 5, 5, 50)
single_scene = Scene([single_gridmap])

engine = Engine(single_scene)
engine.loop()
