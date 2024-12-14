#version 330 core
precision mediump float;
in vec3 POS;
in vec3 NORM;
in vec3 UV;

out vec4 col;
out float w;

uniform mat4 matrice;
uniform float color;

void main(){
    gl_Position = matrice*vec4(POS,1.0);
    col = vec4(NORM,1.0); 
}