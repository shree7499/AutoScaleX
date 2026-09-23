def allocate_resource(infra, instance):
    
    if infra == "VM":
        return f"EC2 instance {instance} allocated"

    elif infra == "CONTAINER":
        return f"Container deployed on cluster"

    return "No allocation"