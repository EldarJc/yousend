import os
import secrets
import random
import string

from django.utils import timezone

from .models import UploadedFile, FileLink, FileKey



class FileUploadHelper:
    
    @staticmethod
    def save_new_file(data, save_method, user=None, url=None):
        file_name = data.name.rsplit(".", 1)

        new_file = UploadedFile(
            name=file_name[0],
            saved_at=data,
            ext=file_name[1],
            mime_type=data.content_type,
            size=data.size
        )

        try:
            new_file.save()
            return FileUploadHelper.generate_access( new_file, save_method, user, url)
        
        except Exception as e:
            new_file.delete()
            return None

    @staticmethod
    def generate_access(file, method, user, url):

        access = None

        if method == "key":
            new_key = FileUploadHelper.generate_key()
            access = FileKey(
                file=file,
                key=new_key
            )

        elif method == "link" and url and user.is_authenticated:
            new_link = FileUploadHelper.generate_link()
            access = FileLink(
                owner=user,
                link=f"{url}/{new_link}",
                file=file,
            )
        
        if access:
            access.save()
            return access.link if method == "link" else access.key
    
        raise ValueError("Invalid save method. Choose 'key' or 'link'.")

    @staticmethod
    def generate_key():
        while True:
            code = secrets.randbelow(900000) + 100000
            if not FileKey.objects.filter(key=code).exists():
                return code

    @staticmethod
    def generate_link():
        while True:
            link = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if not FileLink.objects.filter(link=link).exists():
                return link


class FileDownloadHelper:
    
    @staticmethod
    def get_file_key(key):
        token = FileKey.objects.filter(key=key).first()
        if token:
            return token.file 

    @staticmethod
    def get_file_link(link):
        token =  FileLink.objects.filter(link=link).first().file
        if token:
            return token.file 

class FileHelper:

    @staticmethod
    def get_file(file_uuid):
        return UploadedFile.objects.filter(uuid=file_uuid).first()

    @staticmethod
    def get_user_links(current_user):
        try:
            user_links = FileLink.objects.filter(owner=current_user, file__expires_at__gt=timezone.now())
            return user_links
        
        except Exception as e:
            return None

    @staticmethod
    def delete_file(file_uuid):
        user_file = UploadedFile.objects.filter(uuid=file_uuid).first()
        if user_file:
            user_file.delete()
            return True
        return False

