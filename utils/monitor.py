import random
from models.workload import Workload

def generate_workload():
    cpu = random.randint(10, 95)
    memory = random.randint(20, 90)
    latency = random.randint(50, 500)
    traffic = random.randint(100, 2000)

    return Workload(cpu, memory, latency, traffic)