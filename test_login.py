#!/usr/bin/env python3
"""
Test script for Upwork Job Scraper login functionality.

This script tests both authenticated and anonymous modes to ensure
the login system works correctly.
"""

import asyncio
import json
import sys
import os

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main as scraper_main
from utils.logger import Logger

def test_anonymous_mode():
    """Test scraper in anonymous mode (no credentials)"""
    print("\n" + "="*50)
    print("🧪 TESTING ANONYMOUS MODE")
    print("="*50)
    
    input_data = {
        "credentials": {
            "username": None,
            "password": None
        },
        "search": {
            "query": "python developer",
            "limit": 5  # Small limit for testing
        },
        "general": {
            "save_csv": True
        }
    }
    
    return input_data

def test_authenticated_mode():
    """Test scraper with login credentials"""
    print("\n" + "="*50) 
    print("🧪 TESTING AUTHENTICATED MODE")
    print("="*50)
    
    # Get credentials from user input or environment
    username = os.getenv('UPWORK_USERNAME')
    password = os.getenv('UPWORK_PASSWORD')
    
    if not username or not password:
        print("\n📝 Enter your Upwork credentials for testing:")
        print("   (Or set UPWORK_USERNAME and UPWORK_PASSWORD environment variables)")
        
        if not username:
            username = input("Username/Email: ").strip()
        if not password:
            password = input("Password: ").strip()
    
    if not username or not password:
        print("❌ No credentials provided, skipping authenticated test")
        return None
    
    input_data = {
        "credentials": {
            "username": username,
            "password": password
        },
        "search": {
            "query": "python developer", 
            "limit": 5,  # Small limit for testing
            "payment_verified": True  # This requires login
        },
        "general": {
            "save_csv": True
        }
    }
    
    return input_data

async def run_test(test_name, input_data):
    """Run a single test case"""
    print(f"\n🚀 Running {test_name}...")
    
    try:
        results = await scraper_main.main(input_data)
        
        print(f"✅ {test_name} completed successfully!")
        print(f"   📊 Found {len(results)} jobs")
        
        if results:
            first_job = results[0]
            print(f"   📋 Sample job: {first_job.get('title', 'N/A')}")
            print(f"   💰 Budget: {first_job.get('fixed_budget_amount') or f'${first_job.get('hourly_min', 0)}-${first_job.get('hourly_max', 0)}/hr'}")
            print(f"   🏢 Client: {first_job.get('client_country', 'N/A')}")
            
            # Check for login-only fields
            if input_data["credentials"]["username"]:
                connects = first_job.get('connects_required')
                payment_verified = first_job.get('payment_verified')
                print(f"   🔌 Connects required: {connects if connects is not None else 'N/A'}")
                print(f"   💳 Payment verified: {payment_verified if payment_verified is not None else 'N/A'}")
        
        return True
        
    except Exception as e:
        print(f"❌ {test_name} failed: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🧪 Upwork Job Scraper - Login Functionality Test")
    print("=" * 60)
    
    # Initialize logger
    logger_obj = Logger(level="INFO")  # Use INFO to reduce noise
    scraper_main.logger = logger_obj.get_logger()
    
    test_results = []
    
    # Test 1: Anonymous mode
    print("\n1️⃣ Testing anonymous mode (no login)...")
    anonymous_data = test_anonymous_mode()
    anonymous_result = await run_test("Anonymous Mode", anonymous_data)
    test_results.append(("Anonymous Mode", anonymous_result))
    
    # Test 2: Authenticated mode
    print("\n2️⃣ Testing authenticated mode (with login)...")
    authenticated_data = test_authenticated_mode()
    
    if authenticated_data:
        auth_result = await run_test("Authenticated Mode", authenticated_data)
        test_results.append(("Authenticated Mode", auth_result))
    else:
        test_results.append(("Authenticated Mode", "Skipped"))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, result in test_results:
        if result == True:
            status = "✅ PASSED"
        elif result == False:
            status = "❌ FAILED"
        else:
            status = "⏭️ SKIPPED"
        
        print(f"   {test_name}: {status}")
    
    # Overall result
    passed_tests = sum(1 for _, result in test_results if result == True)
    total_tests = len([r for _, r in test_results if r != "Skipped"])
    
    if total_tests > 0:
        print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Login functionality is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the errors above.")
    else:
        print("\n⚠️ No tests were run.")

if __name__ == "__main__":
    # Check if required modules are available
    try:
        import main
        import utils.logger
    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    
    # Run the tests
    asyncio.run(main())
