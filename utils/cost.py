def estimate_cost(infra, workload):

    if infra == "VM":
        return round(0.5 + (workload.cpu * 0.01), 2)
    else:
        return round(0.2 + (workload.cpu * 0.005), 2)