import boto3
import csv

def get_critical_findings():
    # Initialize a Boto3 client for Security Hub
    client = boto3.client('securityhub')

    # Initialize an empty list to store the findings
    critical_findings = []

    # Get findings from Security Hub (this will include pagination for large result sets)
    paginator = client.get_paginator('get_findings')
    for page in paginator.paginate(
        Filters={
            'SeverityLabel': [
                {'Value': 'CRITICAL', 'Comparison': 'EQUALS'}
            ]
        }
    ):
        # Loop through the findings and append critical findings to the list
        for finding in page['Findings']:
            critical_findings.append({
                'Title': finding.get('Title', 'N/A'),
                'Description': finding.get('Description', 'N/A'),
                'Severity': finding.get('Severity', {}).get('Label', 'N/A'),
                'ResourceType': finding.get('Resources', [{}])[0].get('Type', 'N/A'),
                'ResourceId': finding.get('Resources', [{}])[0].get('Id', 'N/A'),
                'FindingArn': finding.get('AwsSecurityFindingArn', 'N/A'),
                'CreatedAt': finding.get('CreatedAt', 'N/A'),
                'UpdatedAt': finding.get('UpdatedAt', 'N/A'),
            })

    return critical_findings

def save_to_csv(findings, filename='critical_findings.csv'):
    # Define the header for the CSV
    header = ['Title', 'Description', 'Severity', 'ResourceType', 'ResourceId', 'FindingArn', 'CreatedAt', 'UpdatedAt']

    # Write the findings to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(findings)

def main():
    critical_findings = get_critical_findings()
    
    if critical_findings:
        print(f"Found {len(critical_findings)} critical findings.")
        save_to_csv(critical_findings)
        print("Critical findings have been saved to critical_findings.csv.")
    else:
        print("No critical findings found.")

if __name__ == '__main__':
    main()
