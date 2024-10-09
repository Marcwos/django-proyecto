from .models import Task

class TaskBuilder:
    def __init__(self):
        self.task_type = 'personal'
        self.is_important = False
        self.is_soft = False
        self.title = ''
        self.description = ''

    def set_task_type(self, task_type):
        self.task_type = task_type
        return self

    def set_importance(self, is_important):
        self.is_important = is_important
        return self

    def set_soft(self, is_soft):
        self.is_soft = is_soft
        return self

    def set_title(self, title):
        self.title = title
        return self

    def set_description(self, description):
        self.description = description
        return self

    def build(self, user):
        # Aquí construyes la tarea con los valores seleccionados
        importance_tag = 'Importante' if self.is_important else 'Suave' if self.is_soft else 'Normal'
        task = Task(
            task_type=self.task_type,
            title=f"{self.title} - {importance_tag}",
            description=self.description,
            user=user
        )
        task.save()
        return task
