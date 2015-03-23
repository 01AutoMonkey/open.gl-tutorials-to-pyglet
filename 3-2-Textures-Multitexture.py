# Tutorial: https://open.gl/textures
# Original Sample Code: https://github.com/Overv/Open.GL/blob/master/content/code/c3_multitexture.txt

import pyglet
from pyglet.gl import *
from ctypes import *
import math, time


window = pyglet.window.Window(800, 600, "OpenGL")
window.set_location(100, 100)


# Shaders (Vertex and Fragment shaders)
vertexSource = """
#version 150 core

in vec2 position;
in vec3 color;
in vec2 texcoord;

out vec3 Color;
out vec2 Texcoord;

void main() {
	Color = color;
	Texcoord = texcoord;
	gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragmentSource = """
#version 150 core

in vec3 Color;
in vec2 Texcoord;

out vec4 outColor;

uniform sampler2D texKitten;
uniform sampler2D texPuppy;

void main() {
	outColor = mix(texture(texKitten, Texcoord), texture(texPuppy, Texcoord), 0.5);
}
"""


# Vertex Input
## Vertex Array Objects
vao = GLuint()
glGenVertexArrays(1, pointer(vao))
glBindVertexArray(vao)

## Vertex Buffer Object
vbo = GLuint()
glGenBuffers(1, pointer(vbo)) # Generate 1 buffer

##          Position    Color          Texcoords
vertices = [-0.5,  0.5, 1.0, 0.0, 0.0, 0.0, 1.0, # Top-left
		     0.5,  0.5, 0.0, 1.0, 0.0, 1.0, 1.0, # Top-right
		     0.5, -0.5, 0.0, 0.0, 1.0, 1.0, 0.0, # Bottom-right
		    -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0]  # Bottom-left

## Convert the verteces array to a GLfloat array, usable by glBufferData
vertices_gl = (GLfloat * len(vertices))(*vertices)

## Upload data to GPU
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices_gl), vertices_gl, GL_STATIC_DRAW)


# Compile shaders and combining them into a program
## Create and compile the vertex shader
count = len(vertexSource)
src = (c_char_p * count)(*vertexSource)
vertexShader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertexShader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)
glCompileShader(vertexShader)

## Create and compile the fragment shader
count = len(fragmentSource)
src = (c_char_p * count)(*fragmentSource)
fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragmentShader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)
glCompileShader(fragmentShader)

## Link the vertex and fragment shader into a shader program
shaderProgram = glCreateProgram()
glAttachShader(shaderProgram, vertexShader)
glAttachShader(shaderProgram, fragmentShader)
glBindFragDataLocation(shaderProgram, 0, "outColor")
glLinkProgram(shaderProgram)
glUseProgram(shaderProgram)


# Element array
ebo = GLuint()
glGenBuffers(1, pointer(ebo))

elements = [0, 1, 2,
			2, 3, 0]
elements_gl = (GLuint * len(elements))(*elements)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(elements_gl), elements_gl, GL_STATIC_DRAW)


# Making the link between vertex data and attributes
posAttrib = glGetAttribLocation(shaderProgram, "position")
glEnableVertexAttribArray(posAttrib)
glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE, 7 * sizeof(GLfloat), 0)

## colAttrib returns -1 (is not used)
#colAttrib = glGetAttribLocation(shaderProgram, "color")
#glEnableVertexAttribArray(colAttrib)
#glVertexAttribPointer(colAttrib, 3, GL_FLOAT, GL_FALSE, 7 * sizeof(GLfloat), 2 * sizeof(GLfloat))

texAttrib = glGetAttribLocation(shaderProgram, "texcoord")
glEnableVertexAttribArray(texAttrib)
glVertexAttribPointer(texAttrib, 2, GL_FLOAT, GL_FALSE, 7 * sizeof(GLfloat), 5 * sizeof(GLfloat))


# Load textures
textures = [0] * 2
textures_ctype = (GLuint * len(textures))(*textures)
glGenTextures(2, textures_ctype)

glActiveTexture(GL_TEXTURE0)
glBindTexture(GL_TEXTURE_2D, textures_ctype[0])

image = pyglet.image.load("sample.png")
width, height = image.width, image.height
image = image.get_data('RGB', width * 3)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)

glUniform1i(glGetUniformLocation(shaderProgram, "texKitten"), 0)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

glActiveTexture(GL_TEXTURE1)
glBindTexture(GL_TEXTURE_2D, textures_ctype[1])

image = pyglet.image.load("sample2.png")
width, height = image.width, image.height
image = image.get_data('RGB', width * 3)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)

glUniform1i(glGetUniformLocation(shaderProgram, "texPuppy"), 1)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)


@window.event
def on_draw():
	# Set clear color
	glClearColor(0.0, 0.0, 0.0, 1.0)
	# Clear the screen to black
	glClear(GL_COLOR_BUFFER_BIT)

	# Draw a rectangle from the 2 triangles using 6 indices
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
