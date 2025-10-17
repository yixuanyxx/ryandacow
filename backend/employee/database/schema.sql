-- Employee Management System Database Schema
-- This file contains the SQL schema for the employee management system

-- Create the employee table
CREATE TABLE IF NOT EXISTS employee (
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
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_employee_email ON employee(email);
CREATE INDEX IF NOT EXISTS idx_employee_name ON employee(name);
CREATE INDEX IF NOT EXISTS idx_employee_city ON employee(city);
CREATE INDEX IF NOT EXISTS idx_employee_country ON employee(country);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_employee_updated_at 
    BEFORE UPDATE ON employee 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data (optional)
INSERT INTO employee (name, email, phone, address, city, state, zip, country) VALUES
('John Doe', 'john.doe@example.com', '+1-555-0123', '123 Main St', 'New York', 'NY', '10001', 'USA'),
('Jane Smith', 'jane.smith@example.com', '+1-555-0124', '456 Oak Ave', 'Los Angeles', 'CA', '90210', 'USA'),
('Bob Johnson', 'bob.johnson@example.com', '+1-555-0125', '789 Pine Rd', 'Chicago', 'IL', '60601', 'USA')
ON CONFLICT (email) DO NOTHING;
