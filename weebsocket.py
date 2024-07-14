import os
import sys
import django
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Set your project path and settings module
project_path = "."
project_settings = "auth_system.settings"

# Add project path to sys path
if project_path:
    sys.path.append(project_path)

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", project_settings)

# Initialize Django
django.setup()

# Get channel layer
channel_layer = get_channel_layer()

# Send message to test_channel
async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})

# Receive message from test_channel
ret = async_to_sync(channel_layer.receive)('test_channel')
print(ret)

if ret == {'type': 'hello'}:
    print("Ok: redis is working")
else:
    print("Error: redis not working")
