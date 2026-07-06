# Complete API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## 🔐 Authentication Endpoints

### Sign Up
**POST** `/auth/signup`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123!"
}
```

**Response (201):**
```json
{
  "message": "User created successfully",
  "user_id": "uuid",
  "token": "eyJhbGc...",
  "email_verification_sent": true
}
```

**Errors:**
- `400`: Invalid email format or weak password
- `409`: User already exists

---

### Login
**POST** `/auth/login`

Authenticate and get JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGc...",
  "user_id": "uuid",
  "name": "John Doe"
}
```

**Errors:**
- `401`: Invalid credentials

---

### Verify Email
**POST** `/auth/verify-email?token=<token>`

Verify email address using verification token from email.

**Response (200):**
```json
{
  "message": "Email verified successfully"
}
```

---

## 👤 User Profile Endpoints

### Get Profile
**GET** `/user/profile`

Get current user's profile with all data and learning information.

**Response (200):**
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "preferences": {
    "tone": "neutral",
    "response_length": "medium",
    "language": "en"
  },
  "unlocked_skills": ["search", "calculate", "summarize"],
  "skill_proficiency": {
    "search": {"level": 0.7, "practice_count": 15}
  },
  "interaction_count": 45
}
```

---

### Update Preferences
**PUT** `/user/preferences`

Update user preferences.

**Request Body:**
```json
{
  "key": "tone",
  "value": "formal"
}
```

**Available Preferences:**
- `tone`: "neutral" | "formal" | "casual" | "friendly"
- `response_length`: "short" | "medium" | "long"
- `language`: "en" | "es" | "fr" | etc.

**Response (200):**
```json
{
  "message": "Preference updated",
  "preference": "tone"
}
```

---

### Get Learning Analysis
**GET** `/user/learning-analysis`

Get AI's analysis of user behavior and learning patterns.

**Response (200):**
```json
{
  "total_interactions": 45,
  "primary_topics": [["python", 12], ["ai", 8]],
  "skill_progression": {
    "search": {"level": 0.7, "practice_count": 15}
  },
  "learning_pace": "medium",
  "engagement_level": 0.85,
  "recommended_skills": [
    {
      "skill": "code_explain",
      "reason": "You're progressing well!",
      "confidence": 0.8
    }
  ]
}
```

---

## ⚡ Skills Endpoints

### Get Available Skills
**GET** `/skills/available`

Get list of skills available to current user.

**Response (200):**
```json
{
  "unlocked_skills": ["search", "calculate", "summarize", "keywords"],
  "available_skills": ["search", "calculate", "summarize"],
  "proficiency": {
    "search": {"level": 0.7, "practice_count": 15}
  }
}
```

---

### Execute Skill
**POST** `/skills/execute`

Execute a specific skill.

**Request Body:**
```json
{
  "skill_name": "search",
  "query": "Python machine learning"
}
```

**Available Skills:**
- `search` - Web search
- `calculate` - Math operations
- `summarize` - Text summarization
- `keywords` - Keyword extraction
- `code_explain` - Code explanation (requires unlock)
- `brainstorm` - Idea generation (requires unlock)

**Response (200):**
```json
{
  "skill": "search",
  "result": "Python machine learning is...",
  "proficiency_increased": true
}
```

---

### Execute Skill Chain
**POST** `/skills/chain`

Execute multiple skills sequentially.

**Request Body:**
```json
{
  "chain_name": "summarize_and_extract",
  "initial_query": "Long text content..."
}
```

**Response (200):**
```json
{
  "chain": "summarize_and_extract",
  "result": "Extracted summary and keywords..."
}
```

---

## 💬 Chat Endpoints

### Send Message
**POST** `/chat`

Send a message and get personalized response.

**Request Body:**
```json
{
  "message": "What is machine learning?",
  "user_id": "optional-uuid"
}
```

**Response (200):**
```json
{
  "response": "Machine learning is...",
  "user_id": "uuid",
  "personalized": true
}
```

---

## 📊 Analytics Endpoints

### Get Dashboard
**GET** `/analytics/dashboard`

Get comprehensive analytics dashboard.

**Response (200):**
```json
{
  "user_id": "uuid",
  "name": "John Doe",
  "interactions_total": 45,
  "skills_unlocked": 4,
  "analysis": {
    "total_interactions": 45,
    "learning_pace": "medium",
    "engagement_level": 0.85
  },
  "recommendations": [
    {
      "skill": "code_explain",
      "reason": "You're progressing well!",
      "confidence": 0.8
    }
  ]
}
```

---

## 🏥 Health Endpoints

### Health Check
**GET** `/health`

**Response (200):**
```json
{
  "status": "healthy"
}
```

### Service Status
**GET** `/`

**Response (200):**
```json
{
  "status": "running",
  "service": "Jarvondis Smart Chat v2.0",
  "features": [
    "User Authentication",
    "Email Verification",
    "Adaptive Learning",
    "Skills System",
    "Personalization",
    "Analytics"
  ]
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

---

## Rate Limiting

- Free tier: 1,000 requests/hour
- Pro tier: Unlimited
- Enterprise: Custom limits

---

## Pagination

Listy endpoints support pagination:
```
?page=1&per_page=20
```

---

## Webhooks

Coming soon: Webhook notifications for skill unlocks, level achievements, etc.

---

## Need Help?

- 📧 Email: support@jarvondis.com
- 💬 Discord: [Join our community](https://discord.gg/jarvondis)
- 📚 Docs: https://docs.jarvondis.com
