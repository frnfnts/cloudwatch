import boto3
import pprint
import datetime

log_group_name = '/ecs/hoge'
start_time = "2023/10/21 00:00:00"
end_time = "2023/10/22 00:00:00"
save_file_name = "log.txt"


def convert_to_unixtime(time_string):
    time_format = "%Y/%m/%d %H:%M:%S"
    datetime_obj = datetime.datetime.strptime(time_string, time_format)
    unixtime = datetime_obj.timestamp() * 1000
    return int(unixtime)


def main():
    client = boto3.client('logs')
    args = {
        'logGroupName': log_group_name,
        'startTime': convert_to_unixtime(start_time),
        'endTime': convert_to_unixtime(end_time),
    }
    events = []

    while True:
        print("get log events")
        response = client.filter_log_events(**args)
        print(f"num of events: {len(response['events'])}")
        events.extend(response['events'])
        if 'nextToken' not in response:
            break
        args['nextToken'] = response['nextToken']

    messages = list(map(lambda x: x["message"], events))
    if save_file_name:
        with open(save_file_name, mode='w') as f:
            f.write("\n".join(messages))
    else:
        pprint.pprint(messages)


if __name__ == '__main__':
    main()
