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
  - Speaker
  - Arcade Buttons (White, Red, Yellow, Green, Blue)
  - Buzzer

Requirements:
  - Hardware: FIX THIS
    - When locked:   Red LED is on; Green LED is off; Servo is "closed"; Display is unchanged
    - When unlocked: Red LED is off; Green LED is on; Servo is "open"; Display is "----"
    - Display shows value of potentiometer (raw value of analog input divided by 8)
    - Button
      - Waiting for a button press should allow the display to update (if necessary) and return any values
      - Time the button was pressed should be recorded and returned
    - User interaction:
      - Needs to be able to program the combination for the “lock”
        - Need to be able to input three values for the combination to program or unlock the “lock”
      - Combination lock should lock when done programming and wait for combination input
      - If combination is unsuccessful, the lock should go back to waiting for combination input
      - If combination was successful, the lock should unlock
        - When unlocked, pressing button for less than 2s will re-lock the lock; greater than 2s will allow lock to be re-programmed

Uses: FIX THIS
  - Libraries developed in class

"""
import time
import math
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
        self.song     = songs.SONGS[song_number]
        self.notes    = self.song['notes']
        self.button_list = [self.white,self.red,self.yellow,self.green,self.blue]
        self.Note_Map = {
            songs.NOTE_C4: self.white,
            songs.NOTE_D4: self.red,
            songs.NOTE_E4: self.yellow,
            songs.NOTE_F4: self.green,
            songs.NOTE_G4: self.blue
            }
        
        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""

        # Initialize Display, Turn on Initial Two Buttons
        self.screen.image("Welcome Screen.jpg", 270)
        self.green.on()
        self.blue.on()

        # Arcade Buttons
        #   - All initialized by libraries when instanitated

    # End def


    def run(self):
        """Run Function
        """
        print("Run")
        while(1):
            time.sleep(0.1)
            if self.button_pressed(self.green):
                self.green.off()
                self.blue.off()
                self.learn_mode()
        
            if self.button_pressed(self.blue):
                self.green.off()
                self.blue.off()
                self.practice_mode()
    # End def


    def button_pressed(self, goal_button):
        """Unlock the lock.
               - Turn off red LED; Turn on green LED
               - Set servo to open
               - Set display to "----"
        """
        initial_time=time.time()
        while time.time()-initial_time < self.timeout:
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
        """
        """
        print("Learn mode")
        rounds=self.number_rounds() 
        current_round=1
        for i in range(rounds):
            notes_for_round,times_for_round,colors_for_round=self.get_rounds_notes(current_round, rounds)
            note=0
            for i in range(len(notes_for_round)):
                if note > (len(notes_for_round)-1):
                    break
                else:
                    colors_for_round[note].on()
                    time.sleep(times_for_round[note])
                    colors_for_round[note].off()
                    time.sleep(0.1)
                    note=note+1
            current_round=current_round+1
    
    # End def


    def practice_mode(self):
        """
        """
    print("Practice mode")
    # End def


    def number_rounds(self):
        """Execute the main program."""
        number_notes=len(self.notes)
        rounds=math.ceil(number_notes/4)
        return rounds
    # End def


    def get_rounds_notes(self, current_round, rounds):
        """Set display to word "Prog" """
        if current_round == rounds:
            get_current_round_notes=self.notes[(current_round*4-4):len(self.notes)]
        else:
            get_current_round_notes=self.notes[(current_round*4-4):(current_round*4)]
        notes_for_round=[pitch[0] for pitch in get_current_round_notes]
        times_for_round=[time[1] for time in get_current_round_notes]
        colors_for_round=[self.Note_Map[note] for note in notes_for_round if note in self.Note_Map]
        return notes_for_round, times_for_round, colors_for_round
    # End def



    def cleanup(self):
        """Cleanup the hardware components."""
        

    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the lock
    one_handed_piano = OneHandedPiano()

    try:
        # Run the lock
        one_handed_piano.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        one_handed_piano.cleanup()

    print("Program Complete")