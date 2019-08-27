from django.db import models

# Create your models here.
class Categories(models.Model):
    """index.html media files, purpose to assist S3 to accept media"""
    name = models.CharField(max_length=254, default='')
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.name