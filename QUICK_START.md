# 🚀 Quick Start Guide - Interactive Login

## The Easiest Way to Use the Upwork Job Scraper

Just run the scraper without any arguments and follow the interactive prompts!

```bash
python main.py
```

## What You'll See

### 1. **Login Options** (NEW!)
```
🔍 Upwork Job Scraper - Interactive Mode
==================================================

🔐 LOGIN OPTIONS
------------------------------
The scraper can work in two modes:
   🚫 Anonymous Mode: Basic job data (no login required)
   🔓 Authenticated Mode: Enhanced data access (requires Upwork login)

Enhanced features with login:
   ✅ Payment verification status
   ✅ Proposal counts and connects required
   ✅ Advanced filtering options
   ✅ Higher rate limits

🔑 Do you want to login to Upwork? (y/n, default: n):
```

### 2. **Secure Credential Input** (if you choose login)
```
📧 UPWORK CREDENTIALS
------------------------------
⚠️  Your credentials are only used for this session and are not stored.

📧 Upwork email/username: your_email@example.com
🔒 Upwork password: [hidden input]
   ✅ Credentials received for: your_email@example.com
   🔐 Login will be attempted during scraping...
```

### 3. **Search Configuration**
```
📋 JOB SEARCH CONFIGURATION
==================================================

📝 Enter search keyword/job title: python developer
🔢 How many jobs to scrape? (default: 25): 50

📂 Job Categories (optional):
1.  Web, Mobile & Software Dev
2.  AI & Machine Learning
3.  Data Science & Analytics
...
10. All categories

🎯 Select category (1-10, default: 10): 1
```

### 4. **Advanced Options** (optional)
```
🔧 Advanced Filters (optional):
📋 Apply advanced filters? (y/n, default: n): y

💰 Hourly Rate Filter:
   💵 Minimum hourly rate (e.g., 25, default: none): 50
   💎 Maximum hourly rate (e.g., 100, default: none): 150
```

### 5. **Configuration Summary**
```
✅ Search Configuration:
   🔍 Keyword: 'python developer'
   📊 Jobs to scrape: 50
   🔐 Login: Enabled (your_email@example.com)
   📂 Category: Web, Mobile & Software Dev
   💰 Hourly rate: $50-$150/hr
   💾 Save CSV: Yes

🚀 Starting search...
```

## **WHY** This Interactive Mode is Better

### **Before** (Complex JSON):
```bash
python main.py --jsonInput '{"credentials": {"username": "email@example.com", "password": "password"}, "search": {"query": "python developer", "limit": 50, "category": ["web, mobile & software dev"], "hourly_min": 50, "hourly_max": 150}}'
```

### **After** (Simple Interactive):
```bash
python main.py
# Then just answer the prompts!
```

## **HOW** the Interactive Flow Works

1. **🔐 Login Decision**: Choose anonymous or authenticated mode upfront
2. **🔒 Secure Input**: Password input is hidden for security
3. **📋 Step-by-Step**: Guided configuration with helpful examples
4. **✅ Validation**: Input validation with helpful error messages
5. **📊 Summary**: Clear overview before execution
6. **🚀 Execution**: Same powerful scraping with your chosen settings

## Key Benefits

### **🎯 User-Friendly**
- No complex JSON syntax to remember
- Clear prompts with examples
- Default values for quick setup

### **🔒 Secure**
- Password input is hidden (`getpass` module)
- Credentials are session-only (not stored)
- Option to cancel login anytime

### **🎛️ Flexible**
- Start with basic search, add filters as needed
- Skip advanced options for quick searches
- All original functionality still available

### **📱 Responsive**
- Validates inputs in real-time
- Helpful error messages
- Easy retry on invalid input

## Alternative Methods Still Available

### Method 1: JSON Input (Original)
```bash
python main.py --jsonInput '{...}'
```

### Method 2: Environment Variable
```bash
export jsonInput='{"search": {"query": "developer"}}'
python main.py
```

### Method 3: API Endpoints
```bash
curl -X POST "http://localhost:8000/run/keyword" \
     -H "Content-Type: application/json" \
     -d '{"query": "python", "username": "email", "password": "pass"}'
```

## Testing the Interactive Mode

Run the test script to see a demonstration:
```bash
python test_interactive_login.py
```

## Tips for Best Experience

1. **🔐 Use Login for Better Data**: Login provides more detailed job information
2. **📊 Start Small**: Try with 5-10 jobs first to test your filters
3. **🎯 Be Specific**: More specific keywords yield better results
4. **💰 Set Rate Filters**: Use hourly/fixed rate filters to find jobs in your price range
5. **🔄 Iterate**: Run multiple searches with different parameters to find the best jobs

---

**🎉 That's it! The interactive mode makes the Upwork Job Scraper much easier to use while maintaining all its powerful features.**
