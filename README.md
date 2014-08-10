open.gl-tutorials-to-pyglet
===========================

Translation of the http://open.gl/ OpenGL tutorials from C++ and SFML to Python and Pyglet

TODO:

- The first 5 parts of the tutorial are done, finish the remaining 3.
- Get the bug fix of euclid.py into the official repository.
- The texture comes out reversed in 5-1 and 5-2, fix it by altering the tex coordinates.

## Notes on translating from C++ and SFML to Python and Pyglet

More specifically the translation happens like so:
- C++ to Python and ctypes
- SFML to Pyglet
- GLEW to pyglet.gl
- SOIL to pyglet.image
- GLM to pyeuclid (there is a bug in the `Matrix4.new_look_at` method in the official version, use the version in this repository until the patch goes upstream)

General notes:

- `from pyglet.gl import *` gives you access to OpenGL.
- To create GLfloat arrays/lists you just create an ordinary list and then convert it like so: `(GLfloat * len(list1))(*list1)` , and the same for GLuint: `(GLuint * len(list2))(*list2)`
- You sometimes need to use python ctypes: `from ctypes import *` , in terms of the open.gl tutorials you mainly have to use pointer and sizeof for the C++ & and sizeof equivilants.
- Shader code is the same, you just put it in a string or in a seperate file, but to use it with `glShaderSource` you have to use the `cast` ctype, `pointer` and `POINTER` like so: `glShaderSource(fragmentShader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)`.
- Texture coordinates are reversed in pyglet.
- pyeuclid uses radians instead of degrees.
- To use the stencil buffer you have to enable it in the window config: `allowstencil = pyglet.gl.Config(stencil_size=8)` and `window = pyglet.window.Window(800, 600, "OpenGL", config=allowstencil)`