import tkinter as tk
from tkinter import ttk, messagebox
from src.core.state_manager import StateManager
from src.core.llm_service import LLMService
from src.core.localization_service import LocalizationService
from src.ui.views.focus_view import FocusView
from src.ui.views.reward_view import RewardView
# from src.ui.views.tree_view import TreeView # TODO

class FrontalLobeApp:
    def __init__(self, root):
        self.root = root
        self.state_manager = StateManager()
        self.llm_service = LLMService()
        
        # Load language from config (using LLMService's config loader or separate?)
        # For simplicity, let's peek at the config via LLMService or just load it again.
        # Ideally StateManager or a ConfigManager should handle this.
        # Let's just default to 'en' and check if we can get it from LLMService which loads config.
        # Actually LLMService loads config internally. Let's make a quick helper or just re-read.
        # Re-reading is safe enough for now.
        import json
        import os
        config_path = "config.json"
        language = "en"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    language = config.get("language", "en")
            except:
                pass
        
        self.loc = LocalizationService(language)

        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.current_view = None
        self.show_focus_view()

    def show_focus_view(self):
        self._clear_view()
        self.current_view = FocusView(self.main_container, self)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_reward_view(self):
        self._clear_view()
        self.current_view = RewardView(self.main_container, self)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def _clear_view(self):
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
