def predict_scale(workload):
    score = 0

    # Weighted scoring system
    score += workload.cpu * 0.4
    score += workload.memory * 0.3
    score += workload.latency * 0.2
    score += (workload.traffic / 10) * 0.1

    if score > 75:
        return "HIGH"
    elif score > 40:
        return "MEDIUM"
    else:
        return "LOW"