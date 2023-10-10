# Azure-AKS-Clusters-Recommendations-Extractor

## Overview

The Azure-AKS-Clusters-Recommendations-Extractor is a powerful tool designed to streamline the process of extracting recommendation data from Azure AKS (Azure Kubernetes Service) clusters. Azure AKS provides valuable insights and recommendations related to the security and health of your Kubernetes clusters. However, accessing and organizing this data can be challenging, especially when dealing with multiple clusters and subscriptions. This tool simplifies the process of monitoring and managing the security and compliance of your AKS clusters by providing insights into their health and adherence to Azure policies.

## Features

- **Data Extraction**: Retrieve data on AKS clusters, subscriptions, and Azure policy recommendations from your Azure environment.

- **Recommendation Tracking**: Keep track of Azure pod recommendations for each AKS cluster, including their health status (Healthy/Unhealthy/N/A).

- **CSV Export**: Export the extracted data to a CSV file for further analysis and reporting.

- **Flexibility**: Filter and display information for specific clusters, subscriptions, or policy states, making it easy to focus on areas that require attention.

- **Visibility**: Automatically handle naming conflicts and provide clear recommendations status (Healthy/Unhealthy/N/A) for each cluster.

## Prerequisites

Before using the Azure AKS Clusters Recommendations Extractor, ensure you have the following prerequisites:

- **Azure CLI**: You need to have the Azure CLI installed and authenticated to interact with your Azure environment.

- **Python Libraries**: The script uses Python libraries such as `termcolor` and `argparse`. You can install these libraries using pip.

## Usage

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the tool's directory.

3. Run the script using Python, specifying the desired options for cluster, subscription, and policy.

   ```
   python clusters_parser.py -c <cluster_name> -s <subscription_name> -p <policy_state>
   ```
   
   - Use `-c` or `--cluster`: Specify the name of the cluster to extract (use `*` for all clusters).
   - Use `-s` or `--subscription`: Filter clusters by subscription (use `*` for all subscriptions).
   - Use `-p` or `--policy`: Filter clusters by Azure Policy add-on state (Healthy/Unhealthy/N/A) (use `*` for all states).

4. The tool will generate a CSV file containing the extracted data.

### Examples

Extract recommendations data for a specific cluster:

```bash
python clusters_parser.py -c _YourClusterName_
```

Extract recommendations data for clusters within a specific subscription:

```bash
python clusters_parser.py -s _YourSubscriptionName_
```

Extract recommendations data for clusters with a specific Azure Policy add-on state (Healthy/Unhealthy/N/A):

```bash
python clusters_parser.py -p _Healthy_
```

Extract recommendations data for all clusters:

```bash
python clusters_parser.py -c "*" -s "*" -p "*"
```

## Output - Exported Data

The tool generates a CSV file named with a timestamp, containing the following information:

- Cluster name
- Subscription
- Resource Group
- Azure AKS recommendations (with status: Healthy, Unhealthy, or N/A)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This tool is created with ❤️ by Aviv Beniash.
