from locust import HttpUser, task, between

class APIUser(HttpUser):
    #tempo di attesa tra un user e un altro possibile
    wait_time = between(1, 2)

    @task
    def make_prediction(self):
        payload = {"features": [[5.9, 3.0, 5.1, 1.8]]}
        self.client.post("/predict", json=payload)



        