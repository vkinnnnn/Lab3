# 📊 API Usage Indicator Guide

## Visual Usage Tracking

Your friends will see their API usage in **real-time** with beautiful indicators!

---

## 🎯 What They See

### 1. In API Response (Every Request)

```json
{
  "complete_text": { ... },
  "all_numbers": [ ... ],
  "all_tables": [ ... ],
  
  "api_usage": {
    "user": "Friend Name",
    "tier": "free",
    "requests_used": 45,
    "requests_remaining": 55,
    "daily_limit": 100,
    "reset_time": "2025-10-29T00:00:00",
    "processing_time_seconds": 2.34
  }
}
```

### 2. In Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 55
X-RateLimit-Reset: 2025-10-29T00:00:00
```

### 3. Dedicated Usage Endpoint

**Request:**
```bash
curl -X GET "http://your-api.com/api/v1/usage" \
  -H "X-API-Key: friend-key"
```

**Response:**
```json
{
  "user": "Friend Name",
  "email": "friend@example.com",
  "tier": "free",
  
  "usage": {
    "limit": 100,
    "used": 45,
    "remaining": 55,
    "percentage": 45.0,
    "status": "✅ Good",
    "status_color": "green"
  },
  
  "visual": {
    "progress_bar": "█████████░░░░░░░░░░░",
    "indicator": "[█████████░░░░░░░░░░░] 45.0%"
  },
  
  "summary": "Limit: 100 requests/day | Used: 45 | Remaining: 55 | Status: ✅ Good",
  
  "hourly_breakdown": {
    "2025-10-28T10:00:00": 12,
    "2025-10-28T11:00:00": 18,
    "2025-10-28T12:00:00": 15
  }
}
```

---

## 🎨 Visual Indicators

### Status Colors

| Remaining | Status | Color | Emoji |
|-----------|--------|-------|-------|
| > 50% | Good | 🟢 Green | ✅ |
| 20-50% | Warning | 🟡 Yellow | ⚠️ |
| 1-20% | Critical | 🔴 Red | 🔴 |
| 0% | Limit Reached | 🔴 Red | ❌ |

### Progress Bar

```
[████████████████████] 100.0%  ❌ Limit Reached
[█████████████████░░░] 85.0%   🔴 Critical
[████████████░░░░░░░░] 60.0%   ⚠️ Warning
[█████████░░░░░░░░░░░] 45.0%   ✅ Good
[███░░░░░░░░░░░░░░░░░] 15.0%   ✅ Good
[░░░░░░░░░░░░░░░░░░░░] 0.0%    ✅ Good (unused)
```

---

## 💻 Python Client Usage

### Simple Usage Check

```python
from document_extractor_client import DocumentExtractorClient

client = DocumentExtractorClient(api_key="your-key")

# Check usage anytime
client.get_usage()
```

**Output:**
```
============================================================
📊 API Usage for Friend Name
============================================================
Tier: FREE

Daily Limit: 100 requests
Used: 45 requests
Remaining: 55 requests

Progress: [█████████░░░░░░░░░░░] 45.0%
Status: ✅ Good
============================================================
```

### Automatic Usage Display

```python
# Usage is automatically shown after each extraction
result = client.extract("document.pdf")

# Output:
# 📊 API Usage:
#    Used: 46/100
#    Remaining: 54
#    Tier: free
```

---

## 🚨 Rate Limit Exceeded

### What Happens

When limit is reached, your friends get a clear error:

```json
{
  "error": "Rate limit exceeded",
  "message": "You have used all 100 requests for today",
  "requests_used": 100,
  "requests_remaining": 0,
  "limit": 100,
  "reset_time": "2025-10-29T00:00:00",
  "retry_after_seconds": 43200
}
```

### Python Client Handles It

```python
try:
    result = client.extract("document.pdf")
except Exception as e:
    print(e)
    # Output: "Rate limit exceeded: You have used all 100 requests for today"
```

---

## 📈 Hourly Breakdown

See usage patterns throughout the day:

```json
"hourly_breakdown": {
  "2025-10-28T08:00:00": 5,
  "2025-10-28T09:00:00": 12,
  "2025-10-28T10:00:00": 18,
  "2025-10-28T11:00:00": 10
}
```

---

## 🎯 Tier Limits

| Tier | Daily Limit | Cost |
|------|-------------|------|
| **Free** | 100 requests | Free |
| **Pro** | 1,000 requests | $29/month |
| **Enterprise** | 10,000 requests | $199/month |

---

## 🔄 Reset Time

Limits reset at **midnight UTC** every day.

**Current time:** 2025-10-28 14:30:00
**Reset time:** 2025-10-29 00:00:00
**Time until reset:** 9 hours 30 minutes

---

## 📱 Dashboard View (Optional)

You can create a simple dashboard for your friends:

```python
import streamlit as st

# Show usage indicator
usage = client.get_usage()

st.title("📊 API Usage Dashboard")

# Progress bar
st.progress(usage['usage']['percentage'] / 100)

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Used", usage['usage']['used'])
col2.metric("Remaining", usage['usage']['remaining'])
col3.metric("Limit", usage['usage']['limit'])

# Status
st.info(usage['summary'])
```

---

## 🎨 Custom Styling (For Web Apps)

### HTML/CSS Example

```html
<div class="usage-indicator">
  <div class="usage-bar">
    <div class="usage-fill" style="width: 45%"></div>
  </div>
  <div class="usage-text">
    45/100 requests used (55 remaining)
  </div>
</div>

<style>
.usage-bar {
  width: 100%;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
}
.usage-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  border-radius: 10px;
  transition: width 0.3s;
}
.usage-text {
  margin-top: 8px;
  font-size: 14px;
  color: #666;
}
</style>
```

---

## 🔔 Notifications (Optional)

### Email Alerts

You can set up automatic emails when friends reach:
- 80% usage: "⚠️ You've used 80 requests"
- 90% usage: "🔴 You've used 90 requests"
- 100% usage: "❌ Daily limit reached"

### Webhook Alerts

```python
# When user reaches 90%
POST https://friend-app.com/webhook
{
  "event": "rate_limit_warning",
  "user": "friend@example.com",
  "usage_percentage": 90,
  "remaining": 10
}
```

---

## 📊 Admin Dashboard

You can monitor all users:

```python
# Get all usage stats (admin only)
GET /api/v1/admin/usage-stats
```

**Response:**
```json
{
  "total_users": 5,
  "total_requests_today": 234,
  "users": [
    {
      "email": "friend1@example.com",
      "tier": "free",
      "used": 45,
      "remaining": 55
    },
    {
      "email": "friend2@example.com",
      "tier": "pro",
      "used": 234,
      "remaining": 766
    }
  ]
}
```

---

## 🎯 Summary

### Your Friends Will See:

✅ **Real-time usage** in every API response
✅ **Visual progress bar** with percentage
✅ **Status indicator** (Good/Warning/Critical)
✅ **Remaining requests** count
✅ **Reset time** for next day
✅ **Hourly breakdown** of usage
✅ **Clear error messages** when limit reached

### Super Easy to Use:

```python
# One line to check usage
client.get_usage()

# Automatic display after extraction
result = client.extract("doc.pdf")
# Shows: "Used: 46/100 | Remaining: 54"
```

**Your friends will always know exactly how many requests they have left!** 📊✨
