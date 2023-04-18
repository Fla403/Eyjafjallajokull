#version 330 core

// Input attribute variable, given per vertex
in vec3 position;
in vec3 color;

// Global variables
uniform float time;
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

// Out variables used in the fragment shader
out vec3 w_normal;
out vec3 w_position;
out float onSide;

vec3 wavePosition(vec3 position, vec2 direction, float time, float steepness, float wavelength){

    vec3 wave;
    float k = 2*3.14159265359/wavelength;
    float c = sqrt(9.8/k);
    float f = k*(dot(direction, position.xz) - c*time);
    float a = steepness/k;

    wave.x = position.x + direction.x*a*cos(f);
    wave.z = position.z + direction.y*a*cos(f);

    wave.y = position.y + a*sin(f);

    return wave;
}

vec3 waveTangent(vec3 position, vec2 direction, float time, float steepness, float wavelength, vec3 tangent){

    float k = 2*3.14159265359/wavelength;
    float c = sqrt(9.8/k);
    float f = k*(dot(direction, position.xz) - c*time);

    vec3 outTangent = vec3(1-direction.x*direction.x*steepness*sin(f),
                        direction.y*steepness*cos(f),
                        1-direction.y*direction.y*steepness*sin(f));
    return outTangent;
}

vec3 waveBinormal(vec3 position, vec2 direction, float time, float steepness, float wavelength, vec3 binormal){

    float k = 2*3.14159265359/wavelength;
    float c = sqrt(9.8/k);
    float f = k*(dot(direction, position.xz) - c*time);

    vec3 outBinormal = vec3(-direction.x*direction.y*steepness*sin(f),
                        direction.y*steepness*cos(f),
                        1-direction.y*direction.y*steepness*sin(f));
    return outBinormal;
}

void main() {

    float margin = 0.001;
    vec3 leftNeighbour = position + vec3(margin,0,0);
    vec3 rightNeighbour = position + vec3(-margin,0,0);
    vec3 upNeighbour = position + vec3(0,0,margin);
    vec3 downNeighbour = position + vec3(0,0,-margin);

    // Initialize the coefficients of the first wave
    float firstWavelength = 2;
    float firstSteepness = 0.5; //Must be between 0 and 1
    vec2 firstDirection = normalize(vec2(1, 0.3));
    // Initialize the coefficients of the second wave
    float secondWavelength = 3;
    float secondSteepness = 0.5; //Must be between 0 and 1
    vec2 secondDirection = normalize(vec2(0, 1));



    //---------- Compute the first wave ----------
    vec3 firstPosition = wavePosition(position, firstDirection, time, firstSteepness, firstWavelength);
    leftNeighbour = wavePosition(leftNeighbour, firstDirection, time, firstSteepness, firstWavelength);
    rightNeighbour = wavePosition(rightNeighbour, firstDirection, time, firstSteepness, firstWavelength);
    upNeighbour = wavePosition(upNeighbour, firstDirection, time, firstSteepness, firstWavelength);
    downNeighbour = wavePosition(downNeighbour, firstDirection, time, firstSteepness, firstWavelength);

    vec3 tangent = vec3(1, 0, 0);
    vec3 binormal = vec3(0, 0, 1);
    tangent += waveTangent(firstPosition, firstDirection, time, firstSteepness, firstWavelength, tangent);
    binormal += waveBinormal(firstPosition, firstDirection, time, firstSteepness, firstWavelength, binormal);

    //---------- Compute the second wave ----------
    vec3 secondPosition = wavePosition(firstPosition, secondDirection, time, secondSteepness, secondWavelength);
    leftNeighbour = wavePosition(leftNeighbour, secondDirection, time, secondSteepness, secondWavelength);
    rightNeighbour = wavePosition(rightNeighbour, secondDirection, time, secondSteepness, secondWavelength);
    upNeighbour = wavePosition(upNeighbour, secondDirection, time, secondSteepness, secondWavelength);
    downNeighbour = wavePosition(downNeighbour, secondDirection, time, secondSteepness, secondWavelength);

    tangent += waveTangent(secondPosition, secondDirection, time, secondSteepness, secondWavelength, tangent);
    binormal += waveBinormal(secondPosition, secondDirection, time, secondSteepness, secondWavelength, binormal);

    vec3 normal = normalize(cross(binormal, tangent));

    // We look if the vertex is in the hollow of the wave or not for toonshading
    if (leftNeighbour.y < secondPosition.y || rightNeighbour.y < secondPosition.y || upNeighbour.y < secondPosition.y || downNeighbour.y < secondPosition.y){
        onSide = 1;
    }
    else{
        onSide = 0;
    }

    secondPosition.y -= exp(-(secondPosition.x*secondPosition.x + secondPosition.z*secondPosition.z)/15)*15;
    if (secondPosition.x*secondPosition.x + secondPosition.z*secondPosition.z > 35){
        secondPosition.y -= 20;
    }

    w_normal = (model * vec4(normal, 1)).xyz / (model * vec4(normal, 1)).w;
    w_position = (model * vec4(secondPosition, 1)).xyz / (model * vec4(secondPosition, 1)).w;

    gl_Position = projection * view * model *vec4(secondPosition, 1);
}
