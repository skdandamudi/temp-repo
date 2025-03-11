import boto3
import csv

# Initialize SecurityHub client
client = boto3.client('securityhub')

# Define severity levels to filter by
SEVERITY_FILTER = ['CRITICAL', 'MEDIUM']

def get_findings():
    findings = []
    # Paginate through Security Hub findings
    paginator = client.get_paginator('get_findings')
    for page in paginator.paginate():
        findings.extend(page['Findings'])
    
    return findings

def filter_findings_by_severity(findings, severities):
    filtered_findings = []
    for finding in findings:
        severity = finding.get('Severity', {}).get('Label', '')
        if severity in severities:
            filtered_findings.append(finding)
    return filtered_findings

def export_to_csv(filtered_findings, filename='security_hub_findings.csv'):
    keys = filtered_findings[0].keys() if filtered_findings else []
    
    # Write the findings to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for finding in filtered_findings:
            writer.writerow(finding)

def main():
    # Get all findings from Security Hub
    findings = get_findings()

    # Filter findings by critical and medium severity
    filtered_findings = filter_findings_by_severity(findings, SEVERITY_FILTER)

    # Export filtered findings to CSV
    if filtered_findings:
        export_to_csv(filtered_findings)
        print(f"Exported {len(filtered_findings)} findings to security_hub_findings.csv")
    else:
        print("No findings found with specified severity levels.")

if __name__ == '__main__':
    main()
