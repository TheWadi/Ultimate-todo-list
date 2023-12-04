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

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            task = tk.Checkbutton(self.tasks_frame, text=task_text)
            task.pack(anchor='w')
            task.bind("<Button-3>", lambda event, task=task: self.show_context_menu(event, task))
            self.task_entry.delete(0, tk.END)
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
            task.config(text=new_text)
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")

    def delete_task(self, task):
        result = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?", parent=self)
        if result:
            task.destroy()

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
