# Upwork Job Scraper

A comprehensive web scraper for Upwork jobs with enhanced review extraction capabilities.

## 🆕 New Features

### 1. Login Functionality (NEW!)
The scraper now supports optional Upwork login for enhanced data access:
- **🔓 Optional Authentication**: Works with or without login credentials
- **🔐 Enhanced Data Access**: Login provides access to premium features and detailed information
- **🛡️ Secure Handling**: Credentials are validated and passwords are masked in logs
- **🔄 Automatic Fallback**: Falls back to anonymous mode if login fails
- **🧪 Battle-tested**: Robust error handling and retry mechanisms

**Benefits of Login:**
- ✅ **Payment Verification Status**: See which clients have verified payment methods
- ✅ **Proposal Counts**: Access to number of proposals submitted
- ✅ **Connects Required**: Know how many connects you need to apply
- ✅ **Advanced Filters**: Access to login-only search filters
- ✅ **Higher Rate Limits**: Better performance for large scraping jobs

### 2. Review Scraping
The scraper now extracts detailed client reviews and freelancer feedback from job pages, including:
- **Project Title**: The name of the completed project
- **Overall Project Rating**: Numerical rating and star count for the project
- **Client Review Text**: Full client feedback about the project
- **Freelancer Information**: Name and profile URL of the freelancer
- **Freelancer Rating**: Individual rating and star count for the freelancer
- **Freelancer Comment**: Specific feedback about the freelancer's performance

**Edge Case Handling**: The scraper intelligently handles various review scenarios:
- ✅ **Full Reviews**: Complete feedback with text, ratings, and comments
- ⭐ **Stars Only**: Reviews with only ratings (no written feedback)
- 🚫 **No Feedback Given**: Explicit "No feedback given" cases
- 💬 **Partial Reviews**: Reviews missing some elements (text, comments, or ratings)
- 📋 **Minimal Reviews**: Reviews with just project title and basic info

### 2. Improved CSV Output
- **User-Friendly Column Names**: Technical field names are now converted to readable column names
- **Separate Review Files**: Reviews are saved in a separate CSV file for better organization
- **Enhanced Data Structure**: Better organized and more intuitive data presentation

## 📊 CSV Output Structure

### Jobs CSV (Enhanced with Integrated Reviews)
The scraper now generates a single, comprehensive CSV file containing both job data and review information. **Each review gets its own row**, providing maximum granularity for analysis:

**Job Information (repeated for each review):**
- `Job ID` → `job_id`
- `Job Title` → `title`
- `Job Description` → `description`
- `Job Type` → `type`
- `Project Duration` → `duration`
- `Experience Level` → `level`
- `Fixed Budget Amount` → `fixed_budget_amount`
- `Hourly Rate (Min)` → `hourly_min`
- `Hourly Rate (Max)` → `hourly_max`
- `Required Skills` → `skills`
- `Client Country` → `client_country`
- `Client Total Spent ($)` → `client_total_spent`
- And many more...

**Review Information (unique per row):**
- `Project Title` → Name of the completed project
- `Overall Project Rating` → Project rating (e.g., 5.0)
- `Overall Project Stars` → Number of filled stars
- `Client Review Text` → Full client feedback about the project
- `No Feedback Given` → Flag for "No feedback given" cases
- `Review Text Missing` → Flag for reviews without text (stars only)
- `Freelancer Name` → Name of the freelancer who completed the project
- `Freelancer Profile URL` → Link to freelancer's profile
- `Freelancer Rating` → Individual freelancer rating
- `Freelancer Stars` → Number of freelancer stars
- `Freelancer Comment` → Specific feedback about the freelancer's performance
- `Total Reviews Count` → Number of reviews found for this job
- `Review Number` → Which review this is (1st, 2nd, 3rd, etc.)
- `Is Primary Review` → Flag indicating if this is the first/primary review

## 🚀 Usage

### ✨ **NEW: Interactive Mode** (Easiest!)
Simply run without arguments and follow the prompts:
```bash
python main.py
```
🎯 **This will ask you about login and guide you through configuration step-by-step!**

### Basic Usage (JSON)
```bash
python main.py --jsonInput '{"search": {"query": "AI development", "limit": 10}}'
```

### With Login Credentials (Enhanced Access)
```bash
python main.py --jsonInput '{"credentials": {"username": "your_email@example.com", "password": "your_password"}, "search": {"query": "web development", "limit": 20, "payment_verified": true}}'
```

### API Usage
#### Flask API (with login):
```bash
curl -X POST "http://localhost:8000/run/keyword" \
     -H "Content-Type: application/json" \
     -d '{"query": "python developer", "limit": 25, "username": "your_email@example.com", "password": "your_password"}'
```

#### FastAPI (anonymous):
```bash
curl -X POST "http://localhost:8000/run/keyword" \
     -H "Content-Type: application/json" \
     -d '{"query": "react developer", "limit": 30}'
```

### Environment Variable
```bash
set jsonInput={"search": {"query": "mobile app", "limit": 15}}
python main.py
```

## 📁 Output Files

The scraper generates a single, comprehensive CSV file:
**`job_results_YYYYMMDD_HHMMSS.csv`** - Contains all job data with integrated review information

**Key Benefits of Integration:**
- **Single File Analysis**: All data in one place for easier analysis
- **Direct Correlation**: See job details and reviews side by side
- **Complete Picture**: Understand both job requirements and client satisfaction
- **Easier Sharing**: One file instead of multiple files to manage

## 🔧 Configuration

### Search Parameters
- `query`: Main search term
- `limit`: Maximum number of jobs to scrape
- `category`: Job categories (e.g., "web development", "AI & machine learning")
- `type`: Job type ("hourly" or "fixed")
- `level`: Experience level ("entry", "intermediate", "expert")
- `duration`: Project duration ("less than 1 month", "1 to 3 months", etc.)

### Advanced Filters
- `hourly_min`/`hourly_max`: Hourly rate range
- `fixed_min`/`fixed_max`: Fixed price range
- `client_hires`: Client hiring history
- `payment_verified`: Payment verification status
- `location`: Client location preferences

## 🧪 Testing

### Test Login Functionality
```bash
python test_login.py
```

### Test Review Extraction
```bash
python test_review_extraction.py
```

See `LOGIN_USAGE.md` for comprehensive login documentation and examples.

## 📋 Requirements

- Python 3.8+
- BeautifulSoup4
- Playwright
- Pandas
- Requests
- js2py

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔍 How It Works

1. **Browser Setup**: Uses Playwright with Camoufox for anti-detection
2. **Captcha Solving**: Automatically solves Cloudflare challenges
3. **Job Search**: Searches Upwork based on provided parameters
4. **Data Extraction**: Extracts job details using both JSON and HTML parsing
5. **Review Scraping**: Fetches individual job pages to extract client reviews
6. **Data Integration**: Combines job data and review information into single records
7. **Data Normalization**: Converts technical field names to user-friendly names
8. **CSV Export**: Saves comprehensive data in organized, readable CSV files

## 🎯 Use Cases

- **Market Research**: Analyze job market trends and pricing
- **Competitive Analysis**: Understand client requirements and feedback patterns
- **Lead Generation**: Identify potential clients and their needs
- **Portfolio Building**: Find projects that match your skills
- **Business Intelligence**: Track industry trends and client preferences
- **Client Satisfaction Analysis**: Correlate job requirements with client feedback

## ⚠️ Important Notes

- **Rate Limiting**: The scraper includes delays to avoid overwhelming Upwork's servers
- **Captcha Handling**: Automatically solves Cloudflare challenges
- **Data Accuracy**: Combines multiple data sources for comprehensive information
- **Review Expansion**: Automatically expands truncated review text when possible
- **Integrated Data**: Reviews are now directly integrated into job records for easier analysis

## 📈 Performance

- **Concurrent Processing**: Uses ThreadPoolExecutor for parallel job processing
- **Smart Retries**: Implements retry logic for failed requests
- **Memory Efficient**: Processes data in chunks to handle large datasets
- **Error Handling**: Gracefully handles network issues and parsing errors
- **Unified Output**: Single CSV file reduces file management overhead

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the scraper.

## 📄 License

This project is for educational and research purposes. Please respect Upwork's terms of service and use responsibly.