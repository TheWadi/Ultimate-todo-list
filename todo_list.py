import tkinter as tk
from tkinter import messagebox

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
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task name.")

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
