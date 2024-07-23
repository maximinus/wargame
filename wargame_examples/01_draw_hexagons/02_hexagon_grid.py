from pygame import Vector2

from wargame.engine import Engine
from wargame.scene import Scene
from wargame.nodes import GridMap


single_gridmap = GridMap(Vector2(0, 0), 2, 2, 50)
single_scene = Scene([single_gridmap])

engine = Engine(single_scene)
engine.loop()
