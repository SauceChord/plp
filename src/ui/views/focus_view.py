import tkinter as tk
import threading
from tkinter import ttk, simpledialog
from src.core.task_model import TaskStatus

class FocusView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.task = self.app.state_manager.get_next_actionable_task()
        
        self._setup_ui()

    def _setup_ui(self):
        # Center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        container = ttk.Frame(self)
        container.grid(row=0, column=0)
        
        if not self.task:
            ttk.Label(container, text=self.app.loc.get("no_tasks"), font=("Helvetica", 16)).pack(pady=20)
            ttk.Button(container, text=self.app.loc.get("add_task"), command=self._add_task).pack(pady=10)
        else:
            ttk.Label(container, text=self.task.title, font=("Helvetica", 24, "bold"), wraplength=600).pack(pady=20)
            if self.task.description:
                ttk.Label(container, text=self.task.description, font=("Helvetica", 12), wraplength=600).pack(pady=10)
            
            btn_frame = ttk.Frame(container)
            btn_frame.pack(pady=30)
            
            ttk.Button(btn_frame, text=self.app.loc.get("done"), command=self._mark_done).pack(side=tk.LEFT, padx=10)
            ttk.Button(btn_frame, text=self.app.loc.get("blocked"), command=self._cant_do).pack(side=tk.LEFT, padx=10)
            ttk.Button(btn_frame, text=self.app.loc.get("skip"), command=self._skip).pack(side=tk.LEFT, padx=10)
            
            ttk.Button(container, text=self.app.loc.get("add_new_task"), command=self._add_task).pack(pady=20)

    def _mark_done(self):
        if self.task:
            self.app.state_manager.update_task_status(self.task.id, TaskStatus.COMPLETED)
            self.app.show_reward_view()

    def _cant_do(self):
        # Trigger breakdown
        if not self.task:
            return
            
        reason = simpledialog.askstring(self.app.loc.get("blocked"), self.app.loc.get("what_blocking"))
        if not reason:
            return

        self._set_loading_state(True)
        
        # Run in background thread
        thread = threading.Thread(target=self._resolve_block_async, args=(self.task.title, reason))
        thread.daemon = True
        thread.start()

    def _resolve_block_async(self, task_title, reason):
        subtasks = self.app.llm_service.resolve_block(task_title, reason, language=self.app.loc.language)
        # Schedule update on main thread
        self.after(0, self._handle_block_result, subtasks)

    def _handle_block_result(self, subtasks):
        self._set_loading_state(False)
        
        if subtasks:
            for st in subtasks:
                self.app.state_manager.add_task(st["title"], st.get("description", ""), parent_id=self.task.id)
            
            # Refresh view
            self.app.show_focus_view()
        else:
            tk.messagebox.showerror("Error", self.app.loc.get("error_resolve"))

    def _set_loading_state(self, is_loading):
        # Find the button frame to disable buttons
        # In this simple implementation, we might just show a modal or overlay
        # But let's just use a simple label injection for now as per plan
        
        # We need to access the container. In _setup_ui, container is a local var.
        # Let's make it an instance var or find it.
        # Actually, let's just rebuild the UI or use a busy cursor for simplicity + a label?
        # The plan said "disable buttons, show Thinking... label".
        
        # Let's assume we can find the children.
        # A cleaner way for this codebase is to clear the view and show a loading screen, 
        # or just modify the current view.
        
        if is_loading:
            self.config(cursor="watch")
            # Create a loading toplevel or just a label if we can find where to put it.
            # Since we don't have easy access to the container from here without refactoring _setup_ui,
            # let's just change the cursor and maybe show a message box that is non-blocking? 
            # No, message box is blocking.
            # Let's add a loading label to the bottom of self if it doesn't exist.
            
            self.loading_label = ttk.Label(self, text=self.app.loc.get("thinking"), font=("Helvetica", 14, "italic"))
            self.loading_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
            self.update() # Force update
        else:
            self.config(cursor="")
            if hasattr(self, 'loading_label'):
                self.loading_label.destroy()

    def _skip(self):
        if self.task:
            # Maybe just move to end of queue? Or mark skipped?
            # For now, let's mark skipped to see next.
            self.app.state_manager.update_task_status(self.task.id, TaskStatus.SKIPPED)
            self.app.show_focus_view()

    def _add_task(self):
        title = simpledialog.askstring(self.app.loc.get("new_task_title"), self.app.loc.get("new_task_prompt"))
        if title:
            self.app.state_manager.add_task(title)
            self.app.show_focus_view()
