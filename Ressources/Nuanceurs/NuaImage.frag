#version 460 core
precision mediump float;

in vec2 uv;

out vec4 Fragment;

void main(){
    Fragment = vec4(uv,0.0,1.0);
}