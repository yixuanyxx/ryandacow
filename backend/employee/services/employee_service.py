from typing import Dict, Any, Optional, List
from datetime import datetime, UTC
from models.employee import Employee
from repo.employee_repo import EmployeeRepo

class EmployeeService:
    def __init__(self, repo: Optional[EmployeeRepo] = None):
        self.repo = repo or EmployeeRepo()

    def create_employee(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new employee.
        Required fields: name, email, phone, address, city, state, zip, country
        """
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'address', 'city', 'state', 'zip', 'country']
        missing_fields = [field for field in required_fields if not payload.get(field)]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Create employee from payload
        employee = Employee(**payload)
        
        # Convert to dictionary for database insertion
        data = {
            'name': employee.name,
            'email': employee.email,
            'phone': employee.phone,
            'address': employee.address,
            'city': employee.city,
            'state': employee.state,
            'zip': employee.zip,
            'country': employee.country,
            'created_at': employee.created_at.isoformat(),
            'updated_at': employee.updated_at.isoformat()
        }

        # Insert into database
        created = self.repo.insert_employee(data)
        return {
            "Code": 201,
            "Message": f"Employee created! Employee ID: {created.get('id')}",
            "data": created
        }

    def get_employees(self) -> Dict[str, Any]:
        """Get all employees."""
        employees = self.repo.find_all()
        if not employees:
            return {
                "Code": 404,
                "Message": "No employees found",
                "data": []
            }
        return {
            "Code": 200,
            "Message": "Success",
            "data": employees
        }

    def get_employee_by_id(self, employee_id: int) -> Dict[str, Any]:
        """Get a single employee by their ID."""
        employee = self.repo.get_employee(employee_id)
        if not employee:
            return {
                "Code": 404,
                "Message": f"Employee with ID {employee_id} not found"
            }
        return {
            "Code": 200,
            "Message": "Success",
            "data": employee
        }

    def update_employee(self, employee_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Update an employee's information."""
        # Check if employee exists
        existing_employee = self.repo.get_employee(employee_id)
        if not existing_employee:
            return {
                "Code": 404,
                "Message": f"Employee with ID {employee_id} not found"
            }

        # Update the employee
        updated_data = {
            **payload,
            "updated_at": datetime.now(UTC).isoformat()
        }
        updated_employee = self.repo.update_employee(employee_id, updated_data)
        
        return {
            "Code": 200,
            "Message": f"Employee {employee_id} updated successfully",
            "data": updated_employee
        }

    def delete_employee(self, employee_id: int) -> Dict[str, Any]:
        """Delete an employee by their ID."""
        # Check if employee exists
        existing_employee = self.repo.get_employee(employee_id)
        if not existing_employee:
            return {
                "Code": 404,
                "Message": f"Employee with ID {employee_id} not found"
            }

        # Delete the employee
        success = self.repo.delete_employee(employee_id)
        if success:
            return {
                "Code": 200,
                "Message": f"Employee {employee_id} deleted successfully"
            }
        else:
            return {
                "Code": 500,
                "Message": f"Failed to delete employee {employee_id}"
            }