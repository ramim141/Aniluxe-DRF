from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="images/profile",
        default="images/profile/user_avatar.png",
    )
  

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"