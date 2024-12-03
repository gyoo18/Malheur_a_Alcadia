#version 460 core
precision mediump float;

in vec2 uv;

layout (location=0) uniform sampler2D tex;

out vec4 Fragment;

void main(){
    Fragment = texture(tex,uv);
}