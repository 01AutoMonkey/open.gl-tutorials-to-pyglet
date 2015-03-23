# Tutorial: https://open.gl/context
# Original Sample Code: ...

import pyglet
from pyglet.gl import *

window = pyglet.window.Window(800, 600, "OpenGL")
window.set_location(100, 100)

@window.event
def on_draw():
    pass

@window.event
def on_key_press(symbol, modifiers):
    pass

@window.event
def on_key_release(symbol, modifiers):
    print symbol

def update(dt):
    pass
pyglet.clock.schedule(update)

pyglet.app.run()
