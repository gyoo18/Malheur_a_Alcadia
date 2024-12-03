#version 460 core
precision mediump float;

in vec4 col;
in float w;

out vec4 Fragment;

void main(){
    //if( col.z > 1.0){
    //    Fragment = vec4(1.0,0.0,1.0,1.0);
    //}
    //else if(col.z < -1.0)
    //{
    //    Fragment = vec4(0.0,1.0,0.0,1.0);
    //}
    //else
    //{
        Fragment = col*0.5 + 0.5;
    //}
}