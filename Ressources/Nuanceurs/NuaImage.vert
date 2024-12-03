#version 330 core
precision mediump float;

in vec2 i_pos;

uniform vec2 pos;
uniform float rot;
uniform vec2 ech;

uniform vec2 taille_fenetre;

out vec2 uv;

void main(){
    gl_Position = vec4((i_pos*(ech/taille_fenetre)),0.0,1.0);
    uv = i_pos*0.5 + 0.5;
}