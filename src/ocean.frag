#version 330 core

// global color variable
uniform vec3 global_color;
// light direction
uniform vec3 light;

// material properties
uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

// infos of vertex
in vec3 w_normal;
in vec3 w_position;
in float onTop;
in float onSide;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    //out_color = vec4(fragment_color + global_color, 1);

    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 diffuse_color = k_d * max(dot(n, l), 0);
    vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);

    //Fragment on the crest of a wave
    if(w_normal.y > 0.99995 && onSide==1){
        out_color = (vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1))+vec4(1, 1, 1, 1);
    }
    //Fragment between the crest and the hollow of a wave
    else if(w_normal.y > 0.9995 && onSide==1){
        out_color = (vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1))+vec4(0.2, 0.2, 0.2, 1);
    }
    //Fragment between the crest and the hollow of a wave
    else if(w_normal.y > 0.997 && w_normal.y < 0.9985 && onSide==1){
        out_color = (vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1))*0.8;
    }
    //Fragment in the hollow of a wave
    else{
        out_color = vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);
    }

//    out_color = vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);
}