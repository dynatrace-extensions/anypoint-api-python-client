from datetime import datetime


class Statistic:
    def __init__(self, timestamp: str, value: int):
        self.timestamp: datetime = datetime.fromtimestamp(int(timestamp) / 1000)
        self.value: int = value

    def __repr__(self):
        return f"Statistic({self.timestamp}, {self.value})"


class DashboardStatistics:
    def __init__(self, data: dict):
        self.events: list[Statistic] = []
        for timestamp, value in data.get("events").items():
            self.events.append(Statistic(timestamp, value))

        self.workers: list[Worker] = []
        for worker in data.get("workerStatistics"):
            self.workers.append(Worker(worker))

        self._data = data

    def __repr__(self):
        return f"DashboardStatistics({self._data})"


class WorkerMetric:
    def __init__(self, metric_id: str, datapoints: dict | float | int):
        self.metric_id: str = metric_id
        self.statistics: list[Statistic] = []

        if not isinstance(datapoints, dict):
            datapoints = {f"{int(datetime.now().timestamp() * 1000)}": datapoints}
        for timestamp, value in datapoints.items():
            self.statistics.append(Statistic(timestamp, value))


class Worker:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.metrics: list[WorkerMetric] = []
        for metric_id, datapoints in data.get("statistics", {}).items():
            self.metrics.append(WorkerMetric(metric_id, datapoints))
