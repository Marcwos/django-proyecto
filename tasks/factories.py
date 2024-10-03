from .models import Task

class TaskFactory:
    @staticmethod
    def create_task(task_type, **kwargs):
        if task_type == 'urgent':
            kwargs['important'] = True  # estas tareas sean importantes 
        else:
            kwargs['important'] = False
        return Task.objects.create(**kwargs)