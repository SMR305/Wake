from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mac_address = models.CharField(max_length=17, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True, unique=True)
    is_on = models.BooleanField(default=False)

    def __str__(self):
        return self.name
