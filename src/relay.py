import machine

class Relay:
    def __init__(self, pin):
        """
        Initializes the Relay object.

        Args:
            pin (int): GPIO pin number where the relay is connected.
        """
        self.relay_pin = machine.Pin(pin, machine.Pin.OUT)
        self.state = False  # Relay is initially off

    def on(self):
        """
        Turns the relay on.
        """
        self.relay_pin.value(1)
        self.state = True
        print(f"Relay on GPIO {self.relay_pin} is ON")

    def off(self):
        """
        Turns the relay off.
        """
        self.relay_pin.value(0)
        self.state = False
        print(f"Relay on GPIO {self.relay_pin} is OFF")

    def toggle(self):
        """
        Toggles the relay state.
        """
        self.state = not self.state
        self.relay_pin.value(1 if self.state else 0)
        state_str = "ON" if self.state else "OFF"
        print(f"Relay on GPIO {self.relay_pin} is {state_str}")

    def is_on(self):
        """
        Checks if the relay is currently on.

        Returns:
            bool: True if the relay is on, False otherwise.
        """
        return self.state
