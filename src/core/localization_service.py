import json
import os

class LocalizationService:
    def __init__(self, language="en"):
        self.language = language
        self.translations = {
            "en": {
                "no_tasks": "No tasks! You are free.",
                "add_task": "Add Task",
                "add_new_task": "Add New Task",
                "done": "Done",
                "blocked": "I feel blocked",
                "skip": "Skip",
                "what_blocking": "What is blocking you?",
                "thinking": "Thinking... Please wait.",
                "error_resolve": "Could not resolve block.",
                "great_job": "Great Job! 💪",
                "reward_desc": "Do whatever you want for a while.",
                "earned_it": "You earned it! 🎉",
                "ready_again": "I am ready again!",
                "new_task_prompt": "What do you need to do?",
                "new_task_title": "New Task"
            },
            "sv": {
                "no_tasks": "Inga uppgifter! Du är fri.",
                "add_task": "Lägg till uppgift",
                "add_new_task": "Lägg till ny uppgift",
                "done": "Klar",
                "blocked": "Jag känner mig blockerad",
                "skip": "Hoppa över",
                "what_blocking": "Vad blockerar dig?",
                "thinking": "Tänker... Vänta.",
                "error_resolve": "Kunde inte lösa blockeringen.",
                "great_job": "Bra jobbat! 💪",
                "reward_desc": "Gör vad du vill en stund.",
                "earned_it": "Du förtjänar det! 🎉",
                "ready_again": "Jag är redo igen!",
                "new_task_prompt": "Vad behöver du göra?",
                "new_task_title": "Ny uppgift"
            }
        }

    def get(self, key):
        return self.translations.get(self.language, self.translations["en"]).get(key, key)

    def set_language(self, language):
        if language in self.translations:
            self.language = language
