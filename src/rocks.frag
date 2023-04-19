#version 330 core

// Infos of vertex
in vec3 w_normal;
in vec3 w_position;

// Global variables
// Light direction
uniform vec3 light;
// Material properties
uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;
// World camera position
uniform vec3 w_camera_position;

// Output fragment color for OpenGL
out vec4 out_color;

void main() {

    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 diffuse_color = k_d * max(dot(n, l), 0);
    vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);

    out_color = vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);
}
