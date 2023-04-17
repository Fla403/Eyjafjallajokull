#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 viewSkybox;
in vec3 position;
in vec2 tex_coord;

out vec2 frag_tex_coords;

void main() {

    mat4 newView = view;
    newView[0][3] = 0;
    newView[1][3] = 0;
    newView[2][3] = 0;
    gl_Position = projection * viewSkybox * model * vec4(position, 1);
    frag_tex_coords = tex_coord;
}
