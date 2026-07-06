# Skill system for customizable AI capabilities
from typing import Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum

class SkillCategory(Enum):
    """Skill categories."""
    UTILITY = "utility"  # search, calculate
    LEARNING = "learning"  # summarize, explain
    PRODUCTIVITY = "productivity"  # organize, plan
    CREATIVE = "creative"  # brainstorm, write
    ANALYSIS = "analysis"  # analyze, compare

class Skill:
    """Represents a callable skill/tool with metadata."""
    
    def __init__(self, name: str, description: str, category: SkillCategory,
                 function: Callable, required_proficiency: float = 0.0,
                 unlock_requirements: Dict = None):
        self.name = name
        self.description = description
        self.category = category
        self.function = function
        self.required_proficiency = required_proficiency
        self.unlock_requirements = unlock_requirements or {}
        self.created_at = datetime.utcnow()
        self.usage_count = 0
    
    def can_use(self, user_proficiency: float, unlocked_skills: List[str]) -> bool:
        """Check if user can use this skill."""
        if self.name not in unlocked_skills:
            return False
        if user_proficiency < self.required_proficiency:
            return False
        return True
    
    def execute(self, query: str, context: Dict = None) -> str:
        """Execute the skill function."""
        try:
            self.usage_count += 1
            result = self.function(query, context or {})
            return result
        except Exception as e:
            return f"Skill execution error: {str(e)}"

class SkillRegistry:
    """Central registry for all available skills, like Microsoft Copilot."""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.skill_chains: Dict[str, List[str]] = {}  # Skill combinations
        self._initialize_core_skills()
    
    def _initialize_core_skills(self):
        """Initialize built-in skills."""
        # Existing tools from tool_registry
        from orchestrator.tools.web import WebTool
        from orchestrator.tools.math import MathTool
        from orchestrator.tools.nlp import NLPTool
        from orchestrator.tools.system import SystemTool
        
        web_tool = WebTool()
        math_tool = MathTool()
        nlp_tool = NLPTool()
        system_tool = SystemTool()
        
        # Register core skills
        self.register_skill(
            Skill(
                name="search",
                description="Search the web for information",
                category=SkillCategory.UTILITY,
                function=lambda q, ctx: web_tool.run(q)
            )
        )
        
        self.register_skill(
            Skill(
                name="calculate",
                description="Perform mathematical calculations",
                category=SkillCategory.UTILITY,
                function=lambda q, ctx: math_tool.run(q)
            )
        )
        
        self.register_skill(
            Skill(
                name="summarize",
                description="Summarize text content",
                category=SkillCategory.LEARNING,
                function=lambda q, ctx: nlp_tool.run("summarize", q)
            )
        )
        
        self.register_skill(
            Skill(
                name="keywords",
                description="Extract keywords from text",
                category=SkillCategory.LEARNING,
                function=lambda q, ctx: nlp_tool.run("keywords", q)
            )
        )
        
        self.register_skill(
            Skill(
                name="system_info",
                description="Get system information",
                category=SkillCategory.UTILITY,
                function=lambda q, ctx: system_tool.run(q)
            )
        )
        
        # Advanced skills requiring proficiency
        self.register_skill(
            Skill(
                name="code_explain",
                description="Explain code in detail",
                category=SkillCategory.LEARNING,
                required_proficiency=0.3,
                function=self._code_explain_impl
            )
        )
        
        self.register_skill(
            Skill(
                name="brainstorm",
                description="Generate creative ideas",
                category=SkillCategory.CREATIVE,
                required_proficiency=0.5,
                function=self._brainstorm_impl
            )
        )
    
    def register_skill(self, skill: Skill):
        """Register a new skill."""
        self.skills[skill.name] = skill
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self.skills.get(name)
    
    def get_available_skills(self, user_proficiency: Dict[str, float], 
                            unlocked_skills: List[str]) -> List[str]:
        """Get list of skills available to user."""
        available = []
        for skill_name in unlocked_skills:
            if skill_name in self.skills:
                user_prof = user_proficiency.get(skill_name, 0.0)
                if self.skills[skill_name].can_use(user_prof, unlocked_skills):
                    available.append(skill_name)
        return available
    
    def create_skill_chain(self, chain_name: str, skills: List[str]):
        """Create a chain of skills to execute sequentially."""
        self.skill_chains[chain_name] = skills
    
    def execute_skill_chain(self, chain_name: str, initial_query: str, 
                           context: Dict = None) -> str:
        """Execute a chain of skills sequentially."""
        if chain_name not in self.skill_chains:
            return f"Skill chain '{chain_name}' not found""
        
        result = initial_query
        for skill_name in self.skill_chains[chain_name]:
            skill = self.get_skill(skill_name)
            if skill:
                result = skill.execute(result, context)
            else:
                return f"Skill '{skill_name}' not found in chain"
        
        return result
    
    @staticmethod
    def _code_explain_impl(query: str, context: Dict) -> str:
        """Explain code functionality."""
        return f"[Code Explanation] {query[:100]}..."
    
    @staticmethod
    def _brainstorm_impl(query: str, context: Dict) -> str:
        """Generate brainstorm ideas."""
        return f"[Brainstorm Ideas for: {query}]\n1. Idea 1\n2. Idea 2\n3. Idea 3"
