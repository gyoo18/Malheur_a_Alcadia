#version 460 core
precision mediump float;

in vec2 uv;

uniform ivec2 taille_carte;
const int INDEXES_TEXTURE_TAILLE = 30*30;
uniform int indexes_texture[INDEXES_TEXTURE_TAILLE];

uniform ivec2 taille_atlas;

const int MAX_CASES_SELECT = 2;
uniform float taille_bordure[MAX_CASES_SELECT];
uniform vec4 couleur_bordure[MAX_CASES_SELECT];
uniform int indexe_selectionne[MAX_CASES_SELECT];

layout (location=0) uniform sampler2D tex;

out vec4 Fragment;

void main(){
    vec4 couleur_finale = vec4(1.0,0.0,1.0,1.0);

    vec2 tmp_uv = floor(uv*taille_carte);
    int indexe_position = int(tmp_uv.x + tmp_uv.y*taille_carte.x);
    int indexe = indexes_texture[indexe_position];

    vec2 pixels_atlas = vec2(textureSize(tex,0));
    vec2 taille_texture_uv = 1.0/vec2(taille_atlas);
    vec2 decalage = vec2( 
        mod(float(indexe),vec2(taille_atlas).x)*taille_texture_uv.x, 
        floor(float(indexe)/vec2(taille_atlas).x)*taille_texture_uv.y
    );
    vec2 t_uv = mod(uv*taille_carte,1.0)*taille_texture_uv + decalage;
    vec4 couleur_tuile = texture(tex,t_uv);

    couleur_finale = couleur_tuile;

    for(int i = 0; i < MAX_CASES_SELECT; i++){
        if(indexe_selectionne[i] == indexe_position){
            vec2 distance_bordure_uv = abs(mod(uv*taille_carte,1.0)*2.0-1.0);
            float distance_bordure = max(distance_bordure_uv.x,distance_bordure_uv.y);
            float bordure = float( distance_bordure > (1.0-taille_bordure[i]) );
            couleur_finale = mix(couleur_tuile,vec4(couleur_bordure[i].rgb*bordure,1.0),couleur_bordure[i].a*bordure);
            break;
        }
    }

    Fragment = couleur_finale;
}