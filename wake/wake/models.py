from django.db import models

# This is the model for the states of the Servers that are connected
class ServerState(models.Model):
    # Only one row will be used in this example
    button_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Button Enabled: {self.button_enabled}"
