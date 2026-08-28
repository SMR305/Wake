from django.db import models

# Formatting for Database Attributes
# Note: All fields are required!
# name- Name of a given server. Maximum of 100 characters. Can only contain alphanumeric characters '_' and '-'
# mac_address- Holds the mac address of a given server for the purposes of sending the magic packet to request it to wake up
# ip_address- Holds the ip_address of a given server for the purposes of connecting to them to get confirmations on startup and shutdown as well as for polling
# is_on- Holds the last known active state of the server. "True" indicates on, "False" indicates off, and "None" indicates an uncertain state (usually used while waiting for confirmation of an action)

class Server(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mac_address = models.CharField(max_length=17, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    is_on = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.name
