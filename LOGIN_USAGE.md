# Upwork Job Scraper - Login Functionality

## Overview

The Upwork Job Scraper now supports login functionality that allows you to access premium features and enhanced data when scraping jobs. Login is **optional** - the scraper works without credentials but provides more features when logged in.

## Benefits of Using Login

When you provide valid Upwork credentials, you get access to:

- **Premium filters**: Payment verification status, proposal counts, etc.
- **Enhanced job data**: More detailed client information
- **Higher rate limits**: Better performance and reliability
- **Advanced search options**: Filters that require authentication

## Security Features

- **Password masking**: Passwords are masked in logs for security
- **Credential validation**: Validates that both username and password are provided
- **Error handling**: Graceful fallback to non-authenticated mode if login fails

## Usage Methods

### 1. Command Line Interface (CLI)

#### With login credentials:
```bash
python main.py --jsonInput '{
  "credentials": {
    "username": "your_email@example.com",
    "password": "your_password"
  },
  "search": {
    "query": "python developer",
    "limit": 25
  }
}'
```

#### Without login (anonymous mode):
```bash
python main.py --jsonInput '{
  "credentials": {
    "username": null,
    "password": null
  },
  "search": {
    "query": "python developer",
    "limit": 25
  }
}'
```

### 2. Configuration File

Create a `config.json` file:

```json
{
  "credentials": {
    "username": "your_email@example.com",
    "password": "your_password"
  },
  "search": {
    "query": "AI chatbot development",
    "limit": 25,
    "category": ["Web, Mobile & Software Dev"],
    "hourly_min": 25,
    "hourly_max": 100,
    "payment_verified": true
  },
  "general": {
    "save_csv": true
  }
}
```

### 3. Flask API

#### Simple keyword search with login:
```bash
curl -X POST "http://localhost:8000/run/keyword" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "python developer",
       "limit": 25,
       "username": "your_email@example.com",
       "password": "your_password"
     }'
```

#### Advanced search with login:
```bash
curl -X POST "http://localhost:8000/run/advanced" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "data engineer",
       "limit": 50,
       "username": "your_email@example.com", 
       "password": "your_password",
       "category": ["data science & analytics"],
       "hourly_min": 50,
       "hourly_max": 150,
       "payment_verified": true,
       "sort": "newest"
     }'
```

#### Without login (anonymous):
```bash
curl -X POST "http://localhost:8000/run/keyword" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "python developer",
       "limit": 25
     }'
```

### 4. FastAPI

#### With login:
```bash
curl -X POST "http://localhost:8000/run/keyword" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "react developer",
       "limit": 30,
       "username": "your_email@example.com",
       "password": "your_password"
     }'
```

#### Without login:
```bash
curl -X POST "http://localhost:8000/run/keyword" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "react developer",
       "limit": 30
     }'
```

## How Login Works

### **WHY** automated login is needed:
- Upwork uses sophisticated bot detection and Cloudflare protection
- Manual login is not feasible for automated scraping
- Session management is required for authenticated requests

### **HOW** the login process works:

1. **Browser Creation**: Uses Camoufox (stealth browser) to avoid detection
2. **Captcha Solving**: Automatically handles Cloudflare challenges
3. **Login Automation**: 
   - Navigates to Upwork login page
   - Fills username and password fields
   - Handles verification and errors
4. **Session Transfer**: Converts browser cookies to requests session for efficient scraping
5. **Fallback Handling**: Multiple retry mechanisms if login fails

### **Technical Flow**:
```
User Input → Credential Validation → Browser Launch → Captcha Solve → 
Login Attempt → Session Creation → Job Scraping → Result Return
```

## Error Handling

The system handles various error scenarios:

- **Missing credentials**: Falls back to anonymous mode
- **Invalid credentials**: Logs error and continues without login
- **Login failures**: Multiple retry attempts with different strategies
- **Captcha failures**: Re-attempts with fresh context
- **Network issues**: Graceful degradation

## Troubleshooting

### Common Issues:

1. **Login fails repeatedly**:
   - Verify credentials are correct
   - Check if account has 2FA enabled (not supported)
   - Try again after some time (rate limiting)

2. **Captcha not solving**:
   - Internet connection issues
   - Upwork has updated their protection
   - Try running again

3. **Limited data without login**:
   - Some fields require authentication
   - Provide credentials for full data access

### Log Messages:

- `🔐 Login enabled for user: username` - Login will be attempted
- `🚫 Running without login` - Anonymous mode
- `⚠️ Username provided but password is missing` - Validation error
- `✅ Login succeeded` - Successful authentication
- `⚠️ Login failed` - Authentication failed, running anonymously

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for production deployments
3. **Rotate passwords regularly**
4. **Monitor for suspicious account activity**
5. **Use application-specific passwords** if available

## Environment Variables

For production deployments, use environment variables:

```bash
export UPWORK_USERNAME="your_email@example.com"
export UPWORK_PASSWORD="your_password"
```

Then modify your config to use them:
```json
{
  "credentials": {
    "username": "${UPWORK_USERNAME}",
    "password": "${UPWORK_PASSWORD}"
  }
}
```

## Rate Limiting

- **With login**: Higher rate limits, more concurrent requests
- **Without login**: Lower rate limits, may hit restrictions sooner
- **Recommendation**: Use login for production workloads

## Data Differences

| Feature | Anonymous | Logged In |
|---------|-----------|-----------|
| Basic job info | ✅ | ✅ |
| Client verification status | ❌ | ✅ |
| Proposal counts | ❌ | ✅ |
| Connects required | ❌ | ✅ |
| Advanced filters | Limited | Full |
| Rate limits | Lower | Higher |
