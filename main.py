from utils.monitor import generate_workload
from utils.predictor import predict_scale
from utils.decision import decide_infrastructure
from utils.cost import estimate_cost

workload = generate_workload()

scale = predict_scale(workload)

infra = decide_infrastructure(workload, scale)

cost = estimate_cost(infra, workload)

print(workload)
print("Scale Level:", scale)
print("Chosen Infra:", infra)
print("Estimated Cost:", cost)