import neopixel
from LEDPattern import LEDPattern


class SolidPattern(LEDPattern):
    color:tuple[int,int,int] = (255, 0, 0)

    def __init__(self, color:tuple[int,int,int]) -> None:
        super().__init__()
        self.color = color

    def set_leds(self, pixels: neopixel) -> None:
        pixels.fill(self.color)
        pixels.show()

    def is_animated(self) -> bool:
        return False
