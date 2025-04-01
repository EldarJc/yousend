import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone

from yousend_auth.models import CustomUser

# Create your models here.

class UploadedFile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    saved_at = models.FileField(upload_to="files/")
    ext = models.CharField(max_length=5)
    mime_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    uploaded_at = models.DateField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)
    

    def __str__(self):
        return f"{self.name} {self.ext} {self.mime_type}"

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timedelta(hours=48)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.saved_at.delete(save=True)
        return super().delete(*args, **kwargs)
    
    @classmethod
    def get_expired_files(cls):
        return cls.objects.filter(expires_at__lte=timezone.now())

    @classmethod
    def delete_expired_files(cls):
        exp_files = cls.get_expired_files()
        if exp_files.exists():
            exp_files.delete()   
        return exp_files.count()


class FileLink(models.Model):
    link = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_files")
    file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE, related_name="link")

    def __str__(self):
        return f"{self.link}"


class FileKey(models.Model):
    key = models.IntegerField(unique=True)
    file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE, related_name="key")

    def __str__(self):
        return f"{self.key}"

