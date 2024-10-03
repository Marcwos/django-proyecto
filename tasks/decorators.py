from .models import Task

# Decorador base
class TaskDecorator:
    def __init__(self, task):
        self.task = task

    def display_title(self):
        return self.task.title

# Decorador para tareas urgentes
class UrgentTaskDecorator(TaskDecorator):
    def display_title(self):
        return f"🔥 [URGENT] {self.task.title}"

# Decorador para tareas importantes
class ImportantTaskDecorator(TaskDecorator):
    def display_title(self):
        return f"✔️ [IMPORTANT] {self.task.title}"

# Decorador para tareas normales
class NormalTaskDecorator(TaskDecorator):
    def display_title(self):
        return self.task.title
