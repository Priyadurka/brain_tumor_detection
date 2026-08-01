from django.db import models
from django.contrib.auth.models import User


class MRIImage(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='mri_images/'
    )
    prediction = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.user.username