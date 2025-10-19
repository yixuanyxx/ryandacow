#!/usr/bin/env python3
"""
Test script for PSA Workforce AI MVP endpoints
Tests user-management and recommendations microservices
"""

import requests
import json
import sys
import time

# Configuration
BASE_URLS = {
    "user_management": "http://localhost:5001",
    "recommendations": "http://localhost:5004"
}

# Demo user credentials - Note: These users need to exist in your Supabase database
DEMO_USERS = [
    {
        "email": "samantha.lee@globalpsa.com",
        "password": "demo123",
        "user_id": "EMP-20001",
        "name": "Samantha Lee",
        "job_title": "Cloud Solutions Architect"
    },
    {
        "email": "aisyah.rahman@globalpsa.com", 
        "password": "demo123",
        "user_id": "EMP-20002",
        "name": "Nur Aisyah Binte Rahman",
        "job_title": "Cybersecurity Analyst"
    },
    {
        "email": "rohan.mehta@globalpsa.com",
        "password": "demo123", 
        "user_id": "EMP-20003",
        "name": "Rohan Mehta",
        "job_title": "Finance Manager (FP&A)"
    }
]

# Departments to test
DEPARTMENTS = ["Information Technology", "Finance", "Human Resource"]

def test_endpoint(method, url, headers=None, data=None, timeout=10):
    """Test an endpoint and return response"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return {
            "status_code": response.status_code,
            "data": response.json() if response.content else None,
            "success": response.status_code < 400,
            "headers": dict(response.headers)
        }
    except requests.exceptions.ConnectionError:
        return {
            "status_code": 0,
            "data": {"error": "Connection refused - Service not running"},
            "success": False
        }
    except requests.exceptions.Timeout:
        return {
            "status_code": 0,
            "data": {"error": "Request timeout"},
            "success": False
        }
    except Exception as e:
        return {
            "status_code": 0,
            "data": {"error": str(e)},
            "success": False
        }

def check_service_health():
    """Check if services are running"""
    print("🔍 Checking service health...")
    
    services_status = {}
    
    # Test user management service
    try:
        response = requests.get(f"{BASE_URLS['user_management']}/", timeout=5)
        services_status["user_management"] = True
        print("✅ User Management service is responding")
    except:
        services_status["user_management"] = False
        print("❌ User Management service is not responding")
    
    # Test recommendations service  
    try:
        response = requests.get(f"{BASE_URLS['recommendations']}/", timeout=5)
        services_status["recommendations"] = True
        print("✅ Recommendations service is responding")
    except:
        services_status["recommendations"] = False
        print("❌ Recommendations service is not responding")
    
    return services_status

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("🔐 Testing Authentication Endpoints")
    print("=" * 50)
    
    for user in DEMO_USERS:
        print(f"\n📧 Testing login for: {user['email']}")
        
        # Test login
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        
        result = test_endpoint(
            "POST",
            f"{BASE_URLS['user_management']}/auth/login",
            data=login_data
        )
        
        if result["success"]:
            print(f"✅ Login successful")
            print(f"   User: {result['data']['data']['user']['name']}")
            print(f"   Job Title: {result['data']['data']['user']['job_title']}")
            print(f"   Department: {result['data']['data']['user']['department']}")
            
            # Test profile endpoint
            token = result['data']['data']['token']
            headers = {"Authorization": f"Bearer {token}"}
            
            profile_result = test_endpoint(
                "GET",
                f"{BASE_URLS['user_management']}/auth/profile",
                headers=headers
            )
            
            if profile_result["success"]:
                print(f"✅ Profile retrieved successfully")
                print(f"   Skills count: {len(profile_result['data']['data']['skills'])}")
            else:
                print(f"❌ Profile failed: {profile_result['data']}")
        else:
            print(f"❌ Login failed: {result['data']}")

def test_user_endpoints():
    """Test user management endpoints"""
    print("\n👥 Testing User Management Endpoints")
    print("=" * 50)
    
    # Test get user by ID
    for user in DEMO_USERS:
        print(f"\n👤 Testing get user: {user['user_id']}")
        
        result = test_endpoint(
            "GET",
            f"{BASE_URLS['user_management']}/users/{user['user_id']}"
        )
        
        if result["success"]:
            print(f"✅ User retrieved successfully")
            print(f"   Name: {result['data']['data']['user']['name']}")
            print(f"   Job Title: {result['data']['data']['user']['job_title']}")
            print(f"   Skills: {len(result['data']['data']['skills'])}")
        else:
            print(f"❌ User retrieval failed: {result['data']}")
    
    # Test get users by department
    departments = ["Information Technology", "Finance", "Human Resource"]
    for dept in departments:
        print(f"\n🏢 Testing get users by department: {dept}")
        
        result = test_endpoint(
            "GET",
            f"{BASE_URLS['user_management']}/users/department/{dept}"
        )
        
        if result["success"]:
            print(f"✅ Department users retrieved successfully")
            print(f"   Count: {len(result['data']['data'])}")
        else:
            print(f"❌ Department users retrieval failed: {result['data']}")

def test_recommendations_endpoints():
    """Test recommendations endpoints"""
    print("\n🎯 Testing Recommendations Endpoints")
    print("=" * 50)
    
    for user in DEMO_USERS:
        print(f"\n🎯 Testing recommendations for: {user['user_id']}")
        
        # Test general recommendations
        result = test_endpoint(
            "GET",
            f"{BASE_URLS['recommendations']}/recommendations/{user['user_id']}"
        )
        
        if result["success"]:
            print(f"✅ Recommendations retrieved successfully")
            recommendations = result['data']['data']['recommendations']
            print(f"   Recommendations count: {len(recommendations)}")
            for rec in recommendations:
                print(f"   - {rec['type']}: {rec['title']} (Score: {rec['match_score']})")
        else:
            print(f"❌ Recommendations failed: {result['data']}")
        
        # Test course recommendations
        course_result = test_endpoint(
            "GET",
            f"{BASE_URLS['recommendations']}/recommendations/courses/{user['user_id']}"
        )
        
        if course_result["success"]:
            print(f"✅ Course recommendations retrieved successfully")
            courses = course_result['data']['data']
            print(f"   Courses count: {len(courses)}")
            for course in courses:
                print(f"   - {course['title']} (Score: {course['match_score']})")
        else:
            print(f"❌ Course recommendations failed: {course_result['data']}")
        
        # Test mentor recommendations
        mentor_result = test_endpoint(
            "GET",
            f"{BASE_URLS['recommendations']}/recommendations/mentors/{user['user_id']}"
        )
        
        if mentor_result["success"]:
            print(f"✅ Mentor recommendations retrieved successfully")
            mentors = mentor_result['data']['data']
            print(f"   Mentors count: {len(mentors)}")
            for mentor in mentors:
                print(f"   - {mentor['name']} ({mentor['job_title']}) (Score: {mentor['match_score']})")
        else:
            print(f"❌ Mentor recommendations failed: {mentor_result['data']}")

def test_api_structure():
    """Test API structure and document responses"""
    print("\n📋 API Structure Testing")
    print("=" * 50)
    
    # Test with first available user
    test_user = DEMO_USERS[0]
    
    print(f"\n🧪 Testing API structure with user: {test_user['user_id']}")
    
    # Test login endpoint structure
    print("\n1️⃣ Testing Login Endpoint Structure:")
    login_data = {"email": test_user["email"], "password": test_user["password"]}
    result = test_endpoint("POST", f"{BASE_URLS['user_management']}/auth/login", data=login_data)
    
    if result["success"]:
        print("✅ Login endpoint working")
        print(f"   Response structure: {json.dumps(result['data'], indent=2)}")
    else:
        print("❌ Login endpoint failed")
        print(f"   Error: {result['data']}")
        print("   Note: User may not exist in Supabase database")
    
    # Test user profile endpoint structure
    print("\n2️⃣ Testing User Profile Endpoint Structure:")
    result = test_endpoint("GET", f"{BASE_URLS['user_management']}/users/{test_user['user_id']}")
    
    if result["success"]:
        print("✅ User profile endpoint working")
        print(f"   Response structure: {json.dumps(result['data'], indent=2)}")
    else:
        print("❌ User profile endpoint failed")
        print(f"   Error: {result['data']}")
        print("   Note: User may not exist in Supabase database")
    
    # Test recommendations endpoint structure
    print("\n3️⃣ Testing Recommendations Endpoint Structure:")
    result = test_endpoint("GET", f"{BASE_URLS['recommendations']}/recommendations/{test_user['user_id']}")
    
    if result["success"]:
        print("✅ Recommendations endpoint working")
        print(f"   Response structure: {json.dumps(result['data'], indent=2)}")
    else:
        print("❌ Recommendations endpoint failed")
        print(f"   Error: {result['data']}")
        print("   Note: User may not exist in Supabase database")

def generate_curl_commands():
    """Generate curl commands for manual testing"""
    print("\n🔧 Manual Testing Commands")
    print("=" * 50)
    
    test_user = DEMO_USERS[0]
    
    print("\n📋 Copy these commands to test manually:")
    print("\n1. Login:")
    print(f"""curl -X POST http://localhost:5001/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{{"email":"{test_user['email']}","password":"{test_user['password']}"}}'""")
    
    print("\n2. Get User Profile:")
    print(f"""curl http://localhost:5001/users/{test_user['user_id']}""")
    
    print("\n3. Get Department Users:")
    print(f"""curl http://localhost:5001/users/department/Information%20Technology""")
    
    print("\n4. Get Recommendations:")
    print(f"""curl http://localhost:5004/recommendations/{test_user['user_id']}""")
    
    print("\n5. Get Course Recommendations:")
    print(f"""curl http://localhost:5004/recommendations/courses/{test_user['user_id']}""")
    
    print("\n6. Get Mentor Recommendations:")
    print(f"""curl http://localhost:5004/recommendations/mentors/{test_user['user_id']}""")

def main():
    """Main test function"""
    print("🚀 PSA Workforce AI MVP - Endpoint Testing")
    print("=" * 60)
    
    # Check if services are running
    services_status = check_service_health()
    
    if not services_status["user_management"]:
        print("\n❌ User Management service is not running")
        print("   Please start with: cd user-management && python3 app.py")
        return
    
    if not services_status["recommendations"]:
        print("\n❌ Recommendations service is not running")
        print("   Please start with: cd recommendations && python3 app.py")
        return
    
    print("\n" + "=" * 60)
    
    # Run tests
    test_api_structure()
    generate_curl_commands()
    
    print("\n" + "=" * 60)
    print("🎉 Testing completed!")
    print("\n📝 Summary:")
    print("   - API structure tested and documented")
    print("   - Manual testing commands generated")
    print("   - Check API.md for complete documentation")
    print("   - Ensure users exist in Supabase database for full functionality")

if __name__ == "__main__":
    main()
