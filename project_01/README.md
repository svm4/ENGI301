<h1> One-Handed Piano </h1>
<h2> Brief Project Background </h2>
The one-handed piano project combines my passion for music and memorization games. By memorizing a given sequence in which lights are illuminated, users will be able to play "Jingle Bells" on the one-handed piano. 
<h2> Link to Hackster.io </h2>
All hardware information for this project is documented on my Hackster.io page linked here: https://www.hackster.io/svm4/pocketbeagle-one-handed-piano-06330d
<h2> Software Build Instructions </h2>
A few of my hardware components require installation of certain libraries in order to run properly. Install these libraries before running my project's code. 

SPI Screen:
- sudo apt-get update
- sudo pip3 install --upgrade Pillow
- sudo pip3 install adafruit-circuitpython-busdevice
- sudo pip3 install adafruit-circuitpython-rgb-display
- sudo apt-get install ttf-dejavu -y

From here, you can run the screen.py file to test the screen. Note that you should configure pins before running this file. You can copy the spi screen portion of configure_pins.sh into the terminal to do this. 

USB Speaker:

- sudo apt-get install alsa-utils libasound2 -y
- aplay -l
  - card 1 should show the USB device, while device 0 should say USB audio
- nano ~/.asoundrc
  - Add the following to your sound configuration file
      - [insert image]
- sudo apt-get install flite -y
- flite -t Hello!
- sudo apt-get install mplayer -y
- mplayer file_example_MP3_700KB.mp3
  - Download the above file from https://file-examples.com/index.php/sample-audio-files/
- sudo pip3 install sounddevice
- sudo pip3 install numpy
- sudo pip3 install libportaudio2
- sudo pip3 install libasound-dev
- [change to sudo]
  
<h2> Software Operation Instructions </h2>
[finish]
