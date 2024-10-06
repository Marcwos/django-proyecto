## este las clases que implementas el diseno de patron de comportamiento COMAND
from .models import Task

class TaskCommand:
    def execute(self):
        raise NotImplementedError("Debes implementar el método 'execute' en las clases hijas.")

class CreateTaskCommand(TaskCommand):
    def __init__(self, user, title, description, task_type):
        self.user = user
        self.title = title
        self.description = description
        self.task_type = task_type


    def execute(self):
        task = Task.objects.create(
            user=self.user,
            title=self.title,
            description=self.description,
            task_type=self.task_type
        )
        return task

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

