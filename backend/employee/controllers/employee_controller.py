from flask import Blueprint, request, jsonify
from services.employee_service import EmployeeService

employee_bp = Blueprint("employees", __name__, url_prefix="/employees")
service = EmployeeService()

@employee_bp.route("/create", methods=["POST"])
def create_employee():
    """
    Create a new employee.
    """
    try:
        data = request.get_json(silent=True) or {}
        result = service.create_employee(data)
        status_code = result.pop("Code", 201)
        return jsonify(result), status_code
    except ValueError as e:
        return jsonify({"Code": 400, "Message": str(e)}), 400
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@employee_bp.route("/", methods=["GET"])
def get_employees():
    """
    Get all employees.
    """
    result = service.get_employees()
    status_code = result.pop("Code", 200)
    return jsonify(result), status_code

@employee_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    """
    Get a specific employee by ID.
    """
    result = service.get_employee_by_id(employee_id)
    status_code = result.pop("Code", 200)
    return jsonify(result), status_code

@employee_bp.route("/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    """
    Update an employee.
    """
    try:
        data = request.get_json(silent=True) or {}
        result = service.update_employee(employee_id, data)
        status_code = result.pop("Code", 200)
        return jsonify(result), status_code
    except ValueError as e:
        return jsonify({"Code": 400, "Message": str(e)}), 400
    except Exception as e:
        return jsonify({"Code": 500, "Message": f"Internal server error: {str(e)}"}), 500

@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    """
    Delete an employee.
    """
    result = service.delete_employee(employee_id)
    status_code = result.pop("Code", 200)
    return jsonify(result), status_code