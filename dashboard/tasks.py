# Create your tasks here
from celery import shared_task, task


@task()
def printHello():
    return "Hello"
