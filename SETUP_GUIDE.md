# SecureVote - Detailed Setup Guide

This guide provides comprehensive instructions for setting up, configuring, and deploying the SecureVote application.

## 📋 **Prerequisites**

### **System Requirements**
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.11 or higher
- **Memory**: Minimum 2GB RAM
- **Storage**: At least 500MB free space
- **Network**: Internet connection for package installation

### **Software Dependencies**
- Python 3.11+ with pip
- Git (optional, for version control)
- Modern web browser
- Text editor or IDE (VS Code, PyCharm, etc.)

## 🚀 **Installation Steps**

### **Step 1: Extract Project Files**
```bash
# Extract the zip file
unzip SecureVote_Fixed.zip

# Navigate to project directory
cd SecureVote

# Verify project structure
ls -la
```

### **Step 2: Python Environment Setup**

#### **Option A: Using Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv securevote_env

# Activate virtual environment
# On Windows:
securevote_env\Scripts\activate
# On macOS/Linux:
source securevote_env/bin/activate

# Install Django
pip install Django
```

#### **Option B: Global Installation**
```bash
# Install Django globally
pip install Django

# Verify installation
python -m django --version
```

### **Step 3: Database Setup**
```bash
# Navigate to project directory
cd SecureVote

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### **Step 4: Start Development Server**
```bash
# Start the Django development server
python manage.py runserver

# The application will be available at:
# http://localhost:8000
```

## 🔧 **Configuration Options**

### **Basic Configuration**

#### **Settings.py Modifications**
```python
# securevote_project/settings.py

# For production deployment
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Database configuration (PostgreSQL example)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'securevote_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### **OTP Configuration**

#### **SMS Gateway Integration**
To integrate with a real SMS service, modify `core/utils.py`:

```python
# core/utils.py
import requests

def send_otp_sms(mobile_number, otp):
    """
    Send OTP via SMS using your preferred SMS gateway
    """
    # Example using Twilio
    from twilio.rest import Client
    
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=f'Your SecureVote OTP is {otp}. Valid for 10 minutes.',
        from_='+1234567890',  # Your Twilio number
        to=f'+91{mobile_number}'  # Adjust country code as needed
    )
    
    return True

# Alternative: Using any HTTP-based SMS API
def send_otp_sms_http(mobile_number, otp):
    api_url = "https://your-sms-provider.com/api/send"
    payload = {
        'mobile': mobile_number,
        'message': f'Your SecureVote OTP is {otp}. Valid for 10 minutes.',
        'api_key': 'your_api_key'
    }
    
    response = requests.post(api_url, data=payload)
    return response.status_code == 200
```

### **Security Configuration**

#### **Production Security Settings**
```python
# securevote_project/settings.py

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Generate a new secret key for production
SECRET_KEY = 'your-new-secret-key-here'
```

## 🚀 **Deployment Guide**

### **Heroku Deployment**

#### **Step 1: Prepare for Heroku**
```bash
# Install required packages
pip install gunicorn psycopg2-binary whitenoise

# Create requirements.txt
pip freeze > requirements.txt

# Create Procfile
echo "web: gunicorn securevote_project.wsgi" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt
```

#### **Step 2: Configure for Heroku**
```python
# securevote_project/settings.py
import os
import dj_database_url

# Heroku configuration
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'])

# Static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### **Step 3: Deploy to Heroku**
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### **DigitalOcean App Platform**

#### **Step 1: Prepare app.yaml**
```yaml
# app.yaml
name: securevote
services:
- name: web
  source_dir: /
  github:
    repo: your-username/securevote
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm securevote_project.wsgi
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DEBUG
    value: "False"
  - key: SECRET_KEY
    value: "your-secret-key"
databases:
- name: securevote-db
  engine: PG
  version: "13"
```

### **Docker Deployment**

#### **Step 1: Create Dockerfile**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "securevote_project.wsgi"]
```

#### **Step 2: Create docker-compose.yml**
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgres://user:password@db:5432/securevote
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=securevote
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🧪 **Testing & Development**

### **Running Tests**
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### **Development Tools**
```bash
# Install development dependencies
pip install django-debug-toolbar
pip install django-extensions

# Add to INSTALLED_APPS in development
INSTALLED_APPS += ['debug_toolbar', 'django_extensions']
```

### **Database Management**
```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database
python manage.py flush

# Load sample data
python manage.py loaddata fixtures/sample_data.json
```

## 🔍 **Troubleshooting**

### **Common Issues and Solutions**

#### **Issue: Django not found**
```bash
# Solution: Install Django
pip install Django

# Verify installation
python -c "import django; print(django.get_version())"
```

#### **Issue: Database errors**
```bash
# Solution: Run migrations
python manage.py migrate

# If persistent, reset database
rm db.sqlite3
python manage.py migrate
```

#### **Issue: Static files not loading**
```bash
# Solution: Collect static files
python manage.py collectstatic

# For development, ensure DEBUG=True
```

#### **Issue: CSRF token errors**
```bash
# Solution: Clear browser cache and cookies
# Ensure {% csrf_token %} is in all forms
```

#### **Issue: OTP not working**
```bash
# Check server console for OTP codes
# Verify mobile number format (10 digits)
# Ensure session is maintained between requests
```

### **Performance Optimization**

#### **Database Optimization**
```python
# Use select_related for foreign keys
surveys = Survey.objects.select_related('created_by').all()

# Use prefetch_related for many-to-many
surveys = Survey.objects.prefetch_related('options').all()

# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['mobile_number']),
        models.Index(fields=['created_at']),
    ]
```

#### **Caching Configuration**
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Use caching in views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def survey_list(request):
    # View logic here
    pass
```

## 📊 **Monitoring & Maintenance**

### **Logging Configuration**
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'securevote.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### **Health Checks**
```python
# core/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    })
```

### **Backup Strategy**
```bash
# Database backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json

# Media files backup (if applicable)
tar -czf media_backup.tar.gz media/
```

## 🔐 **Security Checklist**

- [ ] Change default admin password
- [ ] Set DEBUG=False in production
- [ ] Configure HTTPS
- [ ] Set secure secret key
- [ ] Enable CSRF protection
- [ ] Configure proper CORS settings
- [ ] Set up rate limiting
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities
- [ ] Implement proper logging

## 📞 **Support & Resources**

### **Documentation**
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

### **Community**
- Django Community Forum
- Stack Overflow (tag: django)
- GitHub Issues

---

This setup guide should help you successfully deploy and configure SecureVote for your specific needs. For additional support, refer to the main README.md file or Django's official documentation.

