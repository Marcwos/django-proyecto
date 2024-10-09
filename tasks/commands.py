## este las clases que implementas el diseno de patron de comportamiento COMAND
from .models import Task
from .task_builder import TaskBuilder

class CreateTaskCommand:
    def __init__(self, user, title, description, task_type, is_important=False, is_soft=False):
        self.user = user
        self.title = title
        self.description = description
        self.task_type = task_type
        self.is_important = is_important
        self.is_soft = is_soft

    def execute(self):
        # Usa el Builder para construir la tarea
        builder = TaskBuilder()
        task = (builder.set_task_type(self.task_type)
                       .set_title(self.title)
                       .set_description(self.description)
                       .set_importance(self.is_important)
                       .set_soft(self.is_soft)
                       .build(self.user))


class UpdateTaskCommand:
    def __init__(self, task, **kwargs):
        self.task = task
        self.kwargs = kwargs  # Aquí puedes pasar todos los campos que quieres actualizar

    def execute(self):
        for key, value in self.kwargs.items():
            setattr(self.task, key, value)
        self.task.save()  # Guardar los cambios en la base de datos


class DeleteTaskCommand:
    def __init__(self, task):
        self.task = task

    def execute(self):
        print(f"Deleting task: {self.task.title}")  # Agrega un print para depuración
        self.task.delete()  # Elimina la tarea de la base de datos

