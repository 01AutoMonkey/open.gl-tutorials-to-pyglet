import pyglet
from pyglet.gl import *
from shader import Shader
from ctypes import pointer, sizeof
import math
import time


window = pyglet.window.Window(800, 600, "OpenGL")
window.set_location(100, 100)


# Shaders (Vertex and Fragment shaders)
vertex = """
#version 150

in vec2 position;
in vec3 color;

out vec3 Color;

void main()
{
    Color = color;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragment = """
#version 150

in vec3 Color;

out vec4 outColor;

void main()
{
    outColor = vec4(Color, 1.0);
}
"""
## Compiling shaders and combining them into a program 
shader = Shader(vertex, fragment)
shader.bind() #glUseProgram


# Vertex Input
## Vertex Array Objects
vao = GLuint()
glGenVertexArrays(1, pointer(vao))
glBindVertexArray(vao)

## Vertex Buffer Object
vbo = GLuint()
glGenBuffers(1, pointer(vbo)) # Generate 1 buffer

vertices = [-0.5, 0.5, 1.0, 0.0, 0.0,
			0.5, 0.5, 0.0, 1.0, 0.0,
			0.5, -0.5, 0.0, 0.0, 1.0,
			-0.5, -0.5, 1.0, 1.0, 1.0]
## Convert the verteces array to a GLfloat array, usable by glBufferData
vertices_ctype = (GLfloat * len(vertices))(*vertices)

## Upload data to GPU
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices_ctype), vertices_ctype, GL_STATIC_DRAW)


# Element array
ebo = GLuint()
glGenBuffers(1, pointer(ebo))

elements = [0, 1, 2,
			2, 3, 0]
elements_ctype = (GLuint * len(elements))(*elements)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(elements_ctype), elements_ctype, GL_STATIC_DRAW);


# Making the link between vertex data and attributes
## shader.handle holds the value of glCreateProgram()
posAttrib = glGetAttribLocation(shader.handle, "position")
glEnableVertexAttribArray(posAttrib)
glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE,
						5*sizeof(GLfloat), 0)

colAttrib = glGetAttribLocation(shader.handle, "color");
glEnableVertexAttribArray(colAttrib);
glVertexAttribPointer(colAttrib, 3, GL_FLOAT, GL_FALSE,
                       5*sizeof(GLfloat), 2*sizeof(GLfloat));


# Set clear color
glClearColor(0.0, 0.0, 0.0, 1.0)


@window.event
def on_draw():
	# Clear the screen to black
	glClear(GL_COLOR_BUFFER_BIT)

	# Draw a triangle from the 3 vertices
	glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)

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