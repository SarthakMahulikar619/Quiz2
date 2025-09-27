# Employee Data Generation & Visualization

A comprehensive Django REST Framework application for employee data management, analytics, and visualization.

## Features

### Core Functionality
- **Employee Management**: Complete employee lifecycle management
- **Department & Position Management**: Organizational structure management
- **Attendance Tracking**: Employee attendance and hours tracking

### API Features
- **RESTful APIs**: Full CRUD operations for all entities
- **Authentication**: Token-based authentication
- **Filtering & Pagination**: Advanced filtering and pagination support
- **Analytics Endpoints**: Comprehensive analytics and reporting
- **Rate Limiting**: Built-in throttling for API protection
- **Swagger Documentation**: Interactive API documentation

### Visualization
- **Interactive Dashboard**: Real-time analytics dashboard
- **Chart.js Integration**: Beautiful charts and graphs
- **Data Export**: CSV/Excel export capabilities
- **Responsive Design**: Mobile-friendly interface

### Technical Features
- **PostgreSQL Database**: Robust data storage
- **Environment Configuration**: Secure configuration management
- **Health Checks**: System health monitoring
- **Logging**: Comprehensive logging system

## Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 15+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd employee_data_generation_and_visualization
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   python manage.py generate_data --employees 5
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Web Dashboard: http://localhost:8000
   - API Documentation: http://localhost:8000/swagger/
   - Django Admin: http://localhost:8000/admin/

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Get authentication token

### Employee Management
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/analytics/` - Employee analytics

### Department Management
- `GET /api/departments/` - List departments
- `POST /api/departments/` - Create department
- `GET /api/departments/{id}/employees/` - Department employees

### Position Management
- `GET /api/positions/` - List positions
- `POST /api/positions/` - Create position
- `GET /api/positions/{id}/employees/` - Position employees

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Create attendance record
- `GET /api/attendance/analytics/` - Attendance analytics

### System
- `GET /health/` - Health check endpoint

## Data Models

### Employee
- Personal information (name, email, phone, address)
- Employment details (position, salary, hire date)
- Emergency contact information
- System metadata

### Department
- Department name and description
- Budget information
- Timestamps

### Position
- Job title and level
- Department association
- Base salary information

### Attendance
- Employee attendance tracking
- Check-in/check-out times
- Hours worked calculation
- Status tracking (present, absent, sick leave, etc.)


## Analytics & Visualization

### Dashboard Features
- Employee statistics overview
- Department distribution charts
- Attendance status visualization
- Salary distribution visualization

### Analytics Endpoints
- Employee analytics: Total employees, department distribution, salary averages
- Attendance analytics: Attendance rates, hours worked, status distribution

## Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=employee_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
The application uses PostgreSQL by default. Update the `DATABASES` setting in `settings.py` for different database configurations.

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Install development dependencies
pip install flake8 black isort

# Format code
black .
isort .

# Lint code
flake8
```

### Data Generation
```bash
# Generate sample data
python manage.py generate_data --employees 10

# Clear existing data
python manage.py generate_data --clear --employees 5
```

## Deployment

### Production Deployment
1. Set `DEBUG=False` in environment variables
2. Configure production database
3. Set up static file serving
4. Configure web server (Apache/Nginx)
5. Set up SSL certificates

## API Usage Examples

### Authentication
```bash
# Get authentication token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Get Employees
```bash
# List all employees
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/employees/

# Get employee analytics
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/employees/analytics/
```

### Create Employee
```bash
curl -X POST http://localhost:8000/api/employees/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "position": 1,
    "salary": "75000.00"
  }'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/swagger/`
- Review the Django admin at `/admin/`

## Changelog

### Version 1.0.0
- Initial release
- Complete employee management system
- REST API with authentication
- Analytics and visualization dashboard
- Comprehensive documentation
