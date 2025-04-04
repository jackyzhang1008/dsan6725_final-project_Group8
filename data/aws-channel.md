# Channel AWS

## Thread: AWS Credit Issues
**Sarah_Johnson** [2025-03-15 10:23 AM]  
Hi everyone, I've run out of credits for my AWS account. Is anyone else having this issue?

**Prof_Martinez** [2025-03-15 10:30 AM]  
@Sarah_Johnson This happens sometimes at this point in the semester. I'll send you a DM with instructions on how to request additional credits through the education program.

**Sarah_Johnson** [2025-03-15 10:35 AM]  
@Prof_Martinez Thank you! I just applied for the additional credits.

**TA_Wong** [2025-03-15 11:05 AM]  
@Sarah_Johnson and others: Just a reminder to everyone to set up billing alerts in AWS so you get notified before running out of credits. Here's how: 1) Go to Billing Dashboard 2) Select "Budgets" 3) Create a budget with alert at 80% of your total credits.

**Sarah_Johnson** [2025-03-15 11:10 AM]  
@TA_Wong Thanks for the tip! Just set this up.

## Thread: SageMaker VPC Configuration Issues
**Alex_Chen** [2025-03-18 2:42 PM]  
I'm getting an error trying to set up SageMaker for our NYC TLC taxi data processing: "The security group 'sg-0123456789abcdef0' does not exist" when trying to create a notebook instance. Any ideas?

**TA_Patel** [2025-03-18 2:55 PM]  
@Alex_Chen Are you using the default VPC or did you create a custom one?

**Alex_Chen** [2025-03-18 3:01 PM]  
@TA_Patel I created a custom VPC following the lab guide, but something seems wrong with the security group references.

**TA_Patel** [2025-03-18 3:10 PM]  
@Alex_Chen I think I see the issue. The security group ID format in your error looks correct but it might be from a different region or account. Make sure you're in the same region where you created your security group. Can you share a screenshot of your VPC console?

**Alex_Chen** [2025-03-18 3:15 PM]  
@TA_Patel You're right! I was in us-east-1 but my security group was created in us-west-2. Switching regions fixed it. Thanks!

**TA_Patel** [2025-03-18 3:20 PM]  
@Alex_Chen Great! A common gotcha with AWS is resources are region-specific. Always check your region in the top-right corner.

## Thread: IAM Role for EC2 to S3
**Maya_Williams** [2025-03-20 9:17 AM]  
I'm trying to access the Amazon product reviews dataset from my EC2 instance, but keep getting "Access Denied" errors when trying to read the S3 bucket. Help!

**Jamie_Rodriguez** [2025-03-20 9:25 AM]  
@Maya_Williams Did you attach an IAM role to your EC2 instance?

**Maya_Williams** [2025-03-20 9:30 AM]  
@Jamie_Rodriguez Yes, I attached the "LabRole" that was mentioned in the instructions. Should I have created a custom one?

**Prof_Martinez** [2025-03-20 9:42 AM]  
@Maya_Williams The LabRole should have S3 read permissions, but let's check the specific policies. Can you run `aws iam list-attached-role-policies --role-name LabRole` from your instance and share what you see?

**Maya_Williams** [2025-03-20 9:50 AM]  
@Prof_Martinez I ran the command and don't see any S3 policies attached:
```
{
    "AttachedPolicies": [
        {
            "PolicyName": "AmazonEC2FullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
        }
    ]
}
```

**TA_Wong** [2025-03-20 10:01 AM]  
@Maya_Williams That's the issue! The LabRole should have had AmazonS3ReadOnlyAccess policy too. Let's attach it:

1. Go to IAM console
2. Click on "Roles" and find "LabRole"
3. Click "Attach policies"
4. Search for and attach "AmazonS3ReadOnlyAccess"

Then give it a few minutes and try again.

**Maya_Williams** [2025-03-20 10:15 AM]  
@TA_Wong That worked perfectly! I can now access the Amazon product reviews data from my EC2 instance. Thank you so much!

**TA_Wong** [2025-03-20 10:18 AM]  
@Maya_Williams Glad to hear it! This is a common issue when setting up AWS for big data projects. Always check your IAM permissions first when you get access denied errors.

## Thread: EMR Cluster for NYC TLC Data
**David_Kim** [2025-03-22 1:05 PM]  
Has anyone successfully set up an EMR cluster for processing the NYC TLC dataset? We're trying to analyze the 2023 yellow taxi data (~20GB) and I'm wondering what instance types work well without breaking the bank.

**Leila_Hassan** [2025-03-22 1:12 PM]  
@David_Kim I used a cluster with 1 m5.xlarge master and 2 m5.large core nodes. Worked well for the taxi data and cost about $3 in credits for a 4-hour analysis session.

**David_Kim** [2025-03-22 1:17 PM]  
@Leila_Hassan Thanks! Did you use Spark or Hive for your analysis?

**Leila_Hassan** [2025-03-22 1:25 PM]  
@David_Kim I used PySpark. Here's what my cluster config looked like:
```
aws emr create-cluster \
--name "TLC-Analysis" \
--release-label emr-6.10.0 \
--applications Name=Spark \
--ec2-attributes KeyName=my-key-pair \
--instance-type m5.xlarge \
--instance-count 3 \
--use-default-roles
```

**Prof_Martinez** [2025-03-22 1:40 PM]  
@David_Kim @Leila_Hassan Good discussion! For the NYC TLC dataset analysis, I recommend everyone also add spot instances to save on costs:
```
--instance-groups InstanceGroupType=MASTER,InstanceType=m5.xlarge,InstanceCount=1 InstanceGroupType=CORE,InstanceType=m5.large,InstanceCount=2,BidPrice=0.13
```
This can reduce costs by 70% compared to on-demand pricing!

**David_Kim** [2025-03-22 1:45 PM]  
@Prof_Martinez That's really helpful! Should we be concerned about spot instances terminating during our analysis?

**Prof_Martinez** [2025-03-22 1:50 PM]  
@David_Kim Good question. For these instance types, the spot market is quite stable. But yes, always implement checkpointing in your Spark code:
```python
spark.sparkContext.setCheckpointDir("s3://your-bucket/checkpoints/")
df.checkpoint()
```
This way, if an instance terminates, you won't lose all your work.

**David_Kim** [2025-03-22 1:55 PM]  
@Prof_Martinez Perfect, thank you! I'll set up my cluster today.

## Thread: SageMaker Memory Issues
**Tyler_Washington** [2025-03-25 11:20 AM]  
My SageMaker notebook keeps crashing when I try to load the full Amazon reviews dataset. The error says "MemoryError". I'm using the ml.t3.medium instance type. Any suggestions?

**TA_Patel** [2025-03-25 11:30 AM]  
@Tyler_Washington The ml.t3.medium only has 4GB of RAM, which isn't enough for the full Amazon reviews dataset. You have a few options:

1. Upgrade to ml.t3.large or ml.m5.xlarge
2. Use Dask or PySpark to process the data in chunks
3. Work with a subset of the data for development, then scale up

**Tyler_Washington** [2025-03-25 11:35 AM]  
@TA_Patel Thanks! How do I upgrade my instance type? Will I lose my work?

**TA_Patel** [2025-03-25 11:42 AM]  
@Tyler_Washington You'll need to:
1. Stop your current notebook instance
2. From the SageMaker console, select your notebook
3. Click "Actions" -> "Update settings"
4. Change the instance type
5. Start your instance again

You won't lose your work as long as you've saved your notebooks. All data in the /home/ec2-user/SageMaker directory persists between restarts and instance changes.

**Tyler_Washington** [2025-03-25 11:50 AM]  
@TA_Patel Perfect! Upgrading to ml.t3.large worked. I can now load the data.

**TA_Wong** [2025-03-25 11:55 AM]  
@Tyler_Washington @TA_Patel Just to add: for everyone working with the Amazon reviews data, consider using the SageMaker Data Wrangler feature to preprocess and sample the data. It's more efficient than loading everything into memory at once.

**Tyler_Washington** [2025-03-25 12:00 PM]  
@TA_Wong Thanks for the tip! I'll check that out.
