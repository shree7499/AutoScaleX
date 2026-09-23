# AutoScaleX

AutoScaleX is an intelligent cloud resource optimization system that dynamically selects the most cost-efficient infrastructure based on workload behavior and real-time cloud metrics.

The system monitors AWS EC2 instances using CloudWatch and automatically recommends deployment strategies such as Containers, Spot Instances, or On-Demand Instances.

---

## Features

- Real-time CPU monitoring using AWS CloudWatch
- Dynamic scaling prediction
- Intelligent infrastructure selection
- Spot instance failure simulation
- Cost estimation and savings analysis
- Resource allocation recommendations
- Flask-based monitoring dashboard

---

## Technologies Used

- Python
- Flask
- AWS EC2
- AWS CloudWatch
- HTML/CSS

---

## Project Structure

```text
AutoScaleX/
│
├── app.py
├── models/
├── utils/
├── templates/
├── static/
└── README.md