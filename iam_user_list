import boto3

def list_iam_users():
    # Create an IAM service client
    iam_client = boto3.client('iam')

    # Initialize the list to store user information
    users = []

    # Paginate through the list of users
    paginator = iam_client.get_paginator('list_users')
    for response in paginator.paginate():
        users.extend(response['Users'])

    return users

def main():
    # List IAM users
    users = list_iam_users()
    for user in users:
        print(f"User: {user['UserName']}, ARN: {user['Arn']}")

if __name__ == "__main__":
    main()
