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
  enable_dns_hostnames = true
  enable_dns_support = true
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
            Defines route table for subnet and IG
--------------------------------------------------------------------------*/
resource "aws_route_table" "route-table-env" {
  vpc_id = aws_vpc.ApplicationVPC.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "subnet-association" {
  subnet_id      = aws_subnet.PrivateSubnet.id
  route_table_id = aws_route_table.route-table-env.id
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
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:*"],
      "Resource": ["arn:aws:dynamodb:eu-west-2:257173663825:table/Inventory"]
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:*"],
      "Resource": ["arn:aws:dynamodb:eu-west-2:257173663825:table/Users"]
    }
  ]
}
EOF
}





/*--------------------------------------------------------------------------
          Creates elastic IP for EC2
--------------------------------------------------------------------------*/
resource "aws_eip" "ip-test-env" {
  instance = "${aws_instance.WebsiteEC2.id}"
  vpc      = true
}

/*--------------------------------------------------------------------------
          Defines ec2 instance for program to run
--------------------------------------------------------------------------*/
resource "aws_instance" "WebsiteEC2" {
  ami           = "ami-0fc15d50d39e4503c"
  instance_type = "t2.micro"
  subnet_id = aws_subnet.PrivateSubnet.id
  user_data = "${file("user-data-website.sh")}"
  key_name = "testKeyPair2"
  iam_instance_profile = "${aws_iam_instance_profile.web_instance_profile.id}"
  security_groups = ["${aws_security_group.sg_ec2.id}"]
}


/*--------------------------------------------------------------------------
          Defines secret manager
--------------------------------------------------------------------------*/
/*
resource "aws_secretsmanager_secret" "Secrets" {
  name = "SuperSecret"
}

resource "aws_secretsmanager_secret_version" "DynamoDBSecrets" {
  secret_id     = aws_secretsmanager_secret.Secrets.id
  secret_string = "example-string-to-protect"
}
*/

