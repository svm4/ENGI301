"""
--------------------------------------------------------------------------
One-Handed Piano
--------------------------------------------------------------------------
License:   
Copyright 2023 - Shannon McGill

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use the following hardware components to make a one-handed piano:  
  - SPI Screen
  - USB Speaker
  - Arcade Buttons (White, Red, Yellow, Green, Blue)
  - Buzzer

Software API: 
  OneHandedPiano()
    - Class for one-handed piano project
    
    run()
      - Navigates between the welcome screen and different modes

    button_pressed(goal_button)
      - Returns true to run function if a certain button is pressed

    learn_mode()
      - Teaches the user a song by illuminating buttons in a certain order and having users press the buttons in the given order to play song
      - Breaks the song into rounds so that users learn four notes at a time until the song is learned
      
    button_pressed_with_error_message(goal_button, note)
      - Illuminates button and plays note if the correct button is pressed
      - Displays error screen if the wrong button is pressed
      - Displays timeout screen if the user waits more than five seconds to press a button
      
    number_rounds()
      - Calculates the number of rounds in a song given rounds with four notes each
      
    get_rounds_notes(current_round, rounds)
      - Generates arrays for the pitches, note lengths, and corresponding button color for the notes in a given round
        
    practice_mode()
      - Allows user to practice by pressing buttons as they wish and playing corresponding notes
      - Returns to run function if the user holds down the red button for more than five seconds
      
    practice_button_pressed()
      - Illuminates button and plays corresponding note for as long as user presses down button
      - Determines and returns the duration of the button press to the practice_mode function
      
    play_note(note, time)
      - Plays a given note for a given amount of time
      
    stop_note()
      - Stops a note that is being played
      
    cleanup()
      - Cleans up hardware and exits program

Requirements:
  - Learn Mode
    - Illuminates buttons for a given round in the correct sequence for users to memorize
    - Users play the buttons in the correct order
    - The round is advanced, and the process continues to add on four notes each time until the song is learned
    - Displays error message if the user plays an incorrect note
    - Displays timeout message if the user waits longer than five seconds to play note
    
  - Practice Mode
    - Users are free to press the buttons as they wish
    - Notes corresponding to the pressed button will be played for as long as the user holds down the button
    - Escape mode by holding down the red button for at least five seconds
    
  - Quit
    - When prompted by the display, the red button can be pressed to cleanup the hardware and exit the program
    
  - Screens display at appropriate times
  - Buttons are used to navigate between modes

Uses: 
  - songs Library
  - color_button library
  - buzzer driver
  - led driver
  - threaded_button driver
  - screen driver

"""
import time
import math
import numpy
import sounddevice
import os
import buzzer
import screen
import threaded_button
import led
import color_button
import songs

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class OneHandedPiano():
    """ One-Handed Piano """
    buzzer      = None
    screen      = None
    white       = None
    red         = None
    yellow      = None
    green       = None
    blue        = None
    timeout     = None
    song        = None
    notes       = None 
    button_list = None 
    Note_Map    = None
    
    def __init__(self, buzzer_pin="P1_36", white_button_pin="P2_2", white_led_pin="P2_1",
                    red_button_pin="P2_4", red_led_pin="P2_3", yellow_button_pin="P2_6",
                    yellow_led_pin="P2_5", green_button_pin="P2_8", green_led_pin="P2_7",
                    blue_button_pin="P2_10", blue_led_pin="P2_9", timeout=5, song_number=0):

        """ Initialize variables and set up display """

        self.buzzer   = buzzer.Buzzer(buzzer_pin)
        self.screen   = screen.SPI_Display()
        self.white    = color_button.ColorButton(white_button_pin, white_led_pin)
        self.red      = color_button.ColorButton(red_button_pin, red_led_pin)
        self.yellow   = color_button.ColorButton(yellow_button_pin, yellow_led_pin)
        self.green    = color_button.ColorButton(green_button_pin, green_led_pin)
        self.blue     = color_button.ColorButton(blue_button_pin, blue_led_pin)
        self.timeout  = timeout
        
        # Creates an array for the song based on the song index
        self.song     = songs.SONGS[song_number]
        
        # Creates an array that contains only the notes in a song
        self.notes    = self.song['notes']
        
        self.button_list = [self.white,self.red,self.yellow,self.green,self.blue]
        
        # Note map to light up a certain LED given a certain pitch
        self.Note_Map = {
            songs.NOTE_C4: self.white,
            songs.NOTE_D4: self.red,
            songs.NOTE_E4: self.yellow,
            songs.NOTE_F4: self.green,
            songs.NOTE_G4: self.blue
            }
            
        # Reverse note map to play a given tone given a certain button color
        self.reverse_Note_Map = {
            self.white : songs.NOTE_C4,
            self.red   : songs.NOTE_D4,
            self.yellow: songs.NOTE_E4,
            self.green : songs.NOTE_F4,
            self.blue  : songs.NOTE_G4
            }
        
        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """ Setup the hardware components, including the screen, certain buttons, and the speaker volume """

        # Initialize display, turn on initial three buttons
        self.screen.image("Welcome Screen.jpg", 270)
        self.red.on()
        self.green.on()
        self.blue.on()
        
        # Set speaker volume at 50%
        os.system("amixer set PCM 50%")

        # Arcade Buttons
        #   - All initialized by libraries when instanitated

    # End def

    def run(self):
        """ Run function that navigates between the welcome screen and different modes """
        while(1):
            time.sleep(0.1)
            
            # Enters learn mode if green button is pressed
            if self.button_pressed(self.green):
                self.red.off()
                self.green.off()
                self.blue.off()
                self.learn_mode()
        
            # Enters practice mode if blue button is pressed
            if self.button_pressed(self.blue):
                self.red.off()
                self.green.off()
                self.blue.off()
                self.practice_mode()
            
            # Quits program if red button is pressed
            if self.button_pressed(self.red):
                self.red.off()
                self.green.off()
                self.blue.off()
                self.cleanup()
                
    # End def

    def button_pressed(self, goal_button):
        """Checks if a given goal_button is pressed. If it is, return to run function to enter a certain mode of play """
        while True:
            for b in self.button_list:
                if b.is_pressed():
                    if b == goal_button:
                        return True
                    else:
                        return False
            time.sleep(0.01)
        return False
            
    # End def

    def learn_mode(self):
        """ Learn Mode
              - For each round, illuminates a light sequence in a given order
              - Then, waits for user to play the buttons back in correct order
        """
        # Determine total number of rounds
        rounds=self.number_rounds() 
        
        current_round=1
        for i in range(rounds):
            
            # Creates arrays for the pitches, note lengths, and colors for a given round
            notes_for_round,times_for_round,colors_for_round=self.get_rounds_notes(current_round, rounds)
            
            note=0
            self.screen.image("Memorize Screen.jpg", 270)
            time.sleep(2)
            for i in range(len(notes_for_round)):
                
                # Breaks from loop if all notes have been illuminated
                if note > (len(notes_for_round)-1):
                    break
                
                # Illuminates note by lighting up correct LED for a given amount of time
                else:
                    colors_for_round[note].on()
                    time.sleep(times_for_round[note])
                    colors_for_round[note].off()
                    time.sleep(0.1)
                    note=note+1
                    
            played_note=0 
            self.screen.image("Play Screen.jpg", 270)
            time.sleep(0.1)
            for i in range(len(notes_for_round)):
                
                # Displays song learned screen once the user plays through all the notes in the song
                if (played_note == (len(self.notes)-1) and current_round == rounds):
                    if self.button_pressed_with_error_message(colors_for_round[played_note],notes_for_round[played_note]):
                        time.sleep(0.1)
                        self.screen.image("Song Learned Screen.jpg", 270) 
                        self.red.on()
                        self.green.on()
                        self.blue.on()
                        time.sleep(0.1)
                        return
                
                    # Returns to run function if wrong note was played or user does not press a button for over five seconds
                    else:
                        return
                
                # Advances to the next round once the user plays through all the notes in the song
                if played_note == (len(notes_for_round)-1):
                    if self.button_pressed_with_error_message(colors_for_round[played_note],notes_for_round[played_note]):
                        time.sleep(0.1)
                        self.screen.image("Next Round Screen.jpg", 270)
                        time.sleep(1)
                        break
                    
                    # Returns to run function if wrong note was played or user does not press a button for over five seconds 
                    else:
                        return
                
                # Plays note and illuminates button if user presses correct button
                elif self.button_pressed_with_error_message(colors_for_round[played_note],notes_for_round[played_note]):
                    time.sleep(0.1)
                    played_note=played_note+1 # Advances to the next note once a note is played
                    
                # Returns to run function if wrong note was played or user does not press a button for over five seconds
                else:
                    return
            current_round=current_round+1 # Advances to the next round once a round is learned
            
    # End def
    
    def button_pressed_with_error_message(self, goal_button, note):
        """ Button Pressed with Error Message
              - Illuminates button and plays note if the correct button is pressed
              - Displays error screen if the wrong button is pressed
              - Displays timeout screen if there is no user input after five seconds
        """
        # Saves initial time in order to track how long until the button is pressed
        initial_time=time.time()
        
        # Runs as long as timeout has not been exceeded 
        while time.time()-initial_time <= self.timeout:
            for b in self.button_list:
                if b.is_pressed():
                    
                    # Illuminates button and plays note if correct button is pressed
                    if b == goal_button:
                        pressed_time=time.time()
                        goal_button.on()
                        self.play_note(note,5)
                        while True:
                            
                            # Turns off LED and stops note once button is released
                            if not goal_button.is_pressed():
                                goal_button.off()
                                self.stop_note()
                                return True
                            time.sleep(0.1)
                    
                    # Displays wrong button screen if the user does not press the correct button
                    else:
                        self.screen.image("Wrong Button Screen.jpg", 270)
                        self.red.on()
                        self.green.on()
                        self.blue.on()
                        self.buzzer.play(440, 1.0, True)
                        time.sleep(0.1)
                        return False
            time.sleep(0.01)
        
        # Displays timeout screen if user does not press a button within five seconds
        self.screen.image("Timeout Screen.jpg", 270)
        self.red.on()
        self.green.on()
        self.blue.on()
        self.buzzer.play(440, 1.0, True)
        time.sleep(0.1)
        return False
            
    # End def
    
    def number_rounds(self):
        """ Calculates the number of rounds in the song given rounds of four notes each """
        number_notes=len(self.notes)
        
        # Ceil function rounds to the nearest whole number; Last round may be less than four notes
        rounds=math.ceil(number_notes/4)
        
        return rounds
        
    # End def

    def get_rounds_notes(self, current_round, rounds):
        """ Creates an array with the notes for the given round """
        # For the last round, creates an array with all remaining notes; This round may not have four notes
        if current_round == rounds:
            get_current_round_notes=self.notes[0:len(self.notes)]
        
        # For all other rounds, creates an array with four notes corresponding to the round number
        else:
            get_current_round_notes=self.notes[0:(current_round*4)]
            
        # Arrays for the pitch, note length, and colors of the notes in a given round
        notes_for_round=[pitch[0] for pitch in get_current_round_notes]
        times_for_round=[time[1] for time in get_current_round_notes]
        colors_for_round=[self.Note_Map[note] for note in notes_for_round if note in self.Note_Map]
        return notes_for_round, times_for_round, colors_for_round
        
    # End def
    
    def practice_mode(self):
        """ Practice Mode
              - Allows user to press buttons and play notes as they wish
              - Returns to run function if the red button has been pressed for longer than five seconds
        """
        self.screen.image("Practice Screen.jpg",270)
        while(1):
            time.sleep(0.1)
            
            # Function that illuminates button and plays note when user presses button
            (button, press_duration)=self.practice_button_pressed() 
            
            # If the red button is held for over five seconds, return to the run function
            if (isinstance(press_duration,float) and press_duration > self.timeout and (button==self.red)):
                self.screen.image("Welcome Screen.jpg", 270)
                self.red.on()
                self.green.on()
                self.blue.on()
                time.sleep(0.1)
                return
            
    # End def

    def practice_button_pressed(self):
        """ Practice Button Pressed Function
              - Illuminates button and plays corresponding note for as long as user presses button
              - Also calculates the time of the press to know if the user is trying to exit practice mode
        """
        for b in self.button_list:
            
            # Turns button on and plays note; also records time of button press
            if b.is_pressed():
                initial_time=time.time()
                b.on()
                self.play_note(self.reverse_Note_Map[b],7)
                while True:
                    
                    # Turns off button and stops note upon release; Calculates the press duration
                    if not b.is_pressed():
                        b.off()
                        self.stop_note()
                        press_duration=time.time()-initial_time
                        return (b, press_duration)
        return (None,0)
        
    # End def
    
    def play_note(self, note, time):
        """ Plays a given note for a given amount of time """
        tone=numpy.sin(2*numpy.pi*note*numpy.arange(0,time,1/44100))
        sounddevice.play(tone, 44100)
        
    # End def
    
    def stop_note(self):
        """ Stops a note """
        sounddevice.stop()
        
    # End def

    def cleanup(self):
        """Cleanup the hardware components."""
        
        self.buzzer.buzzer_cleanup()
        self.screen.blank()
        self.white.button_cleanup()
        self.red.button_cleanup()
        self.yellow.button_cleanup()
        self.green.button_cleanup()
        self.blue.button_cleanup()
        exit()
        
    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the one-handed piano
    one_handed_piano = OneHandedPiano()

    try:
        # Run the one-handed piano
        one_handed_piano.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        one_handed_piano.cleanup()

    print("Program Complete")