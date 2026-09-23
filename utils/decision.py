def decide_infrastructure(workload, scale_level):

    if scale_level == "HIGH":
        if workload.latency > 200:
            return "VM"
        return "VM"

    elif scale_level == "MEDIUM":
        if workload.traffic > 800:
            return "CONTAINER"
        return "VM"

    else:
        return "CONTAINER"