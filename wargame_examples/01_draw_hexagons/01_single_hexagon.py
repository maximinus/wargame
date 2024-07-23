from wargame.engine import Engine
from wargame.scene import Scene
from wargame.nodes import GridMap
from wargame.nodes.tiles import Hexagon, Axial


single_hexagon = Hexagon(Axial(0, 0), 50)
single_gridmap = GridMap([single_hexagon])
single_scene = Scene([single_gridmap])

engine = Engine(single_scene)
engine.loop()
