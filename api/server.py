# Enhanced API with authentication, user management, and learning
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uuid

from jarvondis.core.engine import JarvondisEngine
from jarvondis.safety.filters import SafetyFilters
from jarvondis.policy.policy_engine import PolicyEngine
from jarvondis.persona.persona_engine import PersonaEngine
from jarvondis.memory.memory_engine import MemoryEngine
from jarvondis.orchestrator.tools.tool_registry import ToolRegistry
from jarvondis.orchestrator.task_engine import TaskEngine
from jarvondis.security.auth import SecurityManager
from jarvondis.security.email_connector import SMTPEmailConnector, EmailTemplates
from jarvondis.user.profile import UserProfile
from jarvondis.database.user_db import UserDatabase
from jarvondis.skills.skill_registry import SkillRegistry
from jarvondis.learning.adaptive_engine import AdaptiveLearningEngine

# ============= MODELS =============

class SignupRequest(BaseModel):
    email: str
    name: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    message: str
    user_id: str = None

class ChatResponse(BaseModel):
    response: str
    user_id: str
    personalized: bool = False

class UserPreferenceUpdate(BaseModel):
    key: str
    value: any

class SkillRequest(BaseModel):
    skill_name: str
    query: str

class SkillChainRequest(BaseModel):
    chain_name: str
    initial_query: str

# ============= INITIALIZATION =============

app = FastAPI(
    title="Jarvondis Smart Chat",
    description="Safety-first AI assistant with adaptive learning and skills",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
security_manager = SecurityManager()
email_connector = SMTPEmailConnector()

# Database
user_db = UserDatabase()

# Skills and Learning
skill_registry = SkillRegistry()
adaptive_engine = AdaptiveLearningEngine()

# Core modules
safety = SafetyFilters()
policy = PolicyEngine(rules=[])
persona = PersonaEngine(profile={"tone_prefix": "[Jarvondis] "})
memory = MemoryEngine(store={})
orchestrator = TaskEngine(SkillRegistry())
engine = JarvondisEngine(safety, policy, persona, memory, orchestrator)

# In-memory user profiles (for demo - use database in production)
user_profiles = {}
user_sessions = {}

# ============= UTILITY FUNCTIONS =============

def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """Verify JWT token and get current user."""
    token = credentials.credentials
    payload = security_manager.verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return payload

# ============= AUTHENTICATION ENDPOINTS =============

@app.post("/auth/signup")
def signup(request: SignupRequest):
    """
    🔐 Register new user with email and password
    
    - Validates email format
    - Validates password strength (8+ chars, upper, lower, number, special)
    - Sends verification email
    - Returns JWT token
    """
    # Validate email
    if not security_manager.validate_email(request.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check if user exists
    if user_db.get_user_by_email(request.email):
        raise HTTPException(status_code=409, detail="User already exists")
    
    # Validate password
    is_valid, message = security_manager.validate_password(request.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # Create user
    user_id = str(uuid.uuid4())
    password_hash = security_manager.hash_password(request.password)
    
    if not user_db.create_user(user_id, request.email, request.name, password_hash):
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    # Create user profile
    profile = UserProfile(user_id, request.email, request.name)
    user_profiles[user_id] = profile
    user_db.save_profile(user_id, profile.to_dict())
    
    # Generate verification token
    verification_token = security_manager.generate_verification_token(request.email)
    verification_link = f"http://localhost:3000/verify?token={verification_token}"
    
    # Send verification email
    subject, body = EmailTemplates.welcome_email(request.name, verification_link)
    email_connector.send_email(request.email, subject, body, html=True)
    
    # Create JWT token
    token = security_manager.create_token(user_id, request.email)
    
    return {
        "message": "User created successfully",
        "user_id": user_id,
        "token": token,
        "email_verification_sent": True
    }

@app.post("/auth/login")
def login(request: LoginRequest):
    """
    🔓 Login with email and password
    
    - Validates credentials
    - Returns JWT token
    - Records last login
    """
    user = user_db.get_user_by_email(request.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not security_manager.verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    user_db.update_user(request.email, {"last_login": datetime.utcnow().isoformat()})
    
    # Create token
    token = security_manager.create_token(user["user_id"], request.email)
    
    return {
        "token": token,
        "user_id": user["user_id"],
        "name": user["name"]
    }

@app.post("/auth/verify-email")
def verify_email(token: str):
    """
    ✅ Verify email with token from email link
    """
    payload = security_manager.verify_token(token)
    
    if not payload or payload.get("type") != "email_verification":
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    email = payload["email"]
    
    if not user_db.verify_email(email):
        raise HTTPException(status_code=500, detail="Failed to verify email")
    
    return {"message": "Email verified successfully"}

# ============= USER PROFILE ENDPOINTS =============

@app.get("/user/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    """
    👤 Get user profile with learning data
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile.to_dict()

@app.put("/user/preferences")
def update_preference(request: UserPreferenceUpdate, 
                     current_user: dict = Depends(get_current_user)):
    """
    ⚙️ Update user preferences
    
    - tone: neutral, formal, casual, friendly
    - response_length: short, medium, long
    - language: en, es, fr, etc.
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.update_preference(request.key, request.value)
    user_db.save_profile(user_id, profile.to_dict())
    
    return {"message": "Preference updated", "preference": request.key}

@app.get("/user/learning-analysis")
def get_learning_analysis(current_user: dict = Depends(get_current_user)):
    """
    📊 Get AI's learning analysis of user
    
    Returns:
    - Primary topics of interest
    - Skill progression
    - Learning pace
    - Engagement level
    - Skill recommendations
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    analysis = adaptive_engine.analyze_user_behavior(user_id, profile)
    
    return analysis

# ============= SKILLS ENDPOINTS =============

@app.get("/skills/available")
def get_available_skills(current_user: dict = Depends(get_current_user)):
    """
    🎯 Get skills available to user
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    available = skill_registry.get_available_skills(
        profile.skill_proficiency,
        profile.unlocked_skills
    )
    
    return {
        "unlocked_skills": profile.unlocked_skills,
        "available_skills": available,
        "proficiency": profile.skill_proficiency
    }

@app.post("/skills/execute")
def execute_skill(request: SkillRequest, 
                 current_user: dict = Depends(get_current_user)):
    """
    ⚡ Execute a specific skill
    
    Available skills:
    - search: Search the web
    - calculate: Math operations
    - summarize: Summarize text
    - keywords: Extract keywords
    - code_explain: Explain code (unlocks after progress)
    - brainstorm: Generate ideas (unlocks after progress)
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    skill = skill_registry.get_skill(request.skill_name)
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Check if user can use skill
    user_proficiency = profile.skill_proficiency.get(request.skill_name, {}).get("level", 0.0)
    if not skill.can_use(user_proficiency, profile.unlocked_skills):
        raise HTTPException(status_code=403, detail="Skill not available or unlocked")
    
    # Execute skill
    result = skill.execute(request.query)
    
    # Update skill proficiency
    profile.add_skill(request.skill_name, proficiency=user_proficiency + 0.05)
    profile.record_interaction("skill_use", request.skill_name, True)
    user_db.save_profile(user_id, profile.to_dict())
    
    # Track interaction for learning
    adaptive_engine.track_interaction(user_id, {
        "type": "skill_use",
        "skill": request.skill_name,
        "query": request.query,
        "success": True
    })
    
    return {
        "skill": request.skill_name,
        "result": result,
        "proficiency_increased": True
    }

@app.post("/skills/chain")
def execute_skill_chain(request: SkillChainRequest,
                       current_user: dict = Depends(get_current_user)):
    """
    🔗 Execute a chain of skills sequentially
    
    Example chains:
    - summarize_and_extract: Summarize then extract keywords
    - search_and_summarize: Search web then summarize results
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    result = skill_registry.execute_skill_chain(
        request.chain_name,
        request.initial_query
    )
    
    profile.record_interaction("skill_chain", request.chain_name, True)
    user_db.save_profile(user_id, profile.to_dict())
    
    return {
        "chain": request.chain_name,
        "result": result
    }

# ============= CHAT ENDPOINTS =============

@app.post("/chat")
def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    """
    💬 Send message and get personalized response
    
    Features:
    - Safety filtering
    - Personalized tone
    - Learning integration
    - Skill recommendations
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Process message
    response = engine.process(request.message)
    
    # Personalize based on user preferences
    personalized_response = adaptive_engine.personalize_response(
        user_id, profile, response
    )
    
    # Track interaction
    profile.record_interaction("chat", None, True)
    adaptive_engine.track_interaction(user_id, {
        "type": "chat",
        "message": request.message,
        "success": True
    })
    
    # Check for skill unlocks
    if profile.interaction_count % 10 == 0:
        recommendations = adaptive_engine.get_personalized_recommendations(user_id, profile)
        if recommendations:
            # Auto-unlock new skill
            for rec in recommendations:
                profile.unlock_skill(rec["skill"])
    
    user_db.save_profile(user_id, profile.to_dict())
    
    return ChatResponse(
        response=personalized_response,
        user_id=user_id,
        personalized=True
    )

# ============= ANALYTICS ENDPOINTS =============

@app.get("/analytics/dashboard")
def get_analytics_dashboard(current_user: dict = Depends(get_current_user)):
    """
    📈 Get comprehensive analytics dashboard
    """
    user_id = current_user["user_id"]
    profile = user_profiles.get(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    analysis = adaptive_engine.analyze_user_behavior(user_id, profile)
    
    return {
        "user_id": user_id,
        "name": profile.name,
        "interactions_total": profile.interaction_count,
        "skills_unlocked": len(profile.unlocked_skills),
        "analysis": analysis,
        "recommendations": adaptive_engine.get_personalized_recommendations(user_id, profile)
    }

# ============= HEALTH & STATUS =============

@app.get("/")
def root():
    return {
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

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    from datetime import datetime
    uvicorn.run(app, host="0.0.0.0", port=8000)
