#!/usr/bin/env python3
"""
Test script for integrated review extraction functionality.

This script tests the new review extraction that adds review data
as columns in the same row as job data.
"""

import sys
import os
import pandas as pd
from pathlib import Path

def test_review_integration():
    """Test the integrated review functionality"""
    print("🧪 Testing Integrated Review Extraction")
    print("=" * 60)
    
    print("\n📋 This test will:")
    print("1. Check if review columns are properly defined")
    print("2. Verify CSV output includes review data") 
    print("3. Show sample review data structure")
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found in current directory")
        return False
    
    try:
        # Import the functions to test
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import main as scraper_main
        
        print("\n✅ Successfully imported scraper functions")
        
        # Test if the new review extraction function exists
        if hasattr(scraper_main, 'extract_reviews_as_job_columns'):
            print("✅ extract_reviews_as_job_columns function found")
        else:
            print("❌ extract_reviews_as_job_columns function not found")
            return False
        
        # Test the review data structure
        sample_html = """
        <div>Client's recent history</div>
        <div>
            <a class="link">AI Learning System MVP Development</a>
            <div>★★★★★ 5.0 He is extremely good person, I have never met more professional and visionary person than him...</div>
            <div>To freelancer: Mateen A.</div>
            <div>Apr 2025 - Aug 2025</div>
            <div>140 hrs @ $25.00/hr</div>
            <div>Billed: $3,813.10</div>
        </div>
        """
        
        print("\n🔍 Testing review extraction with sample data...")
        review_data = scraper_main.extract_reviews_as_job_columns(sample_html, "test123")
        
        print(f"✅ Review extraction completed")
        print(f"   📊 Total reviews found: {review_data.get('total_reviews_count', 0)}")
        
        # Show the review column structure
        print("\n📋 Review Column Structure:")
        review_columns = [k for k in review_data.keys() if k.startswith('client_review_')]
        for col in review_columns[:10]:  # Show first 10 columns
            value = review_data[col]
            if value is not None:
                print(f"   ✅ {col}: {value}")
            else:
                print(f"   ⭕ {col}: None")
        
        if len(review_columns) > 10:
            print(f"   ... and {len(review_columns) - 10} more review columns")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def check_csv_output():
    """Check if recent CSV files contain review columns"""
    print("\n📊 Checking Recent CSV Output")
    print("-" * 40)
    
    # Look for CSV files in the data directory
    csv_dir = Path("data/jobs/csv")
    if not csv_dir.exists():
        print("📁 CSV directory doesn't exist yet - run the scraper first")
        return
    
    # Find the most recent CSV file
    csv_files = list(csv_dir.glob("job_results_*.csv"))
    if not csv_files:
        print("📄 No CSV files found - run the scraper first")
        return
    
    latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
    print(f"📄 Checking latest CSV: {latest_csv.name}")
    
    try:
        df = pd.read_csv(latest_csv)
        
        # Check for review columns
        review_columns = [col for col in df.columns if 'Review' in col]
        
        if review_columns:
            print(f"✅ Found {len(review_columns)} review columns:")
            for col in review_columns[:5]:  # Show first 5
                non_null_count = df[col].notna().sum()
                print(f"   📋 {col}: {non_null_count}/{len(df)} rows have data")
            
            if len(review_columns) > 5:
                print(f"   ... and {len(review_columns) - 5} more review columns")
            
            # Show sample review data
            review_sample = df[review_columns].iloc[0]
            non_null_reviews = review_sample[review_sample.notna()]
            
            if len(non_null_reviews) > 0:
                print(f"\n📝 Sample review data from first job:")
                for col, value in non_null_reviews.head(3).items():
                    print(f"   {col}: {value}")
            else:
                print("\n⚠️ No review data found in sample row")
        else:
            print("❌ No review columns found in CSV")
            print("   Make sure to run the scraper after implementing review integration")
        
        print(f"\n📊 CSV Summary:")
        print(f"   📈 Total jobs: {len(df)}")
        print(f"   📋 Total columns: {len(df.columns)}")
        print(f"   🔍 Review columns: {len(review_columns)}")
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

def show_expected_columns():
    """Show what review columns should be present"""
    print("\n📋 Expected Review Columns")
    print("-" * 40)
    
    expected_columns = [
        "Total Reviews",
        "Review 1 Project", "Review 1 Rating", "Review 1 Stars", "Review 1 Text",
        "Review 1 Freelancer", "Review 1 Date Range", "Review 1 Type", "Review 1 Budget",
        "Review 2 Project", "Review 2 Rating", "Review 2 Stars", "Review 2 Text",
        "Review 2 Freelancer", "Review 2 Date Range", "Review 2 Type", "Review 2 Budget",
        "Review 3 Project", "Review 3 Rating", "Review 3 Stars", "Review 3 Text",
        "Review 3 Freelancer", "Review 3 Date Range", "Review 3 Type", "Review 3 Budget"
    ]
    
    print("✅ The scraper should now include these review columns:")
    for i, col in enumerate(expected_columns, 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n📊 Total: {len(expected_columns)} new review-related columns")
    print("💡 Each job row will now contain review data from the client's history")

def main():
    """Main test function"""
    print("🔍 Integrated Review Extraction Test Suite")
    print("=" * 70)
    
    success = test_review_integration()
    
    if success:
        show_expected_columns()
        check_csv_output()
        
        print("\n" + "=" * 70)
        print("🎯 NEXT STEPS")
        print("=" * 70)
        print("1️⃣ Run the scraper with login: python main.py")
        print("2️⃣ Choose a job search (e.g., 'nlp' or 'python developer')")
        print("3️⃣ Check the generated CSV file in data/jobs/csv/")
        print("4️⃣ Look for the new 'Review 1 Project', 'Review 1 Rating', etc. columns")
        print("5️⃣ Each job row should now contain client review data!")
        
        print("\n💡 WHAT TO EXPECT:")
        print("- Review 1 Project: Name of client's most recent project")
        print("- Review 1 Rating: Star rating (e.g., 5.0)")
        print("- Review 1 Text: Client's feedback text")
        print("- Review 1 Freelancer: Name of freelancer who worked on it")
        print("- Review 1 Date Range: When the project happened")
        print("- Review 1 Budget: Project cost/hourly rate")
        print("- Similar data for Review 2 and Review 3")
        
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed - please check the implementation")

if __name__ == "__main__":
    main()
