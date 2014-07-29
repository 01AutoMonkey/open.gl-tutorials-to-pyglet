import pyglet
from pyglet.gl import *
from shader import Shader
from ctypes import pointer, sizeof


window = pyglet.window.Window(800, 600, "OpenGL")
window.set_location(100, 100)


# Vertex Input
## Vertex Array Objects
vao = GLuint()
glGenVertexArrays(1, pointer(vao))
glBindVertexArray(vao)

## Vertex Buffer Object
vbo = GLuint()
glGenBuffers(1, pointer(vbo)) # Generate 1 buffer

vertices = [0.0, 0.5,
			0.5, -0.5,
			-0.5, -0.5]
## Convert the verteces array to a GLfloat array, usable by glBufferData
vertices_gl = (GLfloat * len(vertices))(*vertices)

## Upload data to GPU
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices_gl), vertices_gl, GL_STATIC_DRAW)


# Shaders (Vertex and Fragment shaders)
vertex = """
#version 150

in vec2 position;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragment = """
#version 150

out vec4 outColor;

void main()
{
    outColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""
## Compiling shaders and combining them into a program 
shader = Shader(vertex, fragment)
shader.bind() #glUseProgram


# Making the link between vertex data and attributes
## shader.handle holds the value of glCreateProgram()
posAttrib = glGetAttribLocation(shader.handle, "position")
glEnableVertexAttribArray(posAttrib)
glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE, 0, 0)


# Set clear color
glClearColor(0.0, 0.0, 0.0, 1.0)


@window.event
def on_draw():
	#Clear the screen to black
	glClear(GL_COLOR_BUFFER_BIT)

	#Draw a triangle from the 3 vertices
	glDrawArrays(GL_TRIANGLES, 0, 3);

@window.event
def on_key_press(symbol, modifiers):
    pass

@window.event
def on_key_release(symbol, modifiers):
    pass

def update(dt):
    pass
pyglet.clock.schedule(update)


pyglet.app.run()
