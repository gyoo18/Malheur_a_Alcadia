#version 330 core
precision mediump float;

in vec2 i_pos;

uniform vec2 pos;
uniform float rot;
uniform vec2 ech;

uniform vec2 taille_fenetre;

out vec2 uv;

void main(){
    mat2 rotMat = mat2( cos(rot),-sin(rot),
                        sin(rot), cos(rot));
    vec2 f_pos = rotMat*i_pos;
    gl_Position = vec4((i_pos*(ech/taille_fenetre)) + (pos/taille_fenetre),0.0,1.0);
    uv = i_pos*0.5 + 0.5;
    uv.y = 1.0-uv.y;
}