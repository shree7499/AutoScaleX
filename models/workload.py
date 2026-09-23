class Workload:
    def __init__(self, cpu, memory, latency, traffic):
        self.cpu = cpu              # % CPU usage
        self.memory = memory        # % Memory usage
        self.latency = latency      # ms
        self.traffic = traffic      # requests/sec

    def __repr__(self):
        return f"Workload(cpu={self.cpu}, memory={self.memory}, latency={self.latency}, traffic={self.traffic})"