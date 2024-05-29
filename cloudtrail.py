import boto3
from datetime import datetime, timedelta

def get_cloudtrail_events(days):
    # Create a CloudTrail client
    cloudtrail_client = boto3.client('cloudtrail')

    # Define the time range for the events
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    # Get events within the specified time range
    response = cloudtrail_client.lookup_events(
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50
    )

    events = response['Events']

    # If there are more events, keep fetching them
    while 'NextToken' in response:
        response = cloudtrail_client.lookup_events(
            NextToken=response['NextToken'],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=50
        )
        events.extend(response['Events'])

    return events

def main():
    # Specify the number of days to look back in the logs
    days = 1
    events = get_cloudtrail_events(days)

    for event in events:
        print(f"Event ID: {event['EventId']}")
        print(f"Event Name: {event['EventName']}")
        print(f"Event Time: {event['EventTime']}")
        print(f"User Name: {event.get('Username', 'N/A')}")
        print(f"Event Source: {event['EventSource']}")
        print(f"Resources: {event.get('Resources', 'N/A')}")
        print("------")

if __name__ == "__main__":
    main()
