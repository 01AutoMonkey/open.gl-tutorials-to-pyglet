open.gl-tutorials-to-pyglet
===========================

Translation of the http://open.gl/ OpenGL tutorials from C++ and SFML to Python and Pyglet

TODO:

- The first 5 parts of the tutorial are done, finish the remaining 3.
- Get the bug fix of euclid.py into the official repository.
- The texture comes out reversed in 5-1 and 5-2, fix it by altering the tex coordinates.

## Notes on translating from C++ and SFML to Python and Pyglet

The translation is done like so:
- C++ to Python and ctypes
- SFML to Pyglet
- GLEW to pyglet.gl
- SOIL to pyglet.image
- GLM to pyeuclid (there is a bug in the Matrix4.new_look_at method in the official version which has been fixed in the instance of it in this repository)

General notes:

- `from pyglet.gl import *` gives you access to OpenGL.
- To create GLfloat lists you just create an ordinary list and then multiply it like so: `(GLfloat * len(list1))(*list1)` , and same for GLuint: `(GLuint * len(elements))(*elements)`
- You sometimes need to use python ctypes: `from ctypes import *` , in terms of the open.gl tutorials you have to use pointer and sizeof for the C++ & and sizeof equivilants.
- Shader code is the same, you just put it in a string or in a seperate file, but to use it with `glShaderSource` you have to use the `cast` ctype, `pointer` and `POINTER` like so: `glShaderSource(fragmentShader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)`.
- Texture coordinates are reversed in pyglet.
- pyeuclid uses radians instead of degrees.
- To use the stencil buffer you have to enable it in the window config: `allowstencil = pyglet.gl.Config(stencil_size=8)` and `window = pyglet.window.Window(800, 600, "OpenGL", config=allowstencil)`