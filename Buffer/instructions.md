# The C++ Buffer Breakthrough

## <>1. The Setup (The Vulnerable Environment)
    * In C++, a char array (a "buffer") is a fixed-size block of memory. If we place two arrays next to each other, we can "spill" data from one into the other. This is called a "buffer overflow" vulnerability.

### Instructions:
    run buffer.cpp
        * if you're on VSCode, open terminal and run "g++ buffer.cpp -o    buffer" to compile
        
        * then run "./buffer" to run the program

## 2. The Attack (The Payload)
    - Because C++ is not memory-safe, we can use a Threat Agent payload to overwrite the secret_key variable directly through the password_buffer.

    - Task: Run the program and enter a 16 character PIN

    - What happens in the program
        * The first 4 characters are read into the password_buffer
        * The next 4 characters fill the rest of the 8-character buffer
        * The remaining characters have nowhere to go, so they overflow into the memory space belonging to the secret_key variable

## 3. Analysis of the Attack
    - Subject vs. Object
        * The long string is the Subject (the agent entity used to conduct the attack),
        * while the secret_key memory is the Object (target entity)
    - Integrity Loss
        * Even if "Access Denied" triggers, the Integrity of the secret key is lost because a user modified it without authorization.
    - RAND Report Connection
        * This is exactly what Figure 1-4 refers to as a failure of "Bounds control" in software (Notes).

4. The Fix
    - This is left as an exercise at your discretion.

Why C++
    * To simulate the real-world scenario of a buffer overflow, we need to use a language that is not memory-safe.
    * for #4, you can opt to simulate the solution on any other language that is memory-safe.

5. Post-Activity Questions
    1. When you successfully used the payload to overwrite the secret_key variable, which pillar of the C.I.A. triad did you primarily violate? Explain why.
    2. What specific vulnerability category did you exploit when you entered a string longer than 8 characters?
    3. Why is your solution (#4 The Fix) more effective than simply "asking users to be honest"?
    4. Imagine this was running the control system for a local power grid.
        * Who might want to exploit this vulnerability?
        * What would be the real-world consequence if the secret_key (controlling the power switch) was overwritten by a pro cyber-attacker?