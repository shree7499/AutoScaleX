import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client(
    'cloudwatch',
    region_name='ap-south-1'
)

def get_cpu_metrics(instance_id):

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            }
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=10),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average']
    )

    datapoints = response['Datapoints']

    if datapoints:
        latest = sorted(
            datapoints,
            key=lambda x: x['Timestamp']
        )[-1]

        return round(latest['Average'])

    return 0