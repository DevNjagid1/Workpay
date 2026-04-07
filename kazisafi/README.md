# Kazi Safi - Employee Management System

A comprehensive Django-based employee management system with attendance tracking, earnings calculation, and withdrawal management.

## 🚀 Features

- **Employee Management**: Complete CRUD operations for employee profiles
- **Attendance System**: Check-in/check-out with automatic work hours calculation
- **Earnings Calculator**: Dynamic earnings based on work hours and overtime
- **Withdrawal System**: M-Pesa integration for salary withdrawals
- **Support Tickets**: Categorized support system for employee issues
- **Admin Dashboard**: Real-time statistics and management interface
- **User Dashboard**: Personal attendance and earnings overview
- **Role-Based Access**: Admin and employee user roles

## 🛠️ Tech Stack

- **Backend**: Django 4.x with Python 3.x
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Authentication**: Django's built-in auth system
- **API**: RESTful endpoints for AJAX operations

## 📋 Prerequisites

- Python 3.8+
- Django 4.0+
- Node.js (for frontend tools, optional)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DevNjagid1/Workpay.git
cd Workpay
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup

```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### 6. Load Initial Data (Optional)

```bash
# Load sample data for testing
python manage.py seed_data
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 🎯 Default Credentials

After running `createsuperuser`, use:
- **Admin**: Username and password you created
- **Employee**: Register through the web interface

## 📁 Project Structure

```
Workpay/
├── kazisafi/                 # Main Django project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── main/                    # Main application
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files (CSS, JS, images)
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript files
│   │   └── images/        # Image assets
│   ├── templates/           # HTML templates
│   │   └── html/          # Template files
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # Application configuration
│   ├── forms.py            # Django forms
│   ├── models.py           # Database models
│   ├── tests.py            # Unit tests
│   ├── urls.py             # Application URLs
│   └── views.py            # View functions
├── requirements.txt         # Python dependencies
├── manage.py             # Django management script
└── README.md             # This file
```

## 🎮 Management Commands

### Database Operations

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush
```

### User Management

```bash
# Create superuser
python manage.py createsuperuser

# Create employee with custom command
python manage.py create_employee --username "johndoe" --email "john@example.com"

# Seed sample data
python manage.py seed_data
```

### Development Server

```bash
# Start development server
python manage.py runserver

# Start on specific port
python manage.py runserver 8080

# Start with specific host
python manage.py runserver 0.0.0.0.0:8000
```

### Django Shell

```bash
# Open Django shell for testing
python manage.py shell

# Run specific command in shell
python manage.py shell -c "from main.models import User; print(User.objects.count())"
```

## 🔧 Configuration

### Settings Overview

Key settings in `kazisafi/settings.py`:

```python
# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
DEBUG = os.environ.get('DEBUG', 'False')
```

### Production Deployment

For production deployment:

1. **Set Environment Variables**:
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Use Production Database**:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'kazisafi_db',
           'USER': 'kazisafi_user',
           'PASSWORD': 'your-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test main

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage

The project includes tests for:
- User authentication and registration
- Attendance marking and approval
- Earnings calculations
- Withdrawal processing
- Support ticket system

## 📊 API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/register/` - User registration
- `POST /api/logout/` - User logout

### Attendance
- `POST /api/mark-attendance/` - Mark attendance
- `POST /api/approve-attendance/` - Approve attendance
- `POST /api/reject-attendance/` - Reject attendance
- `GET /api/user-attendance-history/` - Get attendance history

### Withdrawals
- `POST /api/process-withdrawal/` - Process withdrawal
- `GET /api/user-withdrawal-history/` - Get withdrawal history
- `GET /api/withdrawal-status/<id>/` - Get withdrawal status

### Support
- `POST /api/contact-admin/` - Submit support ticket
- `GET /api/support-tickets/` - Get support tickets

## 🎨 Frontend Features

### Responsive Design
- Mobile-first approach
- Breakpoints: 768px, 1024px, 1280px
- CSS Grid and Flexbox layouts

### JavaScript Features
- AJAX form submissions
- Real-time updates
- Client-side validation
- Dynamic content loading

### Browser Support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🔒 Security Features

### Authentication
- Password hashing with Django's built-in security
- CSRF protection on all forms
- Session management
- Role-based access control

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Secure file uploads

## 📈 Performance

### Optimization
- Database query optimization
- Static file compression
- Image optimization
- Lazy loading for large datasets

### Caching
- Template caching
- Database query caching
- Static file caching

## 🚀 Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-production-secret
    volumes:
      - .:/app
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: kazisafi_db
      POSTGRES_USER: kazisafi_user
      POSTGRES_PASSWORD: your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Traditional Deployment

```bash
# Using Gunicorn
pip install gunicorn
gunicorn kazisafi.wsgi:application --bind 0.0.0.0:8000

# Using Nginx (reverse proxy)
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🐛 Troubleshooting

### Common Issues

**Migration Errors**:
```bash
# If migrations fail, check for conflicts
python manage.py makemigrations --merge
python manage.py migrate
```

**Static Files Not Loading**:
```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**Database Connection Issues**:
```bash
# Check database configuration
python manage.py dbshell --database=default

# Reset database if needed
rm db.sqlite3
python manage.py migrate
```

### Debug Mode

Enable debug mode for development:

```python
# In settings.py
DEBUG = True

# Or via environment variable
export DEBUG=True
python manage.py runserver
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python manage.py test`
5. Commit changes: `git commit -m "Add feature"`
6. Push to branch: `git push origin feature-name`
7. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For support and questions:
- Create an issue in the GitHub repository
- Email: support@kazisafi.com
- Documentation: [Link to documentation if available]

## 🔄 Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added work hours calculation and earnings system
- **v1.2.0** - Enhanced support ticket system and UI improvements

---

**Built with ❤️ for efficient employee management**
