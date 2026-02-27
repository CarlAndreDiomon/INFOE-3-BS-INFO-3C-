# Integrity Guardian (Hashing)

1. Goal
    - Build a Python tool that detects unauthorized modification (Loss of Integrity) in a physical file.

2. Scenario
    - You are protecting a sensitive file. If a Threat Agent changes even a single character in that file, your program must detect and provide a notification. 

3. Instructions
    - Create the Asset: Create a file named database.csv (you can check sampleDB.csv and create your own). 

    - Initialize the Control: Write a script to calculate the hash of this file. This represents your Protection Profile—the standard state of your secure data.

    - Simulate the Threat: Manually open the file and change one variable (let's say $100 to $1000).


    * We'll be utilizing cells, so preferable to use Google Colab (online, just run) or Jupyter Notebook (local, needs setup on VSCode)
        - [![Getting Started with Jupyter Notebooks in VS Code](https://thumbs.video-to-markdown.com/60e4fde0.jpg)](https://youtu.be/suAkMeWJ1yE)
        - Preferable to use Jupyter so you can observer changes made to csv file

    * See format.ipynb

- Post-Analysis
    1. In this specific activity, which one is the Subject (the entity that acts to conduct the check) and which is the Object (the entity that is the target of the check)?

    2. If you manually open the file and change one variable (from Instructions), is that action considered a Vulnerability or a Threat Event?

- Submittabls, format
    * the same with previous activity
    * do it by 3
    * document + code
    * lastname_course/yr/section_lab2