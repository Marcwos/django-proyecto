from .models import Task

# Decorador base
class TaskDecorator:
    def __init__(self, task):
        self.task = task

    def display_title(self):
        return self.task.title

# Decorador para tareas urgentes
class UniversidadTaskDecorator(TaskDecorator):
    def display_title(self):
        return f"📓 [Uni] {self.task.title}"

# Decorador para tareas importantes
class LaboralTaskDecorator(TaskDecorator):
    def display_title(self):
        return f"💸 [Laboral] {self.task.title}"

# Decorador para tareas normales
class PersonalTaskDecorator(TaskDecorator):
    def display_title(self):
        return f"🙋 [Personal] {self.task.title}"
