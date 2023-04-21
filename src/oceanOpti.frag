#version 330 core

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

// Infos of vertex
in vec3 w_normal;
in vec3 w_position;

// Output fragment color for OpenGL
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

    vec3 diffuse_color = k_d * max(dot(n, l), 0);
    vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);

    vec3 L = normalize(-light.xyz);
    vec3 N = normalize(w_normal);

    float color = max(dot(N, vec3(-L.x, L.y, -L.z)), 0);
    float toonColor = floor(color*20.0)/50.0;
    vec3 c = (1.0/(10.0*toonColor))*(k_a + diffuse_color + specular_color);
    out_color = vec4(c, 1);

    float d = distance(w_position, w_camera_position);
    float alpha = alphaFog(d);
    vec4 fogColor = vec4(0.6, 0.6, 0.6, 1);
    out_color += mix(out_color, fogColor, alpha);
}
