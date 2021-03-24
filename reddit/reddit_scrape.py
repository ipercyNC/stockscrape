from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed

import requests
import datetime
import traceback
from time import time,sleep
import json
import sys


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown Type")


def downloadFromUrl(filter_string, filename, object_type, start_date):

    url = "https://api.pushshift.io/reddit/{}/search?q=gme&size=100&sort=desc&{}&after="

    count = 0
    previous_epoch = start_date
    comments_dict = {}
    while True:
        new_url = url.format(object_type, filter_string)+str(previous_epoch)
        json_text = requests.get(new_url)
        sleep(1)  # pushshift has a rate limit, if we send requests too fast it will start returning error messages
        try:
            json_data = json_text.json()
        except json.decoder.JSONDecodeError:
            sleep(1)
            continue

        if 'data' not in json_data:
            break
        objects = json_data['data']
        if len(objects) == 0:
            break
        print(len(objects))
        for object in objects:
            previous_epoch = object['created_utc'] - 1
            count += 1

            if object_type == 'comment':
                try:
                    print(object)
                    comment = {'score': str(object['score']),
                               'date': datetime.datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d"),
                               'body': object['body'].encode(encoding='ascii', errors='ignore').decode()}
                    comments_dict[object['id']] = comment
                    comment = {}

                except Exception as err:
                    print(f"Couldn't print comment: https://www.reddit.com{object['permalink']}")
                    print(traceback.format_exc())
        print("Saved {} {}s through {}".format(count, object_type, datetime.datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))




if __name__ == "__main__":
    username = ""
    subreddit = "wallstreetbets"

    filter_string = None
    if username == "" and subreddit == "":
        print("Fill in either username or subreddit")
        sys.exit(0)
    elif username == "" and subreddit != "":
        filter_string = f"subreddit={subreddit}"
    elif username != "" and subreddit == "":
        filter_string = f"author={username}"
    else:
        filter_string = f"author={username}&subreddit={subreddit}"

    first_date = datetime.date(2019, 1, 1)

    downloadFromUrl(filter_string, "comments.txt", "comment", first_date)
