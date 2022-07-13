import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_project.settings")
django.setup()

from api.models import User
from api.data import data
from api.serializers import UserSerializer

User.objects.all().delete()
serializer = UserSerializer(data=data, many=True)
serializer.is_valid(raise_exception=True)
serializer.save()