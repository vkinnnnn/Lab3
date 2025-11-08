# 🎯 Rate Limiting Explained Simply

## What is Rate Limiting?

**Rate limiting = Controlling how many API calls each friend can make per day**

Think of it like a **daily allowance**:
- Free tier: 100 requests/day
- Pro tier: 1,000 requests/day
- Enterprise: 10,000 requests/day

---

## 📊 Visual Example

### Friend 1 (Free Tier - Good Status)

```
============================================================
📊 API Usage for Friend 1
============================================================
Tier: FREE

Daily Limit: 100 requests
Used: 45 requests
Remaining: 55 requests

Progress: [█████████░░░░░░░░░░░] 45.0%
Status: ✅ Good
============================================================
```

**What this means:**
- ✅ Friend 1 can make 55 more requests today
- ✅ Everything is working fine
- ✅ No worries!

---

### Friend 2 (Free Tier - Warning Status)

```
============================================================
📊 API Usage for Friend 2
============================================================
Tier: FREE

Daily Limit: 100 requests
Used: 85 requests
Remaining: 15 requests

Progress: [█████████████████░░░] 85.0%
Status: ⚠️ Warning
============================================================
```

**What this means:**
- ⚠️ Friend 2 only has 15 requests left today
- ⚠️ Should use them carefully
- ⚠️ Will reset at midnight

---

### Friend 3 (Free Tier - Limit Reached)

```
============================================================
📊 API Usage for Friend 3
============================================================
Tier: FREE

Daily Limit: 100 requests
Used: 100 requests
Remaining: 0 requests

Progress: [████████████████████] 100.0%
Status: ❌ Limit Reached

Resets at: 2025-10-29 00:00:00 (in 8 hours)
============================================================
```

**What this means:**
- ❌ Friend 3 has used all 100 requests
- ❌ Cannot make more requests today
- ✅ Will reset at midnight (gets 100 new requests)

---

## 🔄 How It Resets

### Daily Reset Schedule

```
Day 1:
├─ 00:00 - Limit resets to 100
├─ 10:00 - Used 30 (70 remaining)
├─ 14:00 - Used 60 (40 remaining)
├─ 18:00 - Used 95 (5 remaining)
└─ 23:59 - Used 100 (0 remaining)

Day 2:
└─ 00:00 - ✨ RESET! Back to 100 requests
```

---

## 💰 Why Rate Limiting?

### 1. Cost Control

**Each request costs YOU money:**
- Document AI: $1.50-$4.50 per 1000 pages
- If Friend makes 10,000 requests = $15-$45 cost to YOU

**With rate limiting:**
- Free tier: 100 requests/day = $0.15-$0.45/day
- Manageable costs!

### 2. Fair Usage

**Without rate limiting:**
- Friend A: Uses 10,000 requests
- Friend B: Can't use API (server overloaded)

**With rate limiting:**
- Friend A: 100 requests/day
- Friend B: 100 requests/day
- Everyone gets fair access!

### 3. Prevent Abuse

**Bad scenario:**
- Someone writes a script
- Makes 100,000 requests
- Costs you $150-$450!

**With rate limiting:**
- Max 100 requests/day
- Max cost: $0.45/day
- Protected!

---

## 📈 Tier Comparison

### Free Tier (100 requests/day)

```
Perfect for:
- Testing the API
- Small projects
- Personal use
- 3-4 documents per day

Cost to you: ~$0.45/day
Cost to them: FREE
```

### Pro Tier (1,000 requests/day)

```
Perfect for:
- Production apps
- Business use
- 30-40 documents per day

Cost to you: ~$4.50/day
Cost to them: $29/month
Your profit: $24.50/month
```

### Enterprise Tier (10,000 requests/day)

```
Perfect for:
- Large companies
- High volume
- 300-400 documents per day

Cost to you: ~$45/day
Cost to them: $199/month
Your profit: $154/month
```

---

## 🎯 What Your Friends See

### Every API Response Includes:

```json
{
  "complete_text": { ... },
  "all_numbers": [ ... ],
  
  "api_usage": {
    "requests_used": 45,
    "requests_remaining": 55,
    "daily_limit": 100,
    "status": "✅ Good"
  }
}
```

### Simple Python Usage:

```python
from document_extractor_client import DocumentExtractorClient

client = DocumentExtractorClient(api_key="friend-key")

# Check usage anytime
client.get_usage()

# Output:
# 📊 API Usage:
#    Used: 45/100
#    Remaining: 55
#    Status: ✅ Good
```

---

## 🚨 What Happens When Limit Reached?

### Error Response:

```json
{
  "error": "Rate limit exceeded",
  "message": "You have used all 100 requests for today",
  "requests_used": 100,
  "requests_remaining": 0,
  "reset_time": "2025-10-29T00:00:00",
  "retry_after_seconds": 28800
}
```

### Friendly Message:

```
❌ Rate Limit Exceeded

You've used all 100 requests for today.

Your limit will reset in 8 hours at midnight.

Want more requests? Upgrade to Pro (1,000/day) for $29/month!
```

---

## 🎨 Visual Progress Indicators

### 0-50% Used (Green - Good)

```
[█████░░░░░░░░░░░░░░░] 25.0% ✅ Good
Used: 25/100 | Remaining: 75
```

### 50-80% Used (Yellow - Warning)

```
[█████████████░░░░░░░] 65.0% ⚠️ Warning
Used: 65/100 | Remaining: 35
```

### 80-100% Used (Red - Critical)

```
[██████████████████░░] 90.0% 🔴 Critical
Used: 90/100 | Remaining: 10
```

### 100% Used (Red - Blocked)

```
[████████████████████] 100.0% ❌ Blocked
Used: 100/100 | Remaining: 0
Resets in: 6 hours
```

---

## 🔧 How It Works Technically

### 1. Request Comes In

```python
# Friend makes request
POST /api/v1/extract
Headers: X-API-Key: friend-key
```

### 2. Check Rate Limit

```python
# System checks:
user_id = "friend@example.com"
limit = 100  # Free tier
used = 45    # Requests used today

if used >= limit:
    return "Rate limit exceeded"
else:
    # Allow request
    used = 46  # Increment counter
```

### 3. Return Response with Usage

```python
# Response includes:
{
  "data": { ... },
  "api_usage": {
    "used": 46,
    "remaining": 54,
    "limit": 100
  }
}
```

---

## 📊 Real-World Example

### Scenario: Friend Building an App

**Day 1:**
```
09:00 - Upload 10 documents → Used: 10/100 ✅
12:00 - Upload 20 documents → Used: 30/100 ✅
15:00 - Upload 30 documents → Used: 60/100 ⚠️
18:00 - Upload 35 documents → Used: 95/100 🔴
20:00 - Upload 10 documents → ❌ BLOCKED (only 5 allowed)
```

**Day 2:**
```
00:00 - ✨ RESET! Back to 0/100
09:00 - Upload 50 documents → Used: 50/100 ✅
```

---

## 💡 Tips for Your Friends

### 1. Check Usage Before Big Batches

```python
# Check before processing
usage = client.get_usage()
if usage['usage']['remaining'] < 50:
    print("Warning: Less than 50 requests left!")
```

### 2. Batch Processing

```python
# Process in batches
documents = ["doc1.pdf", "doc2.pdf", ..., "doc100.pdf"]

for i, doc in enumerate(documents):
    if i % 10 == 0:
        usage = client.get_usage()
        print(f"Remaining: {usage['usage']['remaining']}")
    
    result = client.extract(doc)
```

### 3. Upgrade When Needed

```
If consistently hitting limit:
- Free (100/day) → Pro (1,000/day)
- Pro (1,000/day) → Enterprise (10,000/day)
```

---

## 🎯 Summary

### What Rate Limiting Does:

✅ **Protects your costs** - Prevents unlimited spending
✅ **Ensures fair access** - Everyone gets their share
✅ **Prevents abuse** - Stops malicious usage
✅ **Provides transparency** - Friends see their usage

### What Your Friends Get:

✅ **Clear limits** - Know exactly how many requests
✅ **Real-time tracking** - See usage after each request
✅ **Visual indicators** - Progress bars and status
✅ **Predictable resets** - Daily at midnight
✅ **Upgrade options** - Can get more if needed

### Super Simple:

```
Free Tier:
- 100 requests/day
- Resets at midnight
- See usage in real-time
- Upgrade anytime

That's it! 🎉
```

---

**Your friends will love the transparency and you'll love the cost control!** 💰✨
