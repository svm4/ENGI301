"""
--------------------------------------------------------------------------
Color Button Library
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

Color Button Library

  This library is built to link a colored LED with a button for the arcade
buttons in my project.

Software API:

  ColorButton(button_pin,led_pin)
    - Provide pins that the LED and button are connected to
    
    button_cleanup()
      - Cleans up button by turning off LED

"""
import threaded_button 
import led 

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

class ColorButton(threaded_button.ThreadedButton, led.LED):
    """ Color Button Class """
    
    def __init__(self, button_pin, led_pin):
        """ Initialize variables and set up Color Buttons """
        threaded_button.ThreadedButton.__init__(self, button_pin, 0.1, True)
        led.LED.__init__(self, led_pin, True)
    # End def
    
    def button_cleanup(self):
        """ Cleanup function to turn off LED """
        led.LED.led_cleanup(self)
    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == "__main__":
# Test code to check if the button flashes on and off properly
  coloredbutton=ColorButton("P2_2","P2_1")
  coloredbutton.on()
  import time
  time.sleep(1)
  coloredbutton.off()
  
