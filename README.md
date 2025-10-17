# Employee Management System

A full-stack employee management system built for the Code Sprint 2025 hackathon (Problem Statement 4).

## Project Structure

```
ryandacow/
├── backend/
│   └── employee/                 # Employee microservice
│       ├── app.py               # Flask application entry point
│       ├── controllers/         # API route handlers
│       ├── models/              # Data models
│       ├── repo/                # Database repository layer
│       ├── services/            # Business logic layer
│       ├── database/            # Database schema and setup
│       ├── requirements.txt     # Python dependencies
│       └── .env.example         # Environment variables template
├── frontend/                    # Vue.js frontend application
│   ├── src/
│   │   ├── components/          # Vue components
│   │   ├── App.vue             # Main application component
│   │   └── main.js             # Application entry point
│   ├── package.json            # Node.js dependencies
│   ├── vite.config.js          # Vite configuration
│   └── index.html              # HTML template
├── hackathon/                   # Hackathon materials
│   ├── Employee_Profiles.json  # Sample employee data
│   ├── Functions & Skills.xlsx # Skills taxonomy
│   └── Code Sprint 2025 Problem Statements.pdf
└── README.md                   # This file
```

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Architecture**: Clean Architecture (Controllers → Services → Repository)
- **API**: RESTful API

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **UI Library**: Vuetify 3
- **HTTP Client**: Axios

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Supabase account (free tier available)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend/employee
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

4. **Set up database**:
   - Create a Supabase project at https://supabase.com
   - Run the SQL schema from `database/schema.sql` in Supabase SQL editor
   - Copy your project URL and service key to `.env`

5. **Run the backend**:
   ```bash
   python app.py
   ```
   Backend will run on http://localhost:5004

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the frontend**:
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:3000

## API Endpoints

### Employee Management
- `GET /employees/` - Get all employees
- `GET /employees/{id}` - Get employee by ID
- `POST /employees/create` - Create new employee
- `PUT /employees/{id}` - Update employee
- `DELETE /employees/{id}` - Delete employee

### Request/Response Format

**Create Employee Request**:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip": "10001",
  "country": "USA"
}
```

**Response Format**:
```json
{
  "Code": 201,
  "Message": "Employee created! Employee ID: 1",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    // ... other fields
  }
}
```

## Database Schema

The system uses a single `employee` table with the following structure:

```sql
employee (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(50) NOT NULL,
  address TEXT NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  zip VARCHAR(20) NOT NULL,
  country VARCHAR(100) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
)
```

## Is a Database Necessary?

**Yes, absolutely!** A database is essential for this project because:

1. **Data Persistence**: Employee information must be stored permanently
2. **CRUD Operations**: Full Create, Read, Update, Delete functionality
3. **Data Integrity**: Proper validation and constraints
4. **Scalability**: Support for multiple users and large datasets
5. **Real-world Application**: Professional systems always require persistent storage

## Development Notes

- The backend follows clean architecture principles
- Frontend uses Vue 3 Composition API with Vuetify for modern UI
- Database includes automatic timestamp updates
- CORS is configured for frontend-backend communication
- Error handling is implemented at all layers

## Hackathon Context

This system is designed for Problem Statement 4 of Code Sprint 2025, focusing on employee management capabilities with a modern, scalable architecture suitable for enterprise use.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational and hackathon purposes.