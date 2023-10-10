from termcolor import colored
from datetime import datetime
import json
import os
import re
import argparse
import csv


def dict_to_str(dictionary):
    return str(dictionary).replace("{'", "").replace("': '", ": ").replace("': ", ": ").replace("', '", "\n") \
        .replace(" Subscription", "\nSubscription").replace("'}, '", "\n""\n").replace("'}}", "").replace("'}", "") \
        .replace("Healthy", colored('Healthy', 'green')).replace("Unhealthy", colored('Unhealthy', 'red'))


def all_clusters():
    command = f'''az graph query -q "resources
        | where type == 'microsoft.containerservice/managedclusters'
        | extend clusterName = tostring(name)" --first 1000'''
    return json.loads(os.popen(command).read())['data']


def list_of_subscription():
    command = f'''az graph query -q "ResourceContainers
        | where type == 'microsoft.resources/subscriptions'" --first 1000'''
    return json.loads(os.popen(command).read())['data']


def list_of_clusters(assessmentkey):
    command = f'''az graph query -q "SecurityResources
        | where type == 'microsoft.security/assessments'
        | extend assessmentKey = tostring(name),
          recommendationName = tostring(properties.displayName),
          recommendationState = tostring(properties.status.code)
        | where assessmentKey == '{assessmentkey}'" --first 1000'''
    return json.loads(os.popen(command).read())['data']


### Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cluster", dest="cluster", default="*", help="Cluster name to extract")
parser.add_argument("-s", "--subscription", dest="subscription", default="*", help="Clusters to extract by a subscription")
parser.add_argument("-p", "--policy", dest="policy", default="*", help="Clusters to extract by Azure policy add-on state (Healthy/Unhealthy)")
args = parser.parse_args()

### Variables
recommendations = {
    "08e628db-e2ed-4793-bc91-d13e684401c3": "Azure Kubernetes Service clusters should have the Azure Policy add-on for Kubernetes installed",
    "b0fdc63a-38e7-4bab-a7c4-2c2665abbaa9": "Role-Based Access Control should be used on Kubernetes Services",
    # "5d90913f-a1c5-4429-ad54-2c6c17fb3c73": "Privileged containers should be avoided",
    # "11c95609-3553-430d-b788-fd41cde8b2db": "Least privileged Linux capabilities should be enforced for containers",
    # "27d6f0e9-b4d5-468b-ae7e-03d5473fd864": "Immutable (read-only) root filesystem should be enforced for containers",
    # "f0debc84-981c-4a0d-924d-aa4bd7d55fef": "Usage of pod HostPath volume mounts should be restricted to a known list to restrict node access from compromised containers",
    # "802c0637-5a8c-4c98-abd7-7c96d89d6010": "Containers sharing sensitive host namespaces should be avoided",
    "86f91051-9d6a-47c3-a07f-bd14cb214b45": "Containers should only use allowed AppArmor profiles",
    "1accfd14-1fbb-1b54-5109-916392065538": "Kubernetes cluster containers should not use forbidden sysctl interfaces",
    "b851f49c-7c24-2095-3481-8c2fb48717bd": "Kubernetes cluster containers should only use allowed seccomp profiles",
    "4506de73-e000-54c1-471d-f23903b5a324": "Kubernetes cluster pods and containers should only use allowed SELinux options",
    "802c0637-5a8c-4c98-abd7-7c96d89d6010": "Containers sharing sensitive host namespaces should be avoided",
    "11c95609-3553-430d-b788-fd41cde8b2db": "Least privileged Linux capabilities should be enforced for containers",
    "5d90913f-a1c5-4429-ad54-2c6c17fb3c73": "Privileged containers should be avoided",
    "ebc68898-5c0f-4353-a426-4a5f1e737b12": "Usage of host networking and ports should be restricted",
    "f0debc84-981c-4a0d-924d-aa4bd7d55fef": "Usage of pod HostPath volume mounts should be restricted to a known list to restrict node access from compromised containers",
    "9b795646-9130-41a4-90b7-df9eae2437c8": "Running containers as root user should be avoided",
    "8b227c88-adb6-3873-b7c9-25aedcf2bcf7": "Kubernetes cluster pods should only use allowed volume types",
    "43dc2a2e-ce69-4d42-923e-ab7d136f2cfe": "Container with privilege escalation should be avoided",
}

subExclusion = [""]
cluster_pattern = "managedclusters/(.*)/providers"
subscription_pattern_in_subscriptions = "/subscriptions/(.*)"
subscription_pattern_in_clusters = "subscriptions/(.*)/resourceGroups"
resource_group_pattern = "resourcegroups/(.*)/providers/microsoft.containerservice/"
subscription_dict = {}
cluster_dict = {}
subCounter = 0
cluCounter = 0
healthyCounter = 0
unhealthyCounter = 0
repeatedCounter = 0
naCounter = 0

### Subscriptions
for subscription in list_of_subscription():
    subscriptionId = subscription["subscriptionId"]
    subscriptionName = subscription["name"]
    subCounter += 1
    print(subCounter, subscriptionId)

    if len(subscription_dict) == 0:
        subscription_dict.update({subscriptionId: []})
    subscription_dict[subscriptionId] = subscriptionName


### Adding cluster, subscription and resource group names.
for cluster in all_clusters():
    clusterName = cluster["name"]
    subscription = subscription_dict[(re.search(subscription_pattern_in_clusters, cluster["id"]).group(1))]
    if subscription in subExclusion:
        continue
    resource_group = cluster["resourceGroup"]

    if clusterName in cluster_dict.keys():
        clusterName = clusterName + "_MANUEL_CHECK_IS_REQUIRED_" + str(cluCounter)
        repeatedCounter += 1

    cluster_dict.update({clusterName: {}})
    cluster_dict[clusterName]['Subscription'] = subscription
    cluster_dict[clusterName]['Resource Group'] = resource_group
    cluCounter += 1
    print(cluCounter, clusterName)
cluster_dict = {k.lower(): v for k, v in cluster_dict.items()}


### Adding recommendation name and state for each cluster.
for key in recommendations:
    for cluster in list_of_clusters(key):
        clusterName = (re.search(cluster_pattern, cluster["id"]).group(1))
        rec_name = cluster["recommendationName"]
        rec_state = cluster["recommendationState"]
        if rec_state == "Healthy":
            healthyCounter += 1
        else:
            unhealthyCounter += 1
        cluster_dict[clusterName][rec_name] = rec_state
cluster_dict = dict(sorted(cluster_dict.items()))


### Adding N/A status for clusters without the relevant recommendation.
for cluster_key in cluster_dict:
    for rec_key in recommendations:
        clusterData = cluster_dict[cluster_key]
        if recommendations[rec_key] not in clusterData:
            cluster_dict[cluster_key][recommendations[rec_key]] = "N/A"
            naCounter += 1


# Print results to console
if args.cluster == "*" and args.subscription == "*" and args.policy == "*":
    print(dict_to_str(cluster_dict))
elif args.cluster != "*":
    print(colored(args.cluster, 'yellow'), "\n", dict_to_str(cluster_dict[args.cluster]), "\n")
elif args.subscription != "*":
    for key in cluster_dict:
        if cluster_dict[key]["Subscription"] == args.subscription:
            print(colored(key, 'yellow'), "\n", dict_to_str(cluster_dict[key]), "\n")
elif args.policy != "*":
    for key in cluster_dict:
        if cluster_dict[key][
            "Azure Kubernetes Service clusters should have the Azure Policy add-on for Kubernetes installed"] == args.policy:
            print(colored(key, 'yellow'), "\n", dict_to_str(cluster_dict[key]), "\n")
print()
print("Number of recommendations:", len(recommendations))
print("Number of Subscriptions:", subCounter)
print("Number of Clusters:", cluCounter)
print("Number of repeated clusters with the same name:", repeatedCounter)
print("Number of Healthy recommendations:", healthyCounter)
print("Number of Unhealthy recommendations:", unhealthyCounter)
print("Number of N/A recommendations:", naCounter)


### Export to EXCEL
csv_file = open('data.csv', 'w')
csv_writer = csv.writer(csv_file)
columns = ['Cluster',
           'Subscription',
           'Resource Group'
        ]
for key in recommendations:
    columns.append(recommendations[key])
csv_writer.writerow(columns)

for key in cluster_dict:
    rowToCSV = list()
    rowToCSV.append(key)
    for value in range(1, len(cluster_dict[key]) + 1):
        rowToCSV.append(cluster_dict[key][columns[value]])
    csv_writer.writerow(rowToCSV)
csv_file.close()

date = datetime.now().strftime("%Y:%m:%d-%I.%M.%S%p")
new_file_name = date + ' | Recs-' + str(len(recommendations)) + ' | Subs-' + str(subCounter) + ' | Clusters-' + str(cluCounter) + ' | Healthy-' + str(healthyCounter) + ' | Unhealthy-' + str(unhealthyCounter) + ' | NA-' + str(naCounter) + ' |.csv'
os.rename('data.csv', new_file_name)
