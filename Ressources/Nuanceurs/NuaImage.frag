#version 460 core
precision mediump float;

in vec2 uv;

layout (location=0) uniform sampler2D tex;
uniform vec4 bordure_couleur;

out vec4 Fragment;

void main(){
    vec2 taille_pixel_uv = 1.0/textureSize(tex,0);
    bool estBordure = texture(tex,uv + vec2(1.0,0.0)*taille_pixel_uv).a > 0.99;
    estBordure = estBordure || texture(tex,uv + vec2(-1.0,0.0)*taille_pixel_uv).a > 0.99;
    estBordure = estBordure || texture(tex,uv + vec2(0.0,1.0)*taille_pixel_uv).a > 0.99;
    estBordure = estBordure || texture(tex,uv + vec2(0.0,-1.0)*taille_pixel_uv).a > 0.99;
    vec4 couleur_texture = texture(tex,uv);
    estBordure = estBordure && couleur_texture.a < 0.99;
    Fragment = mix(texture(tex,uv),bordure_couleur,float(estBordure));
}