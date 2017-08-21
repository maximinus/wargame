# Wargame Engine

### A game engine for building tactical and strategy games.

The wargame engine is for building cross-platform 2D based tactical and strategy games.

It uses Pygame as it's input and rendering engine.

A tree of nodes is used as a viewport, with each node usually representing either a view of sprites, or the sprites themselves.

A messaging system is used to implement the nodes communicating with themselves, which allows for total seperation of systems, since a node does not have to know the details of the gfx, sound or other parts of the game code - it merely sends a message that is handled by some other part of the engine.

Other features include:

* A tween system for sprite animations.
* Builtin loaders for images, sounds and config files.
* A GUI system.
* Automatic game saving, loading and replays.
* A logging system to help pinpoint errors.
* A terminal to interact with any program whilst the code is running.
* Lots of example code.

Wargame-Engine is based on the principles of being *opinionated* and *flexible*. There are a number of standard defaults that are usually "sensible" but all of these can be over-ridden.

Wargame-Engine, unlike Pygame, is not a library. The main event loop is part of the engine and not implemented by the programmer. Similary, elements such as image loading are built into the engine, in a bid to reduce programmer work.

Some example code:

    # display a window with an image
    import os

    import wargame.engine
    from wargame.scene import scene
    from wargame.gui.nodes import GuiImage, VerticalContainer
    from wargame.gui.containers import window

    def game()
        # init the basic engine
        controller = wargame.engine(init(os.cwd()))

        # let's get the node we want to display - it's a simple image
        image = GuiImage.from_image('sprites.dog')

        # put that into a Window
        window = Window(image)

        # all nodes are part of a scene
        scene = Scene([window])

        # tell the engine we have a scene, and start it
        controller.add_scene('start', scene)
        controller.run('start')

    if __name__ == '__main__':
        game()

Wargame-Engine can be installed via pip locally after downloading this repository: see the README.md file in ./wargame/.

Wargame-Engine is currently a work in progress.
