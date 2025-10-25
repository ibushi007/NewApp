from django.db import models

# Create your models here.
class Dataset(models.Model):
    name = models.CharField(max_length=200)
    csv_file = models.FileField(upload_to = '')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __self__(self):
        return self.name