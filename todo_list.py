import tkinter as tk
from tkinter import simpledialog, messagebox

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

        # Load tasks from file on startup
        self.load_tasks()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task = tk.Checkbutton(self.tasks_frame, text=task_text, command=lambda task=task_text: self.toggle_task(task))
            task.pack(anchor='w')
            task.bind("<Button-3>", lambda event, task=task: self.show_context_menu(event, task))
            self.task_entry.delete(0, tk.END)

            # Save tasks to file after adding a new task
            self.save_tasks()
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
            for child in self.tasks_frame.winfo_children():
                if child.cget("text") == task:
                    child.config(text=new_text)
                    break
            # Save tasks to file after editing a task
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")

    def delete_task(self, task):
        result = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?", parent=self)
        if result:
            # Find and remove the task widget
            for child in self.tasks_frame.winfo_children():
                if child.cget("text") == task:
                    child.destroy()
                    break
            # Save tasks to file after deleting a task
            self.save_tasks()

    def toggle_task(self, task_text):
        # Find and update the task widget
        for child in self.tasks_frame.winfo_children():
            if child.cget("text") == task_text:
                current_state = child.instate(['selected'])
                child.deselect() if current_state else child.select()
                break
        # Save tasks to file after toggling a task
        self.save_tasks()

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for child in self.tasks_frame.winfo_children():
                task_text = child.cget("text")
                task_state = child.instate(['selected'])
                file.write(f"{task_text},{task_state}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for line in file:
                    task_text, task_state_str = line.strip().split(',')
                    task_state = task_state_str.lower() == 'true'
                    task = tk.Checkbutton(self.tasks_frame, text=task_text, command=lambda t=task_text: self.toggle_task(t))
                    task.pack(anchor='w')
                    task.select() if task_state else task.deselect()
        except FileNotFoundError:
            pass  # If the file doesn't exist, do nothing (no tasks to load)

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
