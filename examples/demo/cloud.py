# #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demonstrating a cloud of points.
"""

from vispy import oogl
from vispy import app
from vispy import gl
from OpenGL import GL
import numpy as np

# Create vetices 
n = 1000000
a_position = 0.45 * np.random.randn(n, 3).astype(np.float32)
a_bg_color = np.random.uniform(0.85,1.00,(n,4)).astype(np.float32)
a_bg_color[:,3] = 1
a_fg_color = 0.,0.,0.,1.
a_size  = np.random.uniform(5,10,(n,1)).astype(np.float32)
u_linewidth = 1.0
u_antialias = 1.0

from transforms import perspective, translate, rotate


VERT_SHADER = """
#version 120

// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_linewidth;
uniform float u_antialias;

// Attributes
// ------------------------------------
attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_size;

// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

void main (void) {
    v_size = a_size;
    v_linewidth = u_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
}
"""

FRAG_SHADER = """
#version 120

// Constants
// ------------------------------------


// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

// Functions
// ------------------------------------

// ----------------
float disc(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}

// ----------------
float arrow_right(vec2 P, float size)
{
    float r1 = abs(P.x -.50)*size + abs(P.y -.5)*size - v_size/2; 
    float r2 = abs(P.x -.25)*size + abs(P.y -.5)*size - v_size/2; 
    float r = max(r1,-r2);
    return r;
}

// ----------------
float ring(vec2 P, float size)
{
    float r1 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/2;
    float r2 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/4;
    float r = max(r1,-r2);
    return r;
}

// ----------------
float clober(vec2 P, float size)
{
    const float PI = 3.14159265358979323846264;
    const float t1 = -PI/2;
    const vec2  c1 = 0.2*vec2(cos(t1),sin(t1));
    const float t2 = t1+2*PI/3;
    const vec2  c2 = 0.2*vec2(cos(t2),sin(t2));
    const float t3 = t2+2*PI/3;
    const vec2  c3 = 0.2*vec2(cos(t3),sin(t3));

    float r1 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c1)*size);
    r1 -= v_size/3;
    float r2 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c2)*size);
    r2 -= v_size/3;
    float r3 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c3)*size);
    r3 -= v_size/3;
    float r = min(min(r1,r2),r3);
    return r;
}

// ----------------
float square(vec2 P, float size)
{
    float r = max(abs(gl_PointCoord.x -.5)*size, abs(gl_PointCoord.y -.5)*size);
    r -= v_size/2;
    return r;
}

// ----------------
float diamond(vec2 P, float size)
{
    float r = abs(gl_PointCoord.x -.5)*size + abs(gl_PointCoord.y -.5)*size; 
    r -= v_size/2;
    return r;
}

// ----------------
float vbar(vec2 P, float size)
{
    float r1 = max(abs(gl_PointCoord.x -.75)*size, abs(gl_PointCoord.x -.25)*size); 
    float r3 = max(abs(gl_PointCoord.x -.5)*size, abs(gl_PointCoord.y -.5)*size); 
    float r = max(r1,r3);
    r -= v_size/2;
    return r;
}

// ----------------
float hbar(vec2 P, float size)
{
    float r2 = max(abs(gl_PointCoord.y -.75)*size, abs(gl_PointCoord.y -.25)*size); 
    float r3 = max(abs(gl_PointCoord.x -.5)*size, abs(gl_PointCoord.y -.5)*size); 
    float r = max(r2,r3);
    r -= v_size/2;
    return r;
}

// ----------------
float cross(vec2 P, float size)
{
    float r1 = max(abs(gl_PointCoord.x -.75)*size, abs(gl_PointCoord.x -.25)*size); 
    float r2 = max(abs(gl_PointCoord.y -.75)*size, abs(gl_PointCoord.y -.25)*size); 
    float r3 = max(abs(gl_PointCoord.x -.5)*size, abs(gl_PointCoord.y -.5)*size); 
    float r = max(min(r1,r2),r3);
    r -= v_size/2;
    return r;
}


// Main
// ------------------------------------
void main()
{    
    float size = v_size +2*(v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;

    float r = disc(gl_PointCoord, size);
    // float r = square(gl_PointCoord, size);
    // float r = ring(gl_PointCoord, size);
    // float r = arrow_right(gl_PointCoord, size);
    // float r = diamond(gl_PointCoord, size);
    // float r = cross(gl_PointCoord, size);
    // float r = clober(gl_PointCoord, size);
    // float r = hbar(gl_PointCoord, size);
    // float r = vbar(gl_PointCoord, size);


    float d = abs(r) - t;
    if( r > (v_linewidth/2.0+v_antialias))
    {
        discard;
    }
    else if( d < 0.0 )
    {
       gl_FragColor = v_fg_color;
    }
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > 0)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
}
"""



class Canvas(app.Canvas):

    # ---------------------------------
    def __init__(self):
        app.Canvas.__init__(self)
        self.geometry = (0,0,1000,1000)

        self.program = oogl.ShaderProgram( oogl.VertexShader(VERT_SHADER), 
                                           oogl.FragmentShader(FRAG_SHADER) )
        # Set uniform and attribute
        self.program.attributes['a_fg_color'] = a_fg_color
        self.program.attributes['a_bg_color'] = a_bg_color
        self.program.attributes['a_position'] = a_position
        self.program.attributes['a_size']     = a_size
        self.program.uniforms['u_linewidth']  = u_linewidth
        self.program.uniforms['u_antialias']  = u_antialias

        self.view       = np.eye(4,dtype=np.float32)
        self.model      = np.eye(4,dtype=np.float32)
        self.projection = np.eye(4,dtype=np.float32)

        self.translate = 5
        translate(self.view, 0,0, -self.translate)
        self.program.uniforms['u_model'] = self.model
        self.program.uniforms['u_view'] = self.view

        self.theta = 0
        self.phi = 0

        self.timer = app.Timer(1.0/60)
        self.timer.connect(self.on_timer)
        #self.timer.start()


    # ---------------------------------
    def on_initialize(self, event):
        gl.glClearColor(1,1,1,1)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        gl.glEnable(GL.GL_POINT_SPRITE)


    # ---------------------------------
    def on_key_press(self,event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()


    # ---------------------------------
    def on_timer(self,event):
        self.theta += .5
        self.phi += .5
        self.model = np.eye(4, dtype=np.float32)
        rotate(self.model, self.theta, 0,0,1)
        rotate(self.model, self.phi,   0,1,0)
        self.program.uniforms['u_model'] = self.model
        self.update()


    # ---------------------------------
    def on_resize(self, event):
        width, height = event.size
        gl.glViewport(0, 0, width, height)
        self.projection = perspective( 45.0, width/float(height), 1.0, 1000.0 )
        self.program.uniforms['u_projection'] = self.projection


    # ---------------------------------
    def on_mouse_wheel(self, event):
        self.translate +=event.delta[1]
        self.translate = max(2,self.translate)
        self.view       = np.eye(4,dtype=np.float32)
        translate(self.view, 0,0, -self.translate)
        self.program.uniforms['u_view'] = self.view
        self.program.attributes['a_size'] = a_size*5/self.translate
        self.update()


    # ---------------------------------
    def on_paint(self, event):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        with self.program as prog:
            prog.draw_arrays(gl.GL_POINTS)


if __name__ == '__main__':
    c = Canvas()
    c.show()
    app.run()