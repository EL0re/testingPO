from locust import HttpUser, task, between


class OpenBMCUser(HttpUser):
    host = "https://127.0.0.1:2443"

    @task(1)
    def get_system_info(self):
        self.client.get("/redfish/v1/Systems/system", auth=("root", "0penBmc"), verify=False, name="OpenBMC /Systems/system")

    @task(1)
    def get_power_state(self):
        with self.client.get("/redfish/v1/Systems/system", auth=("root", "0penBmc"), verify=False, catch_response=True, name="OpenBMC /Systems/system") as response:
            if response.status_code == 200:
                power_state = response.json().get("PowerState", "Unknown")
                print(f"PowerState: {power_state}")
                response.success()
            else:
                response.failure("Не удалось получить PowerState")


class PublicAPITestUser(HttpUser):
    host = ""

    @task(1)
    def get_posts(self):
        self.client.get("https://jsonplaceholder.typicode.com/posts", name="JSONPlaceholder /posts")