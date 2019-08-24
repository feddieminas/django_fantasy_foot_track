from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Donate(models.Model):
    user = models.ForeignKey(User, null=True)
    donation = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return "User {0} - Donation {1}".format(self.user, self.donation)      