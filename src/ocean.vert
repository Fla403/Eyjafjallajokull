#version 330 core

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;

// global variables
uniform float time;
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

// interpolated color for fragment shader, intialized at vertices
out vec3 w_normal;
out vec3 w_position;
out float onTop;
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

//void waveNormal(vec3 position, vec2 direction, float time, float steepness, float wavelength, inout vec3 tangent, inout vec3 binormal){
//
//    float k = 2*3.14159265359/wavelength;
//    float c = sqrt(9.8/k);
//    float f = k*(dot(direction, position.xz) - c*time);
//
//    tangent = vec3(1-direction.x*direction.x*steepness*sin(f),
//                        direction.y*steepness*cos(f),
//                        1-direction.y*direction.y*steepness*sin(f));
//
//    binormal = vec3(-direction.x*direction.y*steepness*sin(f),
//                        direction.y*steepness*cos(f),
//                        1-direction.y*direction.y*steepness*sin(f));
//}

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

    // Initialize the coefficient of the first wave
    float firstWavelength = 40;
    float firstSteepness = 0.15; //Must be between 0 and 1
    vec2 firstDirection = normalize(vec2(1, 1));
    // Initialize the coefficient of the second wave
    float secondWavelength = 31;
    float secondSteepness = 0.15; //Must be between 0 and 1
    vec2 secondDirection = normalize(vec2(1, 0.6));
    // Initialize the coefficient of the second wave
    float thirdWavelength = 18;
    float thirdSteepness = 0.15; //Must be between 0 and 1
    vec2 thirdDirection = normalize(vec2(1, 1.3));


//    //---------- Compute the first wave ----------
    vec3 position = wavePosition(position, firstDirection, time, firstSteepness, firstWavelength);
    leftNeighbour = wavePosition(leftNeighbour, firstDirection, time, firstSteepness, firstWavelength);
    rightNeighbour = wavePosition(rightNeighbour, firstDirection, time, firstSteepness, firstWavelength);
    upNeighbour = wavePosition(upNeighbour, firstDirection, time, firstSteepness, firstWavelength);
    downNeighbour = wavePosition(downNeighbour, firstDirection, time, firstSteepness, firstWavelength);

    vec3 tangent = vec3(1, 0, 0);
    vec3 binormal = vec3(0, 0, 1);
//    waveNormal(position, firstDirection, time, firstSteepness, firstWavelength, tangent, binormal);
    tangent += waveTangent(position, firstDirection, time, firstSteepness, firstWavelength, tangent);
    binormal += waveBinormal(position, firstDirection, time, firstSteepness, firstWavelength, binormal);

//    //---------- Compute the second wave ----------
    vec3 secondPosition = wavePosition(position, secondDirection, time, secondSteepness, secondWavelength);
    leftNeighbour = wavePosition(leftNeighbour, secondDirection, time, secondSteepness, secondWavelength);
    rightNeighbour = wavePosition(rightNeighbour, secondDirection, time, secondSteepness, secondWavelength);
    upNeighbour = wavePosition(upNeighbour, secondDirection, time, secondSteepness, secondWavelength);
    downNeighbour = wavePosition(downNeighbour, secondDirection, time, secondSteepness, secondWavelength);

//    waveNormal(position, firstDirection, time, firstSteepness, firstWavelength, tangent, binormal);
    tangent += waveTangent(secondPosition, secondDirection, time, secondSteepness, secondWavelength, tangent);
    binormal += waveBinormal(secondPosition, secondDirection, time, secondSteepness, secondWavelength, binormal);

    //---------- Compute the third wave ----------
    vec3 thirdPosition = wavePosition(secondPosition, thirdDirection, time, thirdSteepness, thirdWavelength);
    leftNeighbour = wavePosition(leftNeighbour, thirdDirection, time, thirdSteepness, thirdWavelength);
    rightNeighbour = wavePosition(rightNeighbour, thirdDirection, time, thirdSteepness, thirdWavelength);
    upNeighbour = wavePosition(upNeighbour, thirdDirection, time, thirdSteepness, thirdWavelength);
    downNeighbour = wavePosition(downNeighbour, thirdDirection, time, thirdSteepness, thirdWavelength);

//    waveNormal(position, firstDirection, time, firstSteepness, firstWavelength, tangent, binormal);
    tangent += waveTangent(thirdPosition, thirdDirection, time, thirdSteepness, thirdWavelength, tangent);
    binormal += waveBinormal(thirdPosition, thirdDirection, time, thirdSteepness, thirdWavelength, binormal);

    vec3 normal = normalize(cross(binormal, tangent));

    if ((leftNeighbour.y < thirdPosition.y && rightNeighbour.y < thirdPosition.y) || (upNeighbour.y < thirdPosition.y && downNeighbour.y < thirdPosition.y)){
        onTop = 1;
    }
    else{
        onTop = 0;
    }
    if (leftNeighbour.y < thirdPosition.y || rightNeighbour.y < thirdPosition.y || upNeighbour.y < thirdPosition.y || downNeighbour.y < thirdPosition.y){
        onSide = 1;
    }
    else{
        onSide = 0;
    }

    w_normal = (model * vec4(normal, 1)).xyz / (model * vec4(normal, 1)).w;
    w_position = (model * vec4(thirdPosition, 1)).xyz / (model * vec4(thirdPosition, 1)).w;

    gl_Position = projection * view * model *vec4(thirdPosition, 1); //TODO Besoin de la matrice model ou pas ?
}
