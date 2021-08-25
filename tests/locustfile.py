from locust import HttpUser, TaskSet, between, task, tag
from random import choice

boards = ['b', 'cat', 'dev', 'news']


class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def index(self):
        self.client.get('/')

    @task
    def boards(self):
        self.client.get('/' + choice(boards))
