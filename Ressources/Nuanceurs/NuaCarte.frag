#version 460 core
precision mediump float;

in vec2 uv;

uniform ivec2 taille_carte;
const int INDEXES_TEXTURE_TAILLE = 30*30;
uniform int indexes_texture[INDEXES_TEXTURE_TAILLE];

uniform ivec2 taille_atlas;

layout (location=0) uniform sampler2D tex;

out vec4 Fragment;

void main(){
    vec2 tmp_uv = floor(uv*taille_carte);
    int indexe = indexes_texture[int(tmp_uv.x + tmp_uv.y*taille_carte.x)];

    vec2 pixels_atlas = vec2(textureSize(tex,0));
    vec2 taille_texture_uv = 1.0/vec2(taille_atlas);
    vec2 decalage = vec2( 
        mod(float(indexe),vec2(taille_atlas).x)*taille_texture_uv.x, 
        floor(float(indexe)/vec2(taille_atlas).x)*taille_texture_uv.y
    );
    vec2 t_uv = mod(uv*taille_carte,1.0)*taille_texture_uv + decalage;

    Fragment = texture(tex,t_uv);
}