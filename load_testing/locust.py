from locust import HttpUser, task, between, TaskSet

class UserBehavior(TaskSet):
    """
    @task(3)
    def view_home(self):
        response = self.client.get("/")


    @task(1)
    def view_post(self):
        response = self.client.get("/news/owr-work/healthcare/mobile-healthcare-clinics.html")

    @task(1)
    def view_post_list(self):
        response = self.client.get("/news")


    @task(1)
    def view_post_tr_post(self):
        response = self.client.get("/ru/news/owr-work/healthcare/mobile-healthcare-clinics.html")



    @task(1)
    def view_post_tr_list(self):
        response = self.client.get("/ru/news")


    @task(1)
    def view_post_tr_donation(self):
        response = self.client.get("/ru/donations/")

    @task(1)
    def view_post_tr_static(self):
        response = self.client.get("/ru/contacts.html")


    @task(1)
    def view_about(self):
        response = self.client.get("/about.html")


 """

    @task(1)
    def view_post_tr_cat(self):
        response = self.client.get("/ru/news/owr-work")


"""
    @task(1)
    def view_post(self):
        response = self.client.get("/ru/news/owr-work/healthcare/mobile-healthcare-clinics.html")
"""
class WebsiteUser(HttpUser):
    #host = "http://localhost:8000"
    host = "http://dj.local"
    tasks = [UserBehavior]
    wait_time = between(1, 3)
