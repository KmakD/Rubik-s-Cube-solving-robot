# Rubik-s-Cube-solving-robot

The purpose of this project was to design and construct a Rubik’s Cube solving robot. It was necessary to choose a proper construction type and, on this basis, parts of the device such as stepper motors and their drivers, power supply, camera, and microcontroller. The casing of the robot was made of acrylic glass with the use of a laser cutting method. A rotation of the puzzle's sides is possible due to a rotation of stepper motors which axes are directly connected to a Rubik’s Cube centers. Furthermore, a universal PCB board was created which contains basic connections between electronic parts of the device. The project includes the writing of software enabling usage and proper working of the robot. The software core element is an application which, by using a camera allows to scan the state of a Rubik’s Cube, then find algorithms capable of shuffling the puzzle's side to the desired state and solve it. Moves used to solve the cube are designated using the Kociemba algorithm, which allows finding a highly optimal solution. To read algorithm sent by application and rotate desired stepper motors a microcontroller software was created. 
