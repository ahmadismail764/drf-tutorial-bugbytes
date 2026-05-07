from tasks.models import Task, TaskStatus, InProgressTask, TodoTask, CompletedTask

def run():
    x = CompletedTask.objects.all()
    print(x)
