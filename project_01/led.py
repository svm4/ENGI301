"""
--------------------------------------------------------------------------
LED Driver
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
LED Driver

  This driver is built for LEDs that are connected directly to the processor led_pin 
(i.e. the LED is ON when the output is "High"/"1" and OFF when the output is 
"Low" / "0")

Software API:

  LED(led_pin)
    - Provide led_pin that the LED is connected
    
    is_on()
      - Return a boolean value (i.e. True/False) if the LED is ON / OFF

    on()
      - Turn the LED on

    off()
      - Turn the LED off 
      
    led_cleanup()
      - Cleans up LED by turning it off

"""
import Adafruit_BBIO.GPIO as GPIO

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

class LED():
    """ LED Class """
    led_pin         = None
    on_value        = None
    off_value       = None
    
    def __init__(self, led_pin=None, active_high=True):
        """ Initialize variables and set up the LED """
        if (led_pin == None):
            raise ValueError("led_pin not provided for LED()")
        else:
            self.led_pin = led_pin
        
        # By default the values are determined by the active_high variable
        if active_high:
            self.on_value  = GPIO.HIGH
            self.off_value = GPIO.LOW
        else: 
            self.on_value  = GPIO.LOW
            self.off_value = GPIO.HIGH

        # Initialize the hardware components        
        self._led_setup()
    
    # End def
    
    
    def _led_setup(self):
        """ Setup the hardware components. """
        # Initialize LED

        GPIO.setup(self.led_pin, GPIO.OUT)
        
        self.off()

    # End def


    def is_on(self):
        """ Is the LED on?
        
           Returns:  True  - LED is ON
                     False - LED is OFF
        """
        return GPIO.input(self.led_pin) == self.on_value

    # End def

    
    def on(self):
        """ Turn the LED ON """

        GPIO.output(self.led_pin, self.on_value)
    
    # End def
    
    
    def off(self):
        """ Turn the LED OFF """
        GPIO.output(self.led_pin, self.off_value)
    
    # End def


    def led_cleanup(self):
        """ Cleanup the hardware components. """
        # Turn LED off 
        self.off()
        
    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time

    print("LED Test")

    # Create instantiation of the LED in active high configuration
    led = LED("P2_9")
    
    # Use a Keyboard Interrupt (i.e. "Ctrl-C") to exit the test
    print("Use Ctrl-C to Exit")
    
    try:
        while(1):
            # Turn LED ON
            led.on()
            print("LED ON? {0}".format(led.is_on()))
            time.sleep(1)
            
            # Turn LED OFF
            led.off()
            print("LED ON? {0}".format(led.is_on()))
            time.sleep(1)
        
    except KeyboardInterrupt:
        pass

    print("Test Complete")

