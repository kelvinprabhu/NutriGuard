# ==================== FILE: services/ai_agents/base_agent.py ====================
"""Base Agent class with common functionality"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool
import json
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, 
                 model: str = "gemini-2.5-pro",
                 api_key: str = "AIzaSyBq3XbBUGmQDZefsnpkA2EyUs_4t52PacE",
                 temperature: float = 0.1):
        """
        Initialize base agent with LLM
        
        Args:
            model: Gemini model name
            api_key: Google AI API key
            temperature: Temperature for generation
        """
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            max_retries=3,
        )
        self.agent_name = self.__class__.__name__
        logger.info(f"Initialized {self.agent_name}")
    
    def _clean_json_response(self, response: str) -> str:
        """Clean LLM response to extract pure JSON"""
        response = response.strip()
        
        # Remove markdown code blocks
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        
        if response.endswith("```"):
            response = response[:-3]
        
        response = response.strip()
        
        # Find first { and last }
        start = response.find('{')
        end = response.rfind('}')
        
        if start != -1 and end != -1:
            response = response[start:end+1]
        
        return response
    
    def _parse_json_response(self, response: Any) -> Dict[str, Any]:
        """Parse LLM response to JSON"""
        try:
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            cleaned = self._clean_json_response(response_text)
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error in {self.agent_name}: {e}")
            logger.error(f"Raw response: {response_text[:500]}")
            raise ValueError(f"Failed to parse JSON response: {e}")
    
    def invoke_with_search(self, prompt: PromptTemplate, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke LLM with Google Search tool"""
        chain = prompt | self.llm
        response = chain.invoke(
            variables,
            tools=[GenAITool(google_search={})]
        )
        return self._parse_json_response(response)
    
    def invoke(self, prompt: PromptTemplate, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke LLM without tools"""
        chain = prompt | self.llm
        response = chain.invoke(variables)
        return self._parse_json_response(response)
