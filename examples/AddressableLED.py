import time
import asyncio
import neopixel
from LEDPattern import LEDPattern
from SolidPattern import SolidPattern


class AddressableLED:

    pattern:LEDPattern = SolidPattern((255, 0, 0))
    pixels:neopixel

    def __init__(self, pin: int, length: int):
        self.pixels = neopixel.NeoPixel(
            pin, length, brightness=0.2, auto_write=False, pixel_order=neopixel.RGBW
        )
    
    @property
    def get_led(self):
        return self.pixels
    
    @property
    def set_led(self, pixels:neopixel):
        self.pixels = pixels

    @property
    def set_pattern(self, pattern:LEDPattern):
        if (pattern != self.pattern):
            self.pattern = pattern
            #set the first one pattern
            self.pattern.set_leds(self.pixels)
            # if this is an animated pattern the animation will get triggered each time
            # update() is called.
        
    def update(self) -> None:
        # if the pattern is animated cycle the animation
        if(self.pattern.is_animated):
            self.pattern.set_leds(self.pixels)
            