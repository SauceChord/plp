import json
import os
from typing import List, Dict
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class LLMService:
    def __init__(self, config_path: str = "config.json"):
        self.api_key = None
        self.model = "gpt-4o-mini"
        self.client = None
        self.base_url = None
        self._load_config(config_path)
        
        if self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def _load_config(self, config_path):
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get("openai_api_key")
                    self.model = config.get("model", "gpt-4o-mini")
                    self.base_url = config.get("llm_base_url")
            except Exception as e:
                print(f"Error loading config: {e}")

    def break_down_task(self, task_title: str, task_description: str = "") -> List[Dict[str, str]]:
        """
        Returns a list of subtasks in the format: [{"title": "...", "description": "..."}]
        """
        if not self.client:
            # Mock response if no client/key
            return [
                {"title": f"Step 1 for {task_title}", "description": "First step"},
                {"title": f"Step 2 for {task_title}", "description": "Second step"},
            ]

        prompt = f"""
        You are an executive function assistant. The user is overwhelmed by the task: "{task_title}".
        Description: "{task_description}"
        
        Break this task down into 3-5 smaller, manageable steps. 
        Return ONLY a JSON array of objects with "title" and "description" keys.
        Example:
        [
            {{"title": "Get the vacuum", "description": "Bring it to the room"}},
            {{"title": "Clear the floor", "description": "Pick up large items"}}
        ]
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that breaks down tasks."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            result = json.loads(content)
            # Handle if the LLM returns a wrapper key like "tasks": [...]
            if isinstance(result, dict):
                for key in result:
                    if isinstance(result[key], list):
                        return result[key]
                return [] # Could not find list
            return result
        except Exception as e:
            print(f"LLM Error: {e}")
            return []

    def resolve_block(self, task_title: str, block_reason: str, language: str = "en") -> List[Dict[str, str]]:
        """
        Returns a list of subtasks to resolve a specific block.
        """
        if not self.client:
            # Mock response
            return [
                {"title": f"Address: {block_reason}", "description": "First step to unblock"},
                {"title": "Continue task", "description": "Resume original work"},
            ]

        prompt = f"""
        You are an executive function assistant. The user is blocked on the task: "{task_title}".
        The user says: "{block_reason}"
        
        Provide 2-4 concrete, small steps to resolve this specific blocker and get back on track.
        Reply in {language}.
        Return ONLY a JSON array of objects with "title" and "description" keys.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that resolves blocks."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            result = json.loads(content)
            
            if isinstance(result, dict):
                for key in result:
                    if isinstance(result[key], list):
                        return result[key]
                return []
            return result
        except Exception as e:
            print(f"LLM Error: {e}")
            return []
