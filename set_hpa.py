import csv
import os
import yaml
import pandas as pd
from yaml.loader import SafeLoader

template_file_name = "manifests/hpa-template.yaml"
df_hpa = pd.read_csv("hpa.csv")

for _, row in df_hpa.iterrows():
    service_name = row["Service"]
    cpu_value = int(row["CPU Threshold (%)"])
    memory_value = row["Memory Threshold (Mb)"]
    pods_min = int(row["PodsMin"])
    pods_max = int(row["PodsMax"])
    with open(template_file_name) as file_template:
        data = yaml.load(file_template, Loader=SafeLoader)

        data["metadata"]["name"] = service_name
        data["spec"]["scaleTargetRef"]["name"] = service_name
        data["spec"]["minReplicas"] = pods_min
        data["spec"]["maxReplicas"] = pods_max

        for jj in range(len(data["spec"]["metrics"])):
            metric_resource_name = data["spec"]["metrics"][jj]["resource"]["name"]

            if metric_resource_name == "cpu":
                data["spec"]["metrics"][jj]["resource"]["target"][
                    "averageUtilization"
                ] = cpu_value

            if metric_resource_name == "memory":
                data["spec"]["metrics"][jj]["resource"]["target"][
                    "averageValue"
                ] = memory_value

        target_file_name = "manifests/hpa-{service_name}.yaml".format(
            service_name=service_name
        )
        with open(target_file_name, "w") as file_target:
            yaml.dump(data, file_target, sort_keys=False, default_flow_style=False)

        os.system("kubectl apply -f {file_name}".format(file_name=target_file_name))
