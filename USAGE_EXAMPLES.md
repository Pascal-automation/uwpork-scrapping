# 🚀 Upwork Job Scraper - Usage Examples with Advanced Filters

## **Terminal Interactive Mode**

### **Basic Usage:**
```bash
python main.py
```

**Example Session:**
```
🔍 Upwork Job Scraper - Interactive Mode
==================================================

📝 Enter search keyword/job title: data engineering
🔢 How many jobs to scrape? (default: 25): 10

📂 Job Categories (optional):
1.  Web, Mobile & Software Dev
2.  AI & Machine Learning
3.  Data Science & Analytics
4.  Design & Creative
5.  Writing
6.  Sales & Marketing
7.  Customer Service
8.  Admin Support
9.  Engineering & Architecture
10. All categories

🎯 Select category (1-10, default: 10): 3

🔧 Advanced Filters (optional):
📋 Apply advanced filters? (y/n, default: n): y

💰 Hourly Rate Filter:
   💵 Minimum hourly rate (e.g., 25, default: none): 50
   💎 Maximum hourly rate (e.g., 100, default: none): 

🏢 Client Filters:
1. Any number of hires
2. 1-9 previous hires
3. 10+ previous hires
4. Custom range

   👥 Client hires filter (1-4, default: 1): 3

🎯 Job Type:
1. Both hourly and fixed-price
2. Hourly only
3. Fixed-price only

   💼 Job type (1-3, default: 1): 2

📊 Sort Order:
1. Relevance (default)
2. Newest first
3. Client total spent
4. Client rating

   🔄 Sort by (1-4, default: 1): 2

🔍 Additional Filters:
   💳 Payment verified clients only? (y/n, default: n): y

✅ Search Configuration:
   🔍 Keyword: 'data engineering'
   📊 Jobs to scrape: 10
   📂 Category: Data Science & Analytics
   💰 Hourly rate: $50-$∞/hr
   👥 Client hires: 10-∞ hires
   💼 Job type: Hourly only
   🔄 Sort: Newest
   💳 Payment verified: Yes
   💾 Save CSV: Yes

🚀 Starting search...
```

---

## **API Usage Examples**

### **1. Simple Keyword Search**
```bash
curl -X POST "http://localhost:8000/run/keyword" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "python developer",
    "limit": 10
  }'
```

### **2. Advanced Search with Filters**
```bash
curl -X POST "http://localhost:8000/run/advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data engineering",
    "limit": 15,
    "category": ["data science & analytics"],
    "hourly_min": 50,
    "hires_min": 10,
    "hourly": true,
    "fixed": false,
    "sort": "newest",
    "payment_verified": true
  }'
```

### **3. Full JSON Configuration**
```bash
curl -X POST "http://localhost:8000/run/json" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "credentials": {
        "username": null,
        "password": null
      },
      "search": {
        "query": "machine learning",
        "limit": 20,
        "category": ["data science & analytics", "ai & machine learning"],
        "hourly_min": 30,
        "hourly_max": 150,
        "hires_min": 5,
        "payment_verified": true,
        "sort": "client_rating",
        "hourly": true,
        "fixed": true
      },
      "general": {
        "save_csv": true
      }
    }
  }'
```

---

## **Filter Options Reference**

### **🔍 Search Parameters**
- `query` (required): Job search keyword
- `limit`: Number of jobs to scrape (1-200)

### **📂 Category Filters**
```json
"category": [
  "web, mobile & software dev",
  "data science & analytics", 
  "ai & machine learning",
  "design & creative",
  "writing",
  "sales & marketing",
  "customer service",
  "admin support",
  "engineering & architecture"
]
```

### **💰 Rate Filters**
```json
"hourly_min": 25,    // Minimum hourly rate
"hourly_max": 100    // Maximum hourly rate
```

### **🏢 Client Filters**
```json
"hires_min": 1,           // Minimum client hires
"hires_max": 50,          // Maximum client hires  
"payment_verified": true  // Payment verified clients only
```

### **💼 Job Type Filters**
```json
"hourly": true,  // Include hourly jobs
"fixed": true    // Include fixed-price jobs
```

### **📊 Sort Options**
```json
"sort": "relevance"           // Default relevance
"sort": "newest"              // Newest first
"sort": "client_total_charge" // Client total spent
"sort": "client_rating"       // Client rating
```

---

## **Real-World Examples**

### **High-Paying Data Engineering Jobs**
```bash
curl -X POST "http://localhost:8000/run/advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data engineering ETL",
    "limit": 25,
    "category": ["data science & analytics"],
    "hourly_min": 75,
    "hires_min": 5,
    "payment_verified": true,
    "sort": "client_total_charge"
  }'
```

### **Entry-Level Web Development**
```bash
curl -X POST "http://localhost:8000/run/advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "react javascript",
    "limit": 30,
    "category": ["web, mobile & software dev"],
    "hourly_min": 15,
    "hourly_max": 50,
    "hires_min": 1,
    "hires_max": 20,
    "sort": "newest"
  }'
```

### **Premium Fixed-Price Projects**
```bash
curl -X POST "http://localhost:8000/run/advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mobile app development",
    "limit": 20,
    "category": ["web, mobile & software dev"],
    "hires_min": 10,
    "payment_verified": true,
    "hourly": false,
    "fixed": true,
    "sort": "client_rating"
  }'
```

---

## **Response Format**

All endpoints return the same format:

```json
{
  "count": 15,
  "results": [
    {
      "ID": "abc123",
      "Title": "Senior Data Engineer - ETL Pipeline",
      "Type": "Hourly", 
      "Min Rate": 75,
      "Max Rate": 120,
      "Country": "United States",
      "City": "San Francisco",
      "Total Hires": 25,
      "Payment Verified": true,
      "Skills": ["Python", "Apache Spark", "AWS", "ETL"],
      "Description": "Looking for experienced data engineer..."
    }
  ]
}
```

---

## **Quick Reference**

### **Terminal Mode:**
```bash
python main.py
# Follow interactive prompts
```

### **Simple API:**
```bash
POST /run/keyword
{"query": "python", "limit": 10}
```

### **Advanced API:**
```bash
POST /run/advanced  
{"query": "data", "hourly_min": 50, "hires_min": 10}
```

### **Full Control:**
```bash
POST /run/json
{"input": {"search": {...}, "credentials": {...}}}
```

The advanced filters give you precise control over job quality, client requirements, and search sorting! 🎯
