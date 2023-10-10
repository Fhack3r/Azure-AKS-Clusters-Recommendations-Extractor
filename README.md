# Azure-AKS-Pod-Recommendations-Extractor

## Overview

The Azure AKS Pod Recommendations Extractor is a Python script designed to help you extract and manage recommendations for Azure Kubernetes Service (AKS) clusters. It interacts with the Azure CLI to gather data on AKS clusters, subscriptions, and their associated Azure policy recommendations. This tool simplifies the process of monitoring and managing the security and compliance of your AKS clusters by providing insights into their health and adherence to Azure policies.

## Features

- **Data Extraction**: Retrieve information on AKS clusters, subscriptions, and Azure policy recommendations from your Azure environment.

- **Recommendation Tracking**: Keep track of Azure policy recommendations for each AKS cluster, including their health status (Healthy/Unhealthy).

- **CSV Export**: Export the extracted data to a CSV file for further analysis and reporting.

- **Flexibility**: Filter and display information for specific clusters, subscriptions, or policy states, making it easy to focus on areas that require attention.

## Prerequisites

Before using the Azure AKS Pod Recommendations Extractor, ensure you have the following prerequisites:

- **Azure CLI**: You need to have the Azure CLI installed and authenticated to interact with your Azure environment.

- **Python Libraries**: The script uses Python libraries such as `termcolor` and `argparse`. You can install these libraries using pip.

## Usage

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the tool's directory.

3. Run the script using Python, specifying the desired options for cluster, subscription, and policy.

   ```
   python clusters_parser.py -c <cluster_name> -s <subscription_name> -p <policy_state>
   ```

   - Use `-c` to specify a particular cluster or use `*` to select all clusters.
   - Use `-s` to specify a particular subscription or use `*` to select all subscriptions.
   - Use `-p` to filter by Azure policy state (Healthy/Unhealthy) or use `*` to include all policies.

4. The tool will generate a CSV file containing the extracted data.

## Example

To extract data for a specific cluster named "MyCluster," use the following command:

```
python clusters_parser.py -c MyCluster
```

## Exported Data

The tool exports data to a CSV file containing the following columns:

- Cluster
- Subscription
- Resource Group
- (Azure policy recommendations)

## License

This tool is provided under the [MIT License](LICENSE) and is free to use, modify, and distribute.

## Disclaimer

This tool is not an official Microsoft product. Use it responsibly and ensure that you have the necessary permissions and approvals to access and modify Azure resources.
