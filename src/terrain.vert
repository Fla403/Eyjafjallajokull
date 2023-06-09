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
out vec3 w_position;
out vec3 w_normal;   // in world coordinates

float rand(vec2 co) {
    return fract(0.5*sin(0.02*dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    // initialize the global color
    // fragment_color = color;
    
    

    vec3 finalPosition = position;
    vec2 pos = vec2(position.x, position.z);
    // finalPosition.y = exp(-(position.x*position.x + position.z*position.z)/500)*40
    //                 + exp(-(position.x*position.x + position.z*position.z)/3000)*10
    //                 - exp(-(position.x*position.x + position.z*position.z)/10)*50
    //                 + exp(-((position.x+20)*(position.x+35) + (position.z+20)*(position.z+35))/100)*5
    //                 + exp(-((position.x-25)*(position.x-25) + (position.z+25)*(position.z+25))/50)*10
    //                 + exp(-((position.x-40)*(position.x-40) + (position.z+15)*(position.z+15))/100)*10
    //                 + exp(-((position.x-45)*(position.x-45) + (position.z+30)*(position.z+30))/20)*10
    //                 + exp(-((position.x+45)*(position.x+45) + (position.z-30)*(position.z-30))/20)*10
    //                 + exp(-((position.x+40)*(position.x+40) + (position.z-35)*(position.z-35))/100)*5
    //                 + exp(-((position.x+40)*(position.x+40) + (position.z)*(position.z))/100)*10
    //                 + exp(-((position.x+38)*(position.x+38) + (position.z-20)*(position.z-20))/100)*10
    //                 + exp(-((position.x+5)*(position.x+5) + (position.z-40)*(position.z-40))/150)*15
    //                 + exp(-((position.x+25)*(position.x+25) + (position.z-35)*(position.z-35))/50)*12
    //                 + exp(-((position.x+22)*(position.x+22) + (position.z-45)*(position.z-45))/10)*8
    //                 + exp(-((position.x-22)*(position.x-22) + (position.z+45)*(position.z+45))/1000)*3
    //                 + rand(pos)
    //                 - 3;
    
    vec3 beach = vec3(.7578, .6953, .2);
    vec3 grass = vec3(0, .2, 0);
    vec3 volcano = vec3(.1, .1, .1);

    if(finalPosition.y > 18) {
        fragment_color = volcano;
    }
    else if(finalPosition.y > 6) {
        fragment_color = grass*0.7;
    }
    else {
        fragment_color = beach*0.4;
    }

    vec4 w_position4 = model * vec4(finalPosition, 1.0);
    w_position = w_position4.xyz / w_position4.w;

    w_normal = (model * vec4(normal, 1)).xyz / (model * vec4(normal, 1)).w;

    gl_Position = projection * view * model * w_position4;
}