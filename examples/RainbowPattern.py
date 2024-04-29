import neopixel
from LEDPattern import LEDPattern


class RainbowPattern(LEDPattern):
    first_hue: int = 0

    def __init__(self) -> None:
        super().__init__()

    def set_leds(self, pixels: neopixel) -> None:
        current_hue: int
        num_pixels: int = pixels.n

        for i in range(num_pixels):
            currentHue = (self.first_hue + (i * 180 / num_pixels)) % 180
            pixels[i] = current_hue

        pixels.show()

        m_firstHue = (m_firstHue + 3) % 180

    def is_animated(self) -> bool:
        return True
