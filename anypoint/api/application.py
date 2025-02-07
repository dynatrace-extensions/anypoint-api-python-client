import logging
from collections.abc import Generator
from datetime import datetime
from typing import TYPE_CHECKING

from anypoint import utils
from anypoint.models.application import Application, ApplicationV2, ApplicationV2Details
from anypoint.models.stats import DashboardStatistics, Statistic

if TYPE_CHECKING:
    from anypoint import Anypoint


class ApplicationApi:
    def __init__(self, anypoint: "Anypoint", log: logging.Logger):
        self._client = anypoint
        self._log = log

    def get_application_statistics(
        self, environment_id: str, app_domain: str, date_from: datetime, date_to: datetime
    ) -> Generator[Statistic, None, None]:
        path = f"/cloudhub/api/applications/{app_domain}/statistics"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        params = {
            "start": f"{int(date_from.timestamp() * 1000)}",
            "end": f"{int(date_to.timestamp() * 1000)}",
            "intervalCount": f"{(date_to - date_from).total_seconds() // 60:0.0f}",
        }
        data = self._client.request(path, parameters=params, headers=headers)
        for timestamp, value in data.items():
            yield Statistic(timestamp, value)

    def get_dashboard_statistics(
        self, environment_id: str, app_domain: str, date_from: datetime, date_to: datetime
    ) -> DashboardStatistics:
        path = f"/cloudhub/api/v2/applications/{app_domain}/dashboardStats"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        params = {
            "startDate": utils.date_to_str(date_from),
            "endDate": utils.date_to_str(date_to),
            "interval": "60000",
        }
        data = self._client.request(path, parameters=params, headers=headers)
        return DashboardStatistics(data)

    def get_applications(self, environment_id: str) -> Generator[Application, None, None]:
        path = "/cloudhub/api/applications"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        data = self._client.request(path, headers=headers)
        for app in data:
            app["environment_id"] = environment_id
            yield Application(app, self)

    def get_applications_v2(self, org_id: str, environment_id: str) -> Generator[ApplicationV2, None, None]:
        path = (
            f"/amc/application-manager/api/v2/organizations/{org_id}/"
            f"environments/{environment_id}/deployments"
        )
        data = self._client.request(path)
        for app in data["items"]:
            app["environment_id"] = environment_id
            app["organization_id"] = org_id
            yield ApplicationV2(app, self)

    def get_application_v2(
        self, org_id: str, environment_id: str, deployment_id: str
    ) -> ApplicationV2Details:
        path = (
            f"/amc/application-manager/api/v2/organizations/{org_id}/"
            f"environments/{environment_id}/deployments/{deployment_id}"
        )
        data = self._client.request(path)
        data["environment_id"] = environment_id
        data["organization_id"] = org_id
        return ApplicationV2Details(data, self)

    def get_insights(self, environment_id: str, app_domain: str):
        path = f"/api/v2/applications/{app_domain}/insight"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        return self._client.request(path, headers=headers)

    def get_application_status(self, environment_id: str, app_domain: str):
        path = f"/cloudhub/api/applications/{app_domain}/status"
        headers = {"X-ANYPNT-ENV-ID": environment_id}
        response = self._client.request(path, headers=headers, return_json=False)
        return response.text
