#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;
in vec3 normal;

// global matrix variables
uniform mat4 view;
uniform mat4 projection;
uniform mat4 model;

// interpolated color for fragment shader, intialized at vertices
out vec3 fragment_color;
out vec3 w_position, w_normal;   // in world coordinates

float rand(vec2 co) {
    return fract(0.5*sin(0.02*dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}


void main() {
    // initialize the global color
    // fragment_color = color;
    
    vec4 w_position4 = model * vec4(position, 1.0);
    gl_Position = projection * view * w_position4;
    w_position = w_position4.xyz / w_position4.w;

    mat3 nit_matrix = transpose(inverse(mat3(model)));
    w_normal = normalize(nit_matrix * normal);

    vec3 finalPosition = position;
    vec2 pos = vec2(position.x, position.z);
    finalPosition.y = exp(-(position.x*position.x + position.z*position.z)/500)*40
                    + exp(-(position.x*position.x + position.z*position.z)/2000)*10
                    - exp(-(position.x*position.x + position.z*position.z)/10)*50
                    + exp(-((position.x+20)*(position.x+35) + (position.z+20)*(position.z+35))/100)*5
                    + exp(-((position.x-25)*(position.x-25) + (position.z+25)*(position.z+25))/50)*10
                    + exp(-((position.x-40)*(position.x-40) + (position.z+15)*(position.z+15))/100)*10
                    + exp(-((position.x-45)*(position.x-45) + (position.z+30)*(position.z+30))/20)*10
                    + exp(-((position.x+45)*(position.x+45) + (position.z-30)*(position.z-30))/20)*10
                    + exp(-((position.x+40)*(position.x+40) + (position.z-35)*(position.z-35))/100)*5
                    + exp(-((position.x+40)*(position.x+40) + (position.z)*(position.z))/100)*10
                    + rand(pos)
                    - 3;
    
    vec3 beach = vec3(1, 1, 0);
    vec3 grass = vec3(0, .3, 0);
    vec3 volcanoTop = vec3(0.01, 0.01, 0.01);
    vec3 volcano = vec3(.1, .1, .1);

    if(finalPosition.y > 35) {
        fragment_color = volcanoTop;
    }
    else if(finalPosition.y > 15) {
        fragment_color = volcano;
    }
    else if(finalPosition.y > 2) {
        fragment_color = grass;
    }
    else {
        fragment_color = beach;
    }


    // finalPosition.y = sin(position.x+position.z);
    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * vec4(finalPosition, 1);
}