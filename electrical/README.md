# Designing the Electronic Speed Controller

Up to this point, I was focused only on creating theI knew I needed a motor controller, but spared looking for one until it was finished. However, as I looked online, their prices were rocket high— reliable electric speed Controller ones came at around $30, $40, even $70 dollars for 1! It cost as much as my 3D printed motor I made, and it was even double that of my arduino starter kit! With these price tags, I wanted to get more than a simple motor controller; I should learn something long, lasting, and meaningful that’ll be of service to me in future. It was then I knew I’d make one, one that had much more value than a simple controller.  
Luckily, my electronics journey had already started (around November of 2024). I’d always wanted to learn something new with the starter kit my parents purchased for me. I watched lessons and the playlist series of ELEC 110 and 220, taught by Joe Gryniuk at Lake Washington Technical College, and followed along with the corresponding textbook “Introduction to Electronics“ on train rides and spare time. 

## Breadboard Prototypes
I started by finding values to represent each motor coil in a circuit.  
First, I measured the linear resistance of each inductor using the ohm-meter on my MM450.  

<img src="README_images/CharacterizingAssembledMotor/gsheets_phaseResistances.png" alt="Phase resistance calculations " height="300">

Next, I wanted a good estimate of my motor phase inductances. Despite not having access to an inductance-measuring tool, I eventually figured out a viable formula, using the AC-signal analysis tools I learned from Aaron’s Damer transistors playlist, as well as the node methods from 6.002 lectures by Anant Agarwhal.  

<img src="README_images/CharacterizingAssembledMotor/LR_circuit_derivation.png" alt="Solving for inductances in LR circuit " height="300"><img src="README_images/CharacterizingAssembledMotor/bjt_voltage_amplifier_calculations.png" alt="Solving for DC biasing resistors for a darlington voltage amplification circuit" height="300">

This was the circuit schematic for my voltage AC-source, shown on falstad.com.  

<img src="README_images/ESC_v0_falstad/falstad_winding_inductrance_test_with_darlington_amplifier.png" alt="my darlington amplifier circuit on Falstad.com" height="400">

In the DC Darlington model above,  I used ESP32's DAC pins to generate a pseudo-sine wave to mimic an AC signal, which I fed into a Darlington amplifier to create an AC- voltage source. Using definitions and formulas for impedance, I determined an estimate of the phase inductances.  
 
<img src="README_images/CharacterizingAssembledMotor/gsheets_phaseInductances.png" alt="Phase inductance calculations done on google sheets" height="200">

These phases and 20mΩ current sense shunt resistors comprised of my “Motor phases” subcircuit in Falstad.com

<img src="README_images/ESC_v0_falstad/falstad_subcircuit_motor_phases.png" alt="how I modeled my motor phases in falstad" height="200"> 
<!-- <img src="README_images/ESC_v0_falstad/falstad_subcircuit_motor_symbol.png" alt="how I represented my motor phases in falstad" height="200"> -->



## Motor circuit:

<img src="README_images/ESC_v1/motor_controller_blockDiagram.png" alt="Almost finished block diagram of my motor " height="500">

My motor controller uses a 3 half-bridge configuration, one half-bridge for each phase. The power bus will be connected to a boost converter, taking the 12V battery input and producing 24V for the gates. Shunt current sense resistors in-line with motor phases are paired with current sense amplifiers to measure the current. Another buck-converter supplied the logic voltage of 5V, which will be used to power the ESP-33. The AS5600 magnetic encoder communicates with the ESP-32 using I2C. To reduce costs, I had asked my robotics coach for permission to bring broken FRC motor controllers home, which I disassembled to salvage PSMN1R0-30YLD enhancement-mode mosfets for my half bridges. 

<!--=========================== COLLAPSIBE SECTION ===========================-->
##
<details>
   <summary> <h3><strong>A failed attempt at creating Boost converter with feedback Control Loop</strong></h1> </summary>
    <!-- NEED BROKEN LINE HERE -->
    I wanted to design my own boost and buck converter module as well, after being inspired from watching MIT’s Open Courseware 6.022 Power electronics series; however, I struggled to implement a feedback system for a stable output voltage.  
    Show below is my basic 555 astable implementation for a boost converter:  
    <img src="README_images/555_Timer_Ideas/falstad_subcircuit_boostConverterNoFeedback.png" alt="basic model of my boost coverter in falstad" height="400">
    <br>
    My thought process was this: a logic or feedback system could be made either by programming a microcontroller to take input and give output, or it could automatically be regulated by hardware. I didn’t want to use multiple microcontrollers, and I thought creating feedback systems with hardware was more elegant than programming, so I attempted to manipulate the voltage of the CTRL pin on the 555 timer (used in an astable output configuration). the core Integrated chip(IC) that provided the necessary switching logic. I first attempted to look for a mathematical relationship between the duty cycle and the CTRL pin voltage.  
    <img src="README_images/555_Timer_Ideas/notebook_boostConverter_page1.png" alt="Page 1 of my notebook on boost converters with 555 timer" height="500">
    <img src="README_images/555_Timer_Ideas/notebook_boostConverter_page2.png" alt="Page 2 of my notebook on boost converters with 555 timer" height="500">
    <img src="README_images/555_Timer_Ideas/notebook_boostConverter_page3.png" alt="Page 3 of my notebook on boost converters with 555 timer" height="500">
    <br>
    Graphing showed me a direct (almost linear) relationship between the duty cycle and , which I hoped I could utilize through some feedback network.   
    <img src="README_images/555_Timer_Ideas/notebook_desmos_V_ctrl_vs_Duty.png" alt="Desmos graph of the equation I derived in the notebook" height="300">
    <br>
    So, I tried a 2 stage-implementation of my solution. The vertical switch would be closed, and the horizontal one would be open. Stage one has an Op-Amp with unity gain to act as a buffer (switch open in the circuit) so I drew negligible current from the voltage divider (which brought down the voltage to a ratio I hoped to keep constant). Stage 2 compared the output of the buffer to a potentiometer, which I would use to adjust the setpoint voltage.
    <img src="README_images/555_Timer_Ideas/falstad_subcircuit_boostConverterBadFeedbackLoop.png" alt="model of my boost converter with my 2 stage op-amp for feedback idea in falstad" height="500">
    <br>
    However, it had many problems. Falstad showed that the circuit didn’t work as I predicted: adjustments would often change the 555 switching duty cycle and switching frequency. I spent multiple days attempting to solve this problem, but I realized if I continued, my project’s pacing would be slow. The time I spent on designing motor cases reminded me that I needed to get a prototype soon, and fail fast. So I decided to buy the converters online, and book this sub-project for a future investigation.
    
</details>

##
<!--=========================== COLLAPSIBE SECTION ===========================-->

This was my final breadboard prototype circuit schematic. The main difference between this and my intended PCB design was that I made bootstrap circuits for my high-side MOSFET to use instead of the gate drivers that I lacked. I built this circuit, ran it, and was able to reach motor speeds up to 800rpm using 6-step commutation (see video).  

<img src="README_images/ESC_v0_falstad/falstad_breadboard_prototype_schematic.png" alt="My full breadboard motor controller circuit in falstad" height="500">  

[caption: op-amps to represent Current Sense Amplifiers temporarily removed]

<!-- Testing video: [https://drive.google.com/file/d/1aiDmqKBAf_SJHJi-CjGYLPHVinIo39mS/view?usp=sharing](https://drive.google.com/file/d/1aiDmqKBAf_SJHJi-CjGYLPHVinIo39mS/view?usp=sharing)  -->


# Motor Characteristics

From my tests, my motor coils always struggled with generating a magnetic field. I did my share of research, both from my physics regents classes and online searching, and I learned about B = µ₀(N/ℓ)I. I had an air core for my solenoid, and my number of turns and wire length was already determined by my 4oz supply of wire. So, I had to increase my voltage.

After consideration, I decided to use a motor bus voltage of 23-24V maximum, as that would put my phase current at around 1A (if 2 phases were enabled); However, that would only occur when the motor stalls. In normal operation, I would put the motor current to .8A, as I was worried about motor temperature, and that was a safe limit that online sources and ChatGPT had suggested. 57 degrees was the temperature the PLA casing would start degrading or soften.  

<img src="README_images//ESC_v0_falstad/GPT_on_Thermal_Characteristics.png" alt="Image of Chat GPT’s response to the amount of current I should run to sustain temperatures below 57 degrees F" height="300">

## Designing around ESP32

From watching motor control algorithms, such as Field-Oriented Control (FOC) by Texas Instruments and also Janteen Lee’s series on FOC, I learned I needed shunts for phase current sensing. I will use 2 shunts to determine the current of 2 phases, and use Kirchoff's Current Law to determine the third phase current.

While most modern BLDC motors run with 20kHz PWM frequency, I chose to use 16kHz because 1) it was barely within my audio hearing range, and 2) I wanted to use ESP32’s ADC to read the measurements. For my first PCB, I’ve decided to sample with the ADC at 16kHz as well, so that I my measurements are always timed with the gate switching Using 16kHz allows me to attempt higher sampling frequencies in the future, such as 64kHz across 2 channels, totaling to 128kHz, which was about the limit of Espressif’s recommended ESP32 ADC reading speed.

After my circuit was finished, I recreated the schematic on EasyEDA and added more suitable components. While I haven’t wired the traces on the PCB, I have settled on a preferred component placement to minimize inductance and cross-talk across signals on my PCB. Below are the footprints as well as a 3D-model rendition of my current part placement.  
While it is still a work-in progress, I’m excited for its completion!  
<img src="README_images/ESC_v1/easyeda_plannedComponentLayoutAndFootprints.png" alt="Image of my component layout in EasyEda" height="500">  
<img src="README_images/ESC_v1/easyeda_plannedComponentLayout_3D.png" alt="Image of the 3D view of my component layout in easyeda" height="500">  
