from flask import Flask, render_template, request
from models.workload import Workload
from utils.predictor import predict_scale
from utils.decision import decide_infrastructure
from utils.cost import estimate_cost
from utils.allocator import allocate_resource
from utils.cloudwatch_monitor import get_cpu_metrics
import random

app = Flask(__name__)

# ---------------- INSTANCE SELECTION ----------------

def select_instance(workload_type, infra, cpu):
    if infra == "CONTAINER":
        return "Docker Container"

    if workload_type == "ml":
        return "g4dn.xlarge (GPU)"

    elif workload_type == "realtime":
        return "c5.large"

    elif workload_type == "batch":
        if cpu < 40:
            return "t3.micro"
        elif cpu < 70:
            return "t3.medium"
        else:
            return "m5.large"

    return "t2.medium"

# ---------------- SPOT FAILURE ----------------

def simulate_spot_failure(fault_tolerance):
    failure_chance = {
        "low": 0.3,
        "medium": 0.1,
        "high": 0.0
    }

    return random.random() < failure_chance.get(fault_tolerance, 0.1)

# ---------------- SAVINGS ----------------

def compute_savings(infra, workload_type, scale):
    base = {
        "CONTAINER": 35,
        "SPOT": 60,
        "SERVERLESS": 20,
        "ON_DEMAND": 0
    }

    savings = base.get(infra, 10)

    if scale == "HIGH" and infra == "CONTAINER":
        savings = max(savings - 10, 0)

    return savings

# ---------------- HUMAN READABLE REASON ----------------

def human_readable_reason(workload_type, infra, scale, instance, fault):
    scale_desc = {
        "LOW": "low",
        "MEDIUM": "moderate",
        "HIGH": "high"
    }.get(scale, scale.lower())

    infra_desc = {
        "CONTAINER": "containerised deployment",
        "SPOT": "spot instances",
        "ON_DEMAND": "on-demand instances",
    }.get(infra, infra)

    wl_desc = {
        "ml": "ML/AI",
        "realtime": "realtime",
        "batch": "batch"
    }.get(workload_type, workload_type)

    return (
        f"{wl_desc} workload detected with {scale_desc} demand. "
        f"AutoScaleX selected {infra_desc} using {instance} "
        f"based on cloud telemetry, cost optimization, and "
        f"{fault} fault tolerance."
    )

# ---------------- ROUTE ----------------

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    timeline = []

    if request.method == "POST":
        try:           
            instance_id = request.form["instance_id"]

            cpu = float(get_cpu_metrics(instance_id))
            cpu = round(cpu,2)
            
            if cpu < 1:
                cpu = random.randint(15,40)

            duration = max(
                1,
                int(request.form["duration"])
            )

        except (ValueError, KeyError):
            return render_template(
                "index.html",
                result=None,
                timeline=[],
                error="Invalid input."
            )

        workload_type = request.form.get(
            "resource_type",
            "web"
        )

        fault = request.form.get(
            "fault_tolerance",
            "medium"
        )

        # ---------------- WORKLOAD MODEL ----------------
        if workload_type == "ml":
            workload = Workload(
                cpu=cpu,
                memory=cpu + 20,
                latency=200,
                traffic=cpu * 5
            )

        elif workload_type == "realtime":
            workload = Workload(
                cpu=cpu,
                memory=cpu,
                latency=50,
                traffic=cpu * 15
            )

        else:
            workload = Workload(
                cpu=cpu,
                memory=max(cpu - 10, 10),
                latency=300,
                traffic=cpu * 8
            )

        # ---------------- TIMELINE ----------------
        simulated_loads = [
            cpu // 2,
            cpu,
            min(cpu + 20, 100)
        ]

        stage_labels = [
            "Ramp-up",
            "Peak",
            "Cooldown"
        ]

        for label, c in zip(stage_labels, simulated_loads):
            temp_workload = Workload(
                cpu=c,
                memory=c,
                latency=100,
                traffic=c * 10
            )

            scale = predict_scale(temp_workload)

            infra = decide_infrastructure(
                temp_workload,
                scale
            )

            if infra == "VM":
                infra = (
                    "SPOT"
                    if fault != "high"
                    else "ON_DEMAND"
                )

            timeline.append({
                "stage": label,
                "cpu": c,
                "scale": scale,
                "infra": infra
            })

        # ---------------- FINAL DECISION ----------------
        scale = predict_scale(workload)

        infra = decide_infrastructure(
            workload,
            scale
        )

        if infra == "VM":
            infra = (
                "SPOT"
                if fault != "high"
                else "ON_DEMAND"
            )

        instance = select_instance(
            workload_type,
            infra,
            cpu
        )

        cost = estimate_cost(
            infra,
            workload
        )

        savings = compute_savings(
            infra,
            workload_type,
            scale
        )

        # ---------------- FAILURE HANDLING ----------------
        failed = (
            infra == "SPOT"
            and simulate_spot_failure(fault)
        )

        if failed:
            infra = "ON_DEMAND"

            instance = select_instance(
                workload_type,
                infra,
                cpu
            )

            cost = estimate_cost(
                infra,
                workload
            )

            savings = 0

        # ---------------- RESOURCE ALLOCATION ----------------
        allocation = allocate_resource(
            infra,
            instance
        )

        reason = human_readable_reason(
            workload_type,
            infra,
            scale,
            instance,
            fault
        )

        # ---------------- RESULT ----------------
        result = {
            "cpu": cpu,
            "strategy": infra,
            "instance": instance,
            "cost": round(cost, 2),
            "savings": savings,
            "failed": failed,
            "allocation": allocation,
            "reason": reason
        }

    return render_template(
        "index.html",
        result=result,
        timeline=timeline
    )

if __name__ == "__main__":
    app.run(debug=True)