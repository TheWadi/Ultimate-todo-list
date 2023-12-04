import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
from gettext import gettext as _

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('The Ultimate To-Do List')
        self.geometry('400x300')

        self.task_entry = ttk.Entry(self)
        self.task_entry.pack(pady=10)

        self.add_task_button = ttk.Button(self, text=_('Add Task'), command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.tasks_frame = ttk.Frame(self)
        self.tasks_frame.pack(fill='both', expand=True)

        self.translator = Translator(language='en') 
        self.create_menu()

        self.task_widgets = []

        self.last_file_path = None
        self.load_last_file_tasks()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_('File'), menu=file_menu)
        file_menu.add_command(label=_('Save'), command=self.save_tasks)
        file_menu.add_command(label=_('Load'), command=self.load_tasks)

        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=_('Language'), menu=language_menu)
        language_menu.add_command(label=_('English'), command=lambda: self.change_language('en'))
        language_menu.add_command(label=_('Français'), command=lambda: self.change_language('fr'))
        language_menu.add_command(label=_('Español'), command=lambda: self.change_language('es'))

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            var = tk.BooleanVar()
            task = ttk.Checkbutton(self.tasks_frame, text=task_text, variable=var)
            task.pack(anchor='w')
            task.bind("<Button-3>", lambda event, task=task: self.show_context_menu(event, task))
            self.task_entry.delete(0, tk.END)
            self.task_widgets.append((task, var))
        else:
            messagebox.showwarning(_('warning'), self.translator.translate('enter_task_name'))

    def show_context_menu(self, event, task):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label=self.translator.translate('edit_task'), command=lambda task=task: self.edit_task(task))
        context_menu.add_command(label=self.translator.translate('delete_task'), command=lambda task=task: self.delete_task(task))
        context_menu.post(event.x_root, event.y_root)

    def edit_task(self, task):
        new_text = simpledialog.askstring(self.translator.translate('edit_task'), self.translator.translate('enter_new_task'), parent=self)
        if new_text:
            for (child, var) in self.task_widgets:
                if child.cget('text') == task.cget('text'):
                    child.config(text=new_text)
                    break
        else:
            messagebox.showwarning(_('warning'), self.translator.translate('enter_task_name'))

    def delete_task(self, task):
        result = messagebox.askyesno(self.translator.translate('delete_task'), self.translator.translate('confirm_delete'), parent=self)
        if result:
            for i, (child, var) in enumerate(self.task_widgets):
                if child.cget('text') == task.cget('text'):
                    child.destroy()
                    del self.task_widgets[i]
                    break

    def toggle_task(self, task_text):
        for (child, var) in self.task_widgets:
            if child.cget('text') == task_text:
                current_state = var.get()
                var.set(not current_state)
                break

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if file_path:
            with open(file_path, 'w') as file:
                for (child, var) in self.task_widgets:
                    task_text = child.cget('text')
                    task_state = var.get()
                    file.write(f'{task_text},{task_state}\n')
            self.last_file_path = file_path

    def load_tasks(self):
        file_path = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if file_path:
            self.load_tasks_from_file(file_path)
            self.last_file_path = file_path

    def load_last_file_tasks(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tasks_file_path = os.path.join(script_dir, 'tasks.txt')
        if os.path.exists(tasks_file_path):
            result = messagebox.askyesno(self.translator.translate('load_tasks'), self.translator.translate('load_from_tasks_txt'), parent=self)
            if result:
                self.load_tasks_from_file(tasks_file_path)

    def load_tasks_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    task_text, task_state_str = line.strip().split(',')
                    task_state = task_state_str.lower() == 'true'
                    var = tk.BooleanVar(value=task_state)
                    task = ttk.Checkbutton(self.tasks_frame, text=task_text, variable=var)
                    task.pack(anchor='w')
                    self.task_widgets.append((task, var))
                    task.state(['selected']) if task_state else task.state(['!selected'])
        except FileNotFoundError:
            pass

    def change_language(self, language):
        self.translator = Translator(language=language)
        # Mettez à jour les éléments du menu et les autres textes dans l'interface utilisateur
        self.update_ui_text()

    def update_ui_text(self):
        # Mettez à jour les éléments du menu et les autres textes dans l'interface utilisateur en fonction de la langue actuelle
        self.add_task_button.config(text=self.translator.translate('add_task'))

class Translator:
    def __init__(self, language='en'):
        self.language = language
        self.translations = self.load_translations()

    def load_translations(self):
        translations = {
            'en': {
                'add_task': 'Add Task',
                'save': 'Save',
                'load': 'Load',
                'edit_task': 'Edit Task',
                'enter_new_task': 'Enter new task name:',
                'delete_task': 'Delete Task',
                'confirm_delete': 'Are you sure you want to delete this task?',
                'enter_task_name': 'Please enter a task name.',
                'load_tasks': 'Load Tasks',
                'load_from_tasks_txt': 'Do you want to load tasks from \'tasks.txt\'?',
                'file': 'File',
                'language': 'Language',
                'warning': 'Warning',
            },
            'fr': {
                'add_task': 'Ajouter une tâche',
                'save': 'Enregistrer',
                'load': 'Charger',
                'edit_task': 'Éditer la tâche',
                'enter_new_task': 'Entrez le nouveau nom de la tâche :',
                'delete_task': 'Supprimer la tâche',
                'confirm_delete': 'Êtes-vous sûr de vouloir supprimer cette tâche ?',
                'enter_task_name': 'Veuillez entrer un nom de tâche.',
                'load_tasks': 'Charger les tâches',
                'load_from_tasks_txt': 'Voulez-vous charger les tâches depuis \'tasks.txt\' ?',
                'file': 'Fichier',
                'language': 'Langue',
                'warning': 'Avertissement',
            },
            'es': {
                'add_task': 'Agregar una tarea',
                'save': 'Guardar',
                'load': 'Cargar',
                'edit_task': 'Editar tarea',
                'enter_new_task': 'Ingrese el nuevo nombre de la tarea:',
                'delete_task': 'Eliminar tarea',
                'confirm_delete': '¿Estás seguro de querer eliminar esta tarea?',
                'enter_task_name': 'Por favor, ingrese un nombre de tarea.',
                'load_tasks': 'Cargar tareas',
                'load_from_tasks_txt': '¿Quieres cargar las tareas desde \'tasks.txt\' ?',
                'file': 'Archivo',
                'language': 'Idioma',
                'warning': 'Advertencia',
            },
        }

        return translations.get(self.language, translations['en'])

    def translate(self, key):
        return self.translations.get(key, key)

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
