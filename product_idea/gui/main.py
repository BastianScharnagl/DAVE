import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Path to store tasks
TASKS_FILE = "../storage/tasks.json"


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, 'r') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(TASKS_FILE, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
    
    def add_task(self, title, priority, effort, deadline):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'priority': priority,
            'effort': effort,
            'deadline': deadline,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                return True
        return False
    
    def get_pending_tasks(self):
        """Get all pending tasks sorted by priority"""
        pending = [t for t in self.tasks if not t['completed']]
        return sorted(pending, key=lambda x: x['priority'], reverse=True)


class SmartTaskOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Optimizer")
        self.root.geometry("800x600")
        
        # Initialize task manager
        self.task_manager = TaskManager()
        
        # Create GUI elements
        self.create_menu()
        self.create_main_frame()
        self.create_task_form()
        self.create_tasks_list()
        
        # Load initial data
        self.refresh_tasks_list()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_frame(self):
        """Create main frame"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
    
    def create_task_form(self):
        """Create task input form"""
        form_frame = ttk.LabelFrame(self.main_frame, text="Add New Task", padding="10")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        form_frame.columnconfigure(1, weight=1)
        
        # Task title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(form_frame, textvariable=self.title_var, width=40)
        title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Priority
        ttk.Label(form_frame, text="Priority:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.priority_var = tk.IntVar(value=5)
        priority_spinbox = ttk.Spinbox(form_frame, from_=1, to=10, textvariable=self.priority_var, width=5)
        priority_spinbox.grid(row=0, column=3, padx=(0, 10))
        
        # Effort
        ttk.Label(form_frame, text="Effort:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.effort_var = tk.IntVar(value=5)
        effort_spinbox = ttk.Spinbox(form_frame, from_=1, to=10, textvariable=self.effort_var, width=5)
        effort_spinbox.grid(row=0, column=5, padx=(0, 10))
        
        # Deadline
        ttk.Label(form_frame, text="Deadline:").grid(row=0, column=6, sticky=tk.W, padx=(0, 5))
        self.deadline_var = tk.StringVar()
        deadline_entry = ttk.Entry(form_frame, textvariable=self.deadline_var, width=12)
        deadline_entry.grid(row=0, column=7)
        ttk.Label(form_frame, text="(YYYY-MM-DD)").grid(row=0, column=8, sticky=tk.W, padx=(5, 0))
        
        # Add task button
        add_button = ttk.Button(form_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=9, padx=(10, 0))
        
        # Bind Enter key to add task
        self.root.bind('<Return>', lambda event: self.add_task())
    
    def create_tasks_list(self):
        """Create tasks list view"""
        list_frame = ttk.LabelFrame(self.main_frame, text="Tasks", padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = ('id', 'title', 'priority', 'effort', 'deadline', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('priority', text='Priority')
        self.tree.heading('effort', text='Effort')
        self.tree.heading('deadline', text='Deadline')
        self.tree.heading('status', text='Status')
        
        # Define columns
        self.tree.column('id', width=50, anchor=tk.CENTER)
        self.tree.column('title', width=200, anchor=tk.W)
        self.tree.column('priority', width=100, anchor=tk.CENTER)
        self.tree.column('effort', width=100, anchor=tk.CENTER)
        self.tree.column('deadline', width=100, anchor=tk.CENTER)
        self.tree.column('status', width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons frame
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Complete button
        complete_button = ttk.Button(buttons_frame, text="Mark as Completed", command=self.complete_task)
        complete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Refresh button
        refresh_button = ttk.Button(buttons_frame, text="Refresh", command=self.refresh_tasks_list)
        refresh_button.pack(side=tk.LEFT)
    
    def add_task(self):
        """Add a new task from form input"""
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Task title is required")
            return
        
        try:
            priority = self.priority_var.get()
            effort = self.effort_var.get()
            deadline = self.deadline_var.get().strip()
            
            # Validate deadline format
            if deadline:
                datetime.strptime(deadline, '%Y-%m-%d')
            
            # Add task
            task = self.task_manager.add_task(title, priority, effort, deadline)
            
            # Clear form
            self.title_var.set("")
            self.priority_var.set(5)
            self.effort_var.set(5)
            self.deadline_var.set("")
            
            # Refresh list
            self.refresh_tasks_list()
            
            messagebox.showinfo("Success", "Task added successfully")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {e}")
    
    def complete_task(self):
        """Mark selected task as completed"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to complete")
            return
        
        # Get task ID from selected item
        item = self.tree.item(selection[0])
        task_id = item['values'][0]
        
        # Confirm completion
        if messagebox.askyesno("Confirm", "Mark this task as completed?"):
            if self.task_manager.complete_task(task_id):
                self.refresh_tasks_list()
                messagebox.showinfo("Success", "Task marked as completed")
            else:
                messagebox.showerror("Error", "Failed to complete task")
    
    def refresh_tasks_list(self):
        """Refresh the tasks list view"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add tasks
        for task in self.task_manager.get_pending_tasks():
            status = "Pending" if not task['completed'] else "Completed"
            self.tree.insert('', tk.END, values=(
                task['id'],
                task['title'],
                task['priority'],
                task['effort'],
                task['deadline'],
                status
            ))
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Smart Task Optimizer
Version 0.1

A smart task management system that learns from user behavior to optimize productivity.

Features:
- Task management with priority, effort, and deadline attributes
- Intelligent priority scoring algorithm
- Optimal schedule generation
- Machine learning model for user behavior prediction
- Graphical user interface
- Data persistence

© 2025 Smart Task Optimizer. All rights reserved.
"""
        messagebox.showinfo("About", about_text)


def main():
    root = tk.Tk()
    app = SmartTaskOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()