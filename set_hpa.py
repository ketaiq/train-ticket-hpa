import csv
import os
import yaml
from yaml.loader import SafeLoader

template_file_name = "manifests/hpa-template.yaml"

with open("hpa_conf.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    header = next(csv_reader)
    ii = 0

    for row in csv_reader:
        service_name = str(row[0]).rstrip()

        cpu_value = int(row[2])
        memory_value = row[3]
        pods_min = int(row[4])
        pods_max = int(row[5])

        if pods_max <= 1:
            continue

        if pods_max <= 1:
            pods_max = 3

        ii += 1

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

            # print(
            #     os.system(
            #         "kubectl apply -f {file_name}".format(file_name=target_file_name)
            #     )
            # )
