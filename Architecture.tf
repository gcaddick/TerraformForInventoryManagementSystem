/*
Overview:

Terraform code to create a Inventory Management system

Creates:


To Dos:

*/

provider "aws" {
 region = "eu-west-2"
}

resource "aws_vpc" "ApplicationVPC" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "PublicSubnet" {
  vpc_id     = aws_vpc.ApplicationVPC.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "Main"
  }
}