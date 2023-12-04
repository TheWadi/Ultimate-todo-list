import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('The Ultimate To-Do List')
        self.geometry('400x300')

        self.task_entry = tk.Entry(self)
        self.task_entry.pack(pady=10)

        self.add_task_button = tk.Button(self, text='Add Task', command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.tasks_frame = tk.Frame(self)
        self.tasks_frame.pack(fill='both', expand=True)

        self.create_menu()

        self.task_widgets = []

        self.last_file_path = None


        self.load_last_file_tasks()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_tasks)
        file_menu.add_command(label="Load", command=self.load_tasks)

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            var = tk.BooleanVar()
            task = tk.Checkbutton(self.tasks_frame, text=task_text, variable=var)
            task.pack(anchor='w')
            task.bind("<Button-3>", lambda event, task=task: self.show_context_menu(event, task))
            self.task_entry.delete(0, tk.END)

            # Add Checkbutton and BooleanVar to the list
            self.task_widgets.append((task, var))
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")

    def show_context_menu(self, event, task):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda task=task: self.edit_task(task))
        context_menu.add_command(label="Delete", command=lambda task=task: self.delete_task(task))
        context_menu.post(event.x_root, event.y_root)

    def edit_task(self, task):
        new_text = simpledialog.askstring("Edit Task", "Enter new task name:", parent=self)
        if new_text:
            # Find and update the task widget
            for (child, var) in self.task_widgets:
                if child.cget("text") == task.cget("text"):
                    child.config(text=new_text)
                    break
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")

    def delete_task(self, task):
        result = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?", parent=self)
        if result:
            # Find and remove the task widget
            for i, (child, var) in enumerate(self.task_widgets):
                if child.cget("text") == task.cget("text"):
                    child.destroy()
                    del self.task_widgets[i]
                    break

    def toggle_task(self, task_text):
        # Find and update the task widget
        for (child, var) in self.task_widgets:
            if child.cget("text") == task_text:
                current_state = var.get()
                var.set(not current_state)
                break

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for (child, var) in self.task_widgets:
                    task_text = child.cget("text")
                    task_state = var.get()
                    file.write(f"{task_text},{task_state}\n")
            self.last_file_path = file_path

    def load_tasks(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.load_tasks_from_file(file_path)
            self.last_file_path = file_path

    def load_last_file_tasks(self):
        # Check if "tasks.txt" exists in the same directory as the exe (sonic.exe ref ???)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tasks_file_path = os.path.join(script_dir, "tasks.txt")

        if os.path.exists(tasks_file_path):
            result = messagebox.askyesno("Load Tasks", "Do you want to load tasks from 'tasks.txt'?", parent=self)
            if result:
                self.load_tasks_from_file(tasks_file_path)

    def load_tasks_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                for line in file:
                    task_text, task_state_str = line.strip().split(',')
                    task_state = task_state_str.lower() == 'true'
                    var = tk.BooleanVar(value=task_state)
                    task = tk.Checkbutton(self.tasks_frame, text=task_text, variable=var)
                    task.pack(anchor='w')
                    self.task_widgets.append((task, var))
                    task.select() if task_state else task.deselect()
        except FileNotFoundError:
            pass  # If the file doesn't exist, do nothing (no tasks to load)

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
