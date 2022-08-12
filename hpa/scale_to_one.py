from kubernetes import client, config
import os

config.load_kube_config()

# v1 = client.CoreV1Api()
# service_list = v1.list_namespaced_service(namespace="default")
# services = [item.metadata.name for item in service_list.items]
# services.remove("kubernetes")
# services.remove("rabbitmq")
# print("Services in the default namespace:\n", " - Number of services:", len(services), "\n  - Services:\n", services)

services = [("ts-auth-service", 80, 1, 10),
			("ts-inside-payment-service", 80, 1, 50),
			("ts-order-service", 80, 1, 50),
			("ts-preserve-service", 80, 1, 50),
			("ts-travel-service", 80, 1, 50),
			("ts-travel-plan-service", 80, 1, 10)]

print("Start scaling All containers to one replica .. ")
for service in services:
	service_name = service[0]
	print(os.system("kubectl scale --replicas=1 deployment/{service_name}".format(service_name=service_name)))

print("Done.")
print("HPA info:", os.system("kubectl get hpa"))
