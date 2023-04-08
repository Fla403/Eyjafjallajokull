#version 330 core

// global color variable
uniform vec3 global_color;

uniform vec3 light_dir;
uniform vec3 k_d, k_a, k_s;
uniform float s;
uniform vec3 w_camera_position;

// receiving interpolated color for fragment shader
in vec3 fragment_color;
in vec3 w_position, w_normal;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    // vec3 n = normalize(w_normal);
    // vec3 l = normalize(-light_dir);
    // vec3 r = reflect(-l, n);
    // vec3 v = normalize(w_camera_position - w_position);

    // vec3 diffuse_color = k_d * max(dot(n, l), 0);
    // vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);

    // out_color = vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1) + vec4(fragment_color + global_color, 1);
    out_color = vec4(fragment_color + global_color, 1);
}