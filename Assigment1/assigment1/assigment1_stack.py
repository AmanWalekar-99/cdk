from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_codecommit as codecommit,

)
import aws_cdk as cdk
from constructs import Construct

class Assigment1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #creating S3 bucket 
        bucket = s3.Bucket(self, "MyFirstBucket1",
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True)

        # Creates an AWS CodeCommit repository
        code_repo = codecommit.Repository(
            self, "CodeRepo",
            repository_name="my-code-repo",
        )
        # Creates a VPC for the EC2 instance
        vpc = ec2.Vpc(
            self, "InstanceVpc",
            cidr="10.0.0.0/16"
        )

        # Creates a security group for the EC2 instance
        instance_sg = ec2.SecurityGroup(
            self, "InstanceSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True
        )
        # Allows inbound SSH access to the EC2 instance
        instance_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access",
            remote_rule=False
        )
        # Creates an EC2 instance
        instance = ec2.Instance(
            self, "AppInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            vpc=vpc,
            security_group=instance_sg,
        )

        # Create the EKS cluster
        cluster = eks.Cluster(
            self,
            "EKSCluster",
            cluster_name="my-eks-cluster",
            version=eks.KubernetesVersion.V1_19,
            default_capacity=2,
            vpc=vpc,
            vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)]
        )


