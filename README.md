# SecureVote - Online Voting & Survey Platform

![SecureVote Logo](https://img.shields.io/badge/SecureVote-Online%20Voting%20Platform-blue?style=for-the-badge&logo=vote&logoColor=white)

A secure, responsive web application for conducting online voting and surveys with mobile OTP verification. Built with Django and Bootstrap for a modern, user-friendly experience.

## 🚀 Features

### ✅ **Core Functionality**
- **Mobile OTP Verification**: Secure 2-step user verification process
- **One Vote Per User**: Prevents duplicate voting through mobile verification
- **Survey Management**: Complete admin panel for creating and managing surveys
- **Real-time Results**: Interactive charts and live vote counting
- **Responsive Design**: Mobile-first design that works on all devices
- **Admin Dashboard**: Comprehensive admin interface with analytics

### 🔐 **Security Features**
- CSRF token protection on all forms
- Session-based authentication
- Input sanitization and validation
- Admin route protection
- SQL injection prevention
- Secure OTP generation and verification

### 📱 **User Experience**
- Beautiful welcome page with clear call-to-action
- Simple 2-step mobile verification process
- Intuitive survey listing and voting interface
- Interactive results visualization with Chart.js
- Fully responsive across all devices
- Progress indicators and loading states

## 🛠️ **Technical Stack**

- **Backend**: Django 5.2.4
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5.3.0, HTML5, CSS3, JavaScript
- **Charts**: Chart.js for interactive data visualization
- **Icons**: Font Awesome 6.0
- **Authentication**: Django sessions with OTP verification
- **Testing**: Django test framework

## 📋 **Requirements**

- Python 3.11+
- Django 5.2.4
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 **Quick Start**

### 1. **Extract and Setup**
```bash
# Extract the project files
unzip SecureVote_Fixed.zip
cd SecureVote

# Install Django (only requirement)
pip install Django
```

### 2. **Run the Application**
```bash
# Start the development server
python manage.py runserver

# Open your browser and visit
http://localhost:8000
```

### 3. **Admin Access**
```bash
# Access Django admin panel
http://localhost:8000/admin/

# Default admin credentials:
Username: admin
Password: admin123
```

## 📖 **User Guide**

### **For Voters:**

1. **Welcome Page**: Visit the homepage and click "Get Started"
2. **Registration**: Enter your full name and mobile number
3. **OTP Verification**: 
   - Click "Send OTP" to receive a verification code
   - Check the server console for the OTP (in development mode)
   - Enter the 6-digit OTP and click "Verify OTP"
4. **Survey Participation**: Browse available surveys and cast your vote
5. **View Results**: Check real-time results with interactive charts

### **For Administrators:**

1. **Admin Dashboard**: Access via the admin panel or direct URL
2. **Create Surveys**: Use the survey creation form with multiple options
3. **Manage Surveys**: View, activate/deactivate surveys
4. **Monitor Analytics**: Track participation and voting statistics
5. **View Results**: Access detailed voting results and charts

## 🔧 **Configuration**

### **Development Settings**
The application comes pre-configured for development with:
- SQLite database
- Debug mode enabled
- Console-based OTP logging
- CSRF protection enabled
- Static files serving

### **Production Deployment**
For production deployment, update `settings.py`:
- Set `DEBUG = False`
- Configure PostgreSQL database
- Set up real SMS gateway for OTP sending
- Configure static files serving
- Set secure secret key
- Enable HTTPS

## 📁 **Project Structure**

```
SecureVote/
├── core/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View controllers
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   └── utils.py           # Utility functions
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── welcome.html       # Landing page
│   ├── home.html          # OTP verification
│   ├── survey_list.html   # Survey listing
│   ├── vote.html          # Voting interface
│   ├── results.html       # Results display
│   ├── create_survey.html # Survey creation
│   └── admin_dashboard.html # Admin panel
├── static/                # Static files (auto-generated)
├── securevote_project/    # Django project settings
├── manage.py              # Django management script
├── db.sqlite3             # Database file
└── README.md              # This file
```

## 🧪 **Testing**

### **Manual Testing**
1. **OTP Flow**: Test complete user registration and verification
2. **Voting**: Create surveys and test voting functionality
3. **Admin Panel**: Test survey management and analytics
4. **Responsive Design**: Test on different screen sizes

### **Automated Testing**
```bash
# Run Django tests
python manage.py test
```

## 🔍 **Troubleshooting**

### **Common Issues**

**OTP Not Working:**
- Check server console for OTP codes (development mode)
- Ensure mobile number is 10 digits
- Verify CSRF tokens are included in forms

**Page Not Loading:**
- Ensure Django server is running
- Check for any error messages in console
- Verify URL patterns are correct

**Admin Access Issues:**
- Use default credentials: admin/admin123
- Create new superuser if needed: `python manage.py createsuperuser`

**Database Issues:**
- Run migrations: `python manage.py migrate`
- Reset database if needed: Delete `db.sqlite3` and run migrations

## 🚀 **Deployment Options**

### **Local Development**
- Use built-in Django development server
- SQLite database for simplicity
- Console-based OTP for testing

### **Production Deployment**
- **Heroku**: Ready for Heroku deployment
- **DigitalOcean**: Compatible with App Platform
- **AWS**: Can be deployed on EC2 or Elastic Beanstalk
- **Docker**: Dockerfile can be added for containerization

## 🔐 **Security Considerations**

- Change default admin password in production
- Set up real SMS gateway for OTP sending
- Enable HTTPS in production
- Configure proper database security
- Set up monitoring and logging
- Regular security updates

## 📞 **Support**

For technical support or questions:
- Check the troubleshooting section above
- Review Django documentation for advanced configuration
- Ensure all requirements are properly installed

## 📄 **License**

This project is created for demonstration purposes. Feel free to modify and use according to your needs.

## 🎯 **Key Fixes Applied**

### **OTP Verification Issues Fixed:**
1. ✅ **Page Redirection**: Fixed OTP verification to properly redirect to survey list
2. ✅ **OTP Generation**: Implemented proper OTP generation and logging
3. ✅ **Session Management**: Corrected user session handling after verification
4. ✅ **CSRF Protection**: Added proper CSRF token handling
5. ✅ **Form Validation**: Enhanced form validation and error handling

### **Additional Improvements:**
- Enhanced responsive design
- Improved user experience with progress indicators
- Added comprehensive error handling
- Optimized database queries
- Enhanced security measures

---

**SecureVote** - Your voice matters. Vote securely, vote confidently. 🗳️

