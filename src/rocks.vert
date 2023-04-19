#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float time;
uniform float posX;
uniform float posY;
uniform float posZ;
uniform float speedX;
uniform float speedY;
uniform float speedZ;
uniform float accelX;
uniform float accelY;
uniform float accelZ;

in vec3 position;

out vec3 w_normal;
out vec3 w_position;


void main() {

    vec3 pos = vec3(posX, posY, posZ) + position;
    vec3 speed = vec3(speedX, speedY, speedZ);
    vec3 accel = vec3(accelX, accelY, accelZ);



    vec3 newPosition = (1.0/2.0)*accel*time*time + speed*time + pos;

    float cyclingTime;
    float rollbackTime = (-speed.y - sqrt(speed.y*speed.y-2*accel.y*posY))/accel.y;
    if (newPosition.y < 0){
        cyclingTime = mod(time, rollbackTime);
    }

    newPosition = (1.0/2.0)*accel*cyclingTime*cyclingTime + speed*cyclingTime + pos;

    w_normal = newPosition;
    w_position = newPosition;

    gl_Position = projection * view * model * vec4(newPosition, 1);
}
