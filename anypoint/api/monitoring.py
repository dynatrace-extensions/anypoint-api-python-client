import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anypoint import Anypoint


class MonitoringApi:
    def __init__(self, client: "Anypoint", log: logging.Logger):
        self._client = client
        self._log = log
        self._proxy_influx_db: str = ""
        self._influx_db: str = ""

    def sync(self):
        path = "/monitoring/api/sync"
        data = self._client.request(path)
        for p in data.get("proxies", []):
            if p["name"] == "influxdb":
                self._proxy_influx_db = p["id"]
            elif p["name"] == "influx_analytics":
                self._proxy_influx_analytics = p["id"]

    def authorize(self, org_id: str):
        path = "/accounts/api/authorize"
        data = {
            "namespace": "monitoringcenter",
            "action": "GET",
            "resources": [f"/organizations/{org_id}/admin", f"/organizations/{org_id}/viewer"],
        }
        return self._client.request(path, method="POST", body=data)

    def boot_data(self):
        path = "/monitoring/api/visualizer/api/bootdata"
        data = self._client.request(path)
        influx_data = data.get("Settings", {}).get("datasources", {}).get("influxdb", {})
        if influx_data:
            self._influx_db = influx_data["database"]
            self._proxy_influx_db = influx_data["id"]

    def get_applications(self, environment_id: str):
        # /monitoring/api/visualizer/environments/c22c6dfd-0257-42a5-b64e-6037910935e8/applications
        path = f"/monitoring/api/visualizer/environments/{environment_id}/applications"
        return self._client.request(path)

    def query(self, query_string: str) -> dict:
        if not self._proxy_influx_db:
            self.boot_data()
        path = f"/monitoring/api/visualizer/api/datasources/proxy/{self._proxy_influx_db}/query"
        return self._client.request(
            path, parameters={"db": self._influx_db, "q": query_string, "epoch": "ms"}
        )
