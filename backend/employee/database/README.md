# Database Setup

This directory contains database-related files for the Employee Management System.

## Database Requirements

**Yes, a database is necessary** for this project because:

1. **Data Persistence**: Employee information needs to be stored permanently
2. **CRUD Operations**: The system requires Create, Read, Update, Delete operations
3. **Data Relationships**: Future features may require relationships between entities
4. **Scalability**: A proper database allows for growth and performance optimization

## Database Options

### Option 1: Supabase (Recommended for Hackathon)
- **Pros**: Easy setup, built-in API, real-time features, free tier
- **Setup**: 
  1. Create account at https://supabase.com
  2. Create new project
  3. Copy URL and service key to `.env` file
  4. Run the schema.sql file in the SQL editor

### Option 2: PostgreSQL (Local Development)
- **Pros**: Full control, no external dependencies
- **Setup**:
  1. Install PostgreSQL locally
  2. Create database: `createdb employee_management`
  3. Run schema: `psql employee_management < schema.sql`

### Option 3: SQLite (Simple Setup)
- **Pros**: No server required, file-based
- **Cons**: Limited for production use
- **Setup**: Modify the repo to use SQLite instead of Supabase

## Quick Start with Supabase

1. Copy `.env.example` to `.env`
2. Fill in your Supabase credentials
3. Run the backend: `python app.py`
4. The system will automatically connect to Supabase

## Schema Overview

The `employee` table includes:
- Basic employee information (name, email, phone)
- Address details (address, city, state, zip, country)
- Timestamps (created_at, updated_at)
- Automatic timestamp updates via triggers

## Sample Data

The schema includes sample employee data for testing purposes.
