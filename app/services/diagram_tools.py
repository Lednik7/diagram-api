# Available diagram tools for the agent
DIAGRAM_TOOLS = {
    # AWS Compute
    "aws.compute.EC2": "EC2 Instance",
    "aws.compute.ECS": "ECS Container Service", 
    "aws.compute.EKS": "EKS Kubernetes",
    "aws.compute.Lambda": "Lambda Function",
    "aws.compute.Lightsail": "Lightsail VPS",
    
    # AWS Network
    "aws.network.ALB": "Application Load Balancer",
    "aws.network.ELB": "Elastic Load Balancer",
    "aws.network.NLB": "Network Load Balancer",
    "aws.network.VPC": "Virtual Private Cloud",
    "aws.network.CloudFront": "CloudFront CDN",
    "aws.network.Route53": "Route53 DNS",
    "aws.network.APIGateway": "API Gateway",
    
    # AWS Database
    "aws.database.RDS": "RDS Database",
    "aws.database.DynamoDB": "DynamoDB NoSQL",
    "aws.database.ElastiCache": "ElastiCache",
    "aws.database.Redshift": "Redshift Data Warehouse",
    
    # AWS Storage
    "aws.storage.S3": "S3 Bucket",
    "aws.storage.EBS": "EBS Volume",
    "aws.storage.EFS": "EFS File System",
    
    # AWS Integration
    "aws.integration.SQS": "SQS Queue",
    "aws.integration.SNS": "SNS Notifications",
    "aws.integration.SES": "SES Email Service",
    
    # AWS Security
    "aws.security.IAM": "IAM Identity Management",
    "aws.security.Cognito": "Cognito User Pool",
    
    # AWS Management
    "aws.management.Cloudwatch": "CloudWatch Monitoring",
    "aws.management.Cloudtrail": "CloudTrail Audit",
    
    # GCP Compute
    "gcp.compute.ComputeEngine": "Compute Engine VM",
    "gcp.compute.GKE": "Google Kubernetes Engine",
    "gcp.compute.Functions": "Cloud Functions",
    
    # GCP Network
    "gcp.network.LoadBalancing": "Load Balancer",
    "gcp.network.CDN": "Cloud CDN",
    "gcp.network.DNS": "Cloud DNS",
    
    # GCP Database  
    "gcp.database.SQL": "Cloud SQL",
    "gcp.database.Firestore": "Firestore NoSQL",
    "gcp.database.BigQuery": "BigQuery Data Warehouse",
    
    # GCP Storage
    "gcp.storage.GCS": "Cloud Storage",
    
    # Azure Compute
    "azure.compute.VirtualMachines": "Virtual Machine",
    "azure.compute.AKS": "Azure Kubernetes Service",
    "azure.compute.FunctionApps": "Function Apps",
    
    # Azure Network
    "azure.network.LoadBalancer": "Load Balancer",
    "azure.network.ApplicationGateway": "Application Gateway",
    "azure.network.CDN": "Azure CDN",
    
    # Azure Database
    "azure.database.SQLDatabases": "SQL Database",
    "azure.database.CosmosDB": "Cosmos DB",
    
    # Azure Storage
    "azure.storage.BlobStorage": "Blob Storage"
}

def get_available_tools():
    """Get all available diagram tools"""
    return DIAGRAM_TOOLS