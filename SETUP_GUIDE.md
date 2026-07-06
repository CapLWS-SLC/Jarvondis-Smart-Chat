# Jarvondis Smart Chat - Complete Setup Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ (optional, for frontend development)
- Docker & Docker Compose (optional, for containerized deployment)
- Git

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/CapLWS-SLC/Jarvondis-Smart-Chat.git
cd Jarvondis-Smart-Chat
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run Application
```bash
# Start API server
uvicorn api.server:app --reload --host 0.0.0.0 --port 8000

# In another terminal, serve frontend
cd static
python -m http.server 3000
```

### 6. Access Application
- Landing Page: http://localhost:3000/landing.html
- Chat: http://localhost:3000
- API Docs (Swagger): http://localhost:8000/docs

---

## 🐳 Docker Setup

### Build Image
```bash
docker build -t jarvondis:latest .
```

### Run Container
```bash
docker run -p 8000:8000 jarvondis:latest
```

### Docker Compose
```bash
docker-compose up -d
```

Access:
- Frontend: http://localhost
- API: http://localhost:8000

---

## ⚙️ Configuration

### Email Setup (Gmail)

1. Enable 2-factor authentication on your Google account
2. Generate app password: https://myaccount.google.com/apppasswords
3. Set environment variables:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

### Email Setup (Custom SMTP)

```bash
SMTP_SERVER=mail.yourserver.com
SMTP_PORT=587
SENDER_EMAIL=noreply@yourserver.com
SENDER_PASSWORD=password
```

---

## 🔑 Security

### JWT Secret
```bash
# Generate strong secret
openssl rand -hex 32

# Set in .env
JWT_SECRET=your-generated-secret
```

### Password Requirements
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

---

## 📱 Features Overview

### Authentication
- ✅ Sign up with email
- ✅ Login with email/password
- ✅ Email verification
- ✅ Password reset (coming soon)
- ✅ JWT-based sessions

### User Profiles
- ✅ Customizable preferences
- ✅ Learning data tracking
- ✅ Skill progression
- ✅ Interaction history
- ✅ Interest detection

### Skills System
- ✅ Core skills: search, calculate, summarize, keywords
- ✅ Advanced skills: code_explain, brainstorm (unlock via engagement)
- ✅ Skill proficiency tracking
- ✅ Skill chains (execute multiple skills)
- ✅ Auto skill unlock based on progress

### Adaptive Learning
- ✅ Behavior analysis
- ✅ Topic clustering
- ✅ Learning pace detection
- ✅ Engagement tracking
- ✅ Personalized recommendations
- ✅ Response customization

### Analytics
- ✅ Interaction tracking
- ✅ Skill progression visualization
- ✅ Learning pace metrics
- ✅ Engagement scoring
- ✅ Recommendation engine

---

## 📚 API Usage Examples

### Sign Up
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"message": "Hello!"}'
```

### Execute Skill
```bash
curl -X POST http://localhost:8000/skills/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "skill_name": "search",
    "query": "Python programming"
  }'
```

---

## 🧪 Testing

### Run Tests
```bash
pip install -r requirements-dev.txt
pytest --cov=. --cov-report=html
```

### Test Coverage
```bash
# View coverage report
open htmlcov/index.html
```

---

## 🚢 Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku config:set JWT_SECRET=your-secret
```

### AWS Elastic Beanstalk
```bash
eb init
eb create
eb deploy
```

### DigitalOcean
```bash
# Create droplet
# SSH into droplet
# Follow Linux setup from DEPLOYMENT.md
```

### Docker Hub
```bash
docker build -t yourusername/jarvondis:latest .
docker push yourusername/jarvondis:latest
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 PID
```

### Email Not Sending
1. Check SMTP credentials in .env
2. Verify Gmail app password (not account password)
3. Check firewall settings
4. Look at server logs for errors

### Import Errors
```bash
# Reinstall packages
pip install --force-reinstall -r requirements.txt
```

### Database Corruption
```bash
# Reset database (careful!)
rm users.json
```

---

## 📖 Documentation

- **API Docs**: See API_DOCS.md
- **Deployment**: See DEPLOYMENT.md
- **Contributing**: See CONTRIBUTING.md (coming soon)

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📝 License

MIT License - see LICENSE file

---

## 🆘 Support

- 📧 Email: support@jarvondis.com
- 💬 Discord: [Join Community](https://discord.gg/jarvondis)
- 🐛 Issues: [GitHub Issues](https://github.com/CapLWS-SLC/Jarvondis-Smart-Chat/issues)

---

## 🎯 Roadmap

### Version 2.1 (Next)
- Multi-language support (50+ languages)
- Voice input/output
- Real-time WebSocket chat
- Advanced NLP models

### Version 2.5
- Mobile app (iOS/Android)
- Plugin system
- Advanced admin dashboard
- Video tutorials

### Version 3.0
- GPT-4 integration
- Code execution sandbox
- Team collaboration features
- Enterprise features

---

Happy chatting! 🚀
