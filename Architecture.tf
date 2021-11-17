/*
Overview:

Terraform code to create a Inventory Management system

Creates:
    - In UK region
    - VPC (ApplicationVPC)
    - Public and private subnets

To Dos:

*/

/*--------------------------------------------------------------------------
                Defines provider and region
--------------------------------------------------------------------------*/
provider "aws" {
 region = "eu-west-2"
}
/*--------------------------------------------------------------------------
                Defines VPC, cidr blocks and subnets 
--------------------------------------------------------------------------*/
resource "aws_vpc" "ApplicationVPC" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "PublicSubnet" {
  vpc_id     = aws_vpc.ApplicationVPC.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_subnet" "PrivateSubnet" {
  vpc_id     = aws_vpc.ApplicationVPC.id
  cidr_block = "10.0.2.0/24"
}

/*--------------------------------------------------------------------------
                Defines security group for ALB 
--------------------------------------------------------------------------*/
resource "aws_security_group" "sg_ALB" {
  name        = "sg_ALB"
  description = "Allow HTTP/S inbound traffic"
  vpc_id      = aws_vpc.ApplicationVPC.id

  ingress {
    description      = "HTTPS from Anywhere"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    description      = "SSH from Anywhere"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    description      = "HTTP from Anywhere"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
    ingress {
    description      = "HTTP from Anywhere"
    from_port        = 5000
    to_port          = 5000
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

/*--------------------------------------------------------------------------
                Defines security group for EC2 Instance 
--------------------------------------------------------------------------*/
resource "aws_security_group" "sg_ec2" {
  name        = "sg_ec2"
  description = "Allow HTTP/S inbound traffic"
  vpc_id      = aws_vpc.ApplicationVPC.id

  ingress {
    description      = "HTTPS from Anywhere"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    description      = "SSH from Anywhere"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  ingress {
    description      = "HTTP from Anywhere"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
    ingress {
    description      = "HTTP from Anywhere"
    from_port        = 5000
    to_port          = 5000
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

/*--------------------------------------------------------------------------
                Defines internet gateway for vpc 
--------------------------------------------------------------------------*/
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.ApplicationVPC.id

  tags = {
    Name = "main"
  }
}


/*--------------------------------------------------------------------------
                         Defines ALB 
--------------------------------------------------------------------------*/
resource "aws_lb" "AppALBtoEC2" {
    name               = "ALBtoEC2"
    internal           = false
    load_balancer_type = "application"
    subnets            = [aws_subnet.PublicSubnet.id]
    security_groups    = [aws_security_group.sg_ALB.id]

}


/*--------------------------------------------------------------------------
              Creates the bucket for Wesite code and templates 
--------------------------------------------------------------------------*/
/*

resource "aws_s3_bucket" "template-bucket" {
    bucket = "template-bucket-5623"
    acl = "private"
    force_destroy = true

 versioning {
    enabled = true
 }
}
*/

/*
/*--------------------------------------------------------------------------
  Defines DynamoDB tables for user information and inventory information 
--------------------------------------------------------------------------*/
resource "aws_dynamodb_table" "UserDatabaseDynamoDB" {
  name           = "UserDatabase"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "InventoryDatabaseDynamoDB" {
  name           = "InventoryDatabase"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "prod_ID"

  attribute {
    name = "prod_ID"
    type = "S"
  }
}
*/


/*--------------------------------------------------------------------------
      IAM roles for ec2 to grab content from s3 
--------------------------------------------------------------------------*/
resource "aws_iam_role" "web_iam_role" {
    name = "web_iam_role"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "web_instance_profile" {
    name = "web_instance_profile"
    role = "${aws_iam_role.web_iam_role.id}"
}

resource "aws_iam_role_policy" "web_iam_role_policy" {
  name = "web_iam_role_policy"
  role = "${aws_iam_role.web_iam_role.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::template-bucket-5623"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": ["arn:aws:s3:::template-bucket-5623/*"]
    }
  ]
}
EOF
}



/*--------------------------------------------------------------------------
          Defines ec2 instance for program to run
--------------------------------------------------------------------------*/
resource "aws_instance" "WebsiteEC2" {
  ami           = "ami-0fc15d50d39e4503c"
  instance_type = "t2.micro"
  subnet_id = aws_subnet.PrivateSubnet.id
  user_data = "${file("user-data-website.sh")}"
  key_name = "testKeyPair"
  iam_instance_profile = "${aws_iam_instance_profile.web_instance_profile.id}"
  security_groups = ["${aws_security_group.sg_ec2.id}"]
}

// Defines secret manager
resource "aws_secretsmanager_secret" "Secrets" {
  name = "SuperSecret"
}

resource "aws_secretsmanager_secret_version" "DynamoDBSecrets" {
  secret_id     = aws_secretsmanager_secret.Secrets.id
  secret_string = "example-string-to-protect"
}


/*--------------------------------------------------------------------------
             Resize Image Terraform code
--------------------------------------------------------------------------*/
/*

/*--------------------------------------------------------------------------
             Creates the source image bucket
--------------------------------------------------------------------------*/
resource "aws_s3_bucket" "source-image-bucket" {
    bucket = "test-source-image-bucket-5623"
    acl = "public-read-write"
    force_destroy = true

 versioning {
    enabled = true
 }
}

/*--------------------------------------------------------------------------
             Creates the refactored image bucket
--------------------------------------------------------------------------*/
resource "aws_s3_bucket" "refactored-image-bucket" {
    bucket = "test-refactored-image-bucket-5623"
    acl = "public-read-write"
    force_destroy = true
    
 versioning {
    enabled = true
 }
}

/*--------------------------------------------------------------------------
          Allows Lambda function to be invoked from S3 bucket
--------------------------------------------------------------------------*/
resource "aws_lambda_permission" "allow_source_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = "lambda_function"
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.source-image-bucket.arn
}

/*--------------------------------------------------------------------------
              Creates function from zip file
--------------------------------------------------------------------------*/
resource "aws_lambda_function" "func" {
  filename      = "lambda_function.zip"
  function_name = "lambda_function"
  role          = "arn:aws:iam::257173663825:role/lambda_stuffs"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  layers        = ["arn:aws:lambda:eu-west-2:770693421928:layer:Klayers-python38-Pillow:14"]
  
  timeout = 15
  
  environment {
       variables = {
           DST_BUCKET = "refactored-image-bucket-5623"
           REGION = "eu-west-2"
        }
  }
}

/*--------------------------------------------------------------------------
      Sets S3 notification when object is created in source bucket
      triggers lambda function
--------------------------------------------------------------------------*/
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.source-image-bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.func.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_source_bucket]
}
*/