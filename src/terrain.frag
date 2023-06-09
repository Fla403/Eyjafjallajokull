#version 330 core

// global color variable
uniform vec3 global_color;

uniform vec3 light;
uniform vec3 k_d = vec3(.9, .9, .9);
uniform vec3 k_a = vec3(0.9, 0.8, 0.8);
uniform vec3 k_s = vec3(.8, .6, .6);

float s = 2;
uniform vec3 w_camera_position;

// receiving interpolated color for fragment shader
in vec3 fragment_color;
in vec3 w_position;
in vec3 w_normal;

// output fragment color for OpenGL
out vec4 out_color;

float alphaFog(float dist) {
    float fogMin = 250.0;
    float fogMax = 450.0;

    if(dist < fogMin) {
        return 0.0;
    }
    if(dist > fogMax) {
        return 1.0;
    }

    return 1 - (fogMax - dist)/(fogMax - fogMin);
}

void main() {
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 diffuse_color = k_d * max(dot(n, l), 0.0);
    vec3 specular_color = k_s * pow(max(dot(r, v), 0.0), s);

    float d = distance(w_position, w_camera_position);
    float alpha = alphaFog(d);
    vec4 fogColor = vec4(0.6, 0.6, 0.6, 1);
// 
    out_color = (vec4(k_a, 1) + vec4(diffuse_color, 1.0) + vec4(specular_color, 1.0)) * vec4(fragment_color, 1.0);
    out_color += mix(out_color, fogColor, alpha);
    // out_color = vec4(fragment_color + global_color, 1);
}