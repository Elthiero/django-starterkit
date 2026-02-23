#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create Superuser automatically if credentials are provided in the environment
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
email = os.environ.get('SUPERUSER_EMAIL')
password = os.environ.get('SUPERUSER_PASSWORD')

if email and password:
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, password=password)
        print(f'Superuser {email} created successfully!')
    else:
        print(f'Superuser {email} already exists. Skipping creation.')
else:
    print('SUPERUSER_EMAIL or SUPERUSER_PASSWORD not set. Skipping superuser creation.')
"