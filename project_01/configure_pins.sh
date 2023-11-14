#!/bin/bash
# --------------------------------------------------------------------------
# One-Handed Piano - Configure Pins
# --------------------------------------------------------------------------
# License:   
# Copyright 2023 - Shannon McGill
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------------
# 
# Configure pins for One-Handed Piano:
#   - Arcade Buttons (GPIO)
#   - LEDs (GPIO)
#   - Buzzer (PWM)
#   - Touchscreen (SPI1)
# 
# --------------------------------------------------------------------------

# USB Speaker, Use USB1 dedicated pins

# Arcade Buttons, GPIO
config-pin P2_02 gpio
config-pin P2_04 gpio
config-pin P2_06 gpio
config-pin P2_08 gpio
config-pin P2_10 gpio

# LEDs, GPIO
config-pin P2_01 gpio
config-pin P2_03 gpio
config-pin P2_05 gpio
config-pin P2_07 gpio
config-pin P2_09 gpio

# Buzzer, PWM1A
config-pin P1_36 pwm

# Touchscreen, SPI1
config-pin P2_25 spi
config-pin P2_27 spi
config-pin P2_29 spi_sclk
config-pin P2_31 gpio
config-pin P2_17 gpio
config-pin P2_19 gpio