import boto3
import os

asg = boto3.client("autoscaling")
rds = boto3.client("rds")

# Environment variables (set in Lambda Config)
ASG_NAME = os.environ["ASG_NAME"]
RDS_INSTANCE_ID = os.environ["RDS_INSTANCE_ID"]

START_DESIRED = int(os.getenv("START_DESIRED", "1"))
START_MIN = int(os.getenv("START_MIN", "1"))
START_MAX = int(os.getenv("START_MAX", "2"))

def lambda_handler(event, context):
    action = event.get("action", "").upper()

    if action not in ["START", "STOP"]:
        return {"error": "Invalid action. Use START or STOP."}

    result = {"action": action, "done": []}

    # ---- RDS Start/Stop ----
    if action == "START":
        rds.start_db_instance(DBInstanceIdentifier=RDS_INSTANCE_ID)
        result["done"].append({"rds": f"starting {RDS_INSTANCE_ID}"})
    else:
        rds.stop_db_instance(DBInstanceIdentifier=RDS_INSTANCE_ID)
        result["done"].append({"rds": f"stopping {RDS_INSTANCE_ID}"})

    # ---- ASG Scale Up/Down ----
    if action == "START":
        asg.update_auto_scaling_group(
            AutoScalingGroupName=ASG_NAME,
            MinSize=START_MIN,
            MaxSize=START_MAX,
            DesiredCapacity=START_DESIRED
        )
        result["done"].append({"asg": f"scaled UP {ASG_NAME} desired={START_DESIRED}"})
    else:
        asg.update_auto_scaling_group(
            AutoScalingGroupName=ASG_NAME,
            MinSize=0,
            MaxSize=0,
            DesiredCapacity=0
        )
        result["done"].append({"asg": f"scaled DOWN {ASG_NAME} desired=0"})

    return result
