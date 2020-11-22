import requests
from datetime import datetime
import traceback
import time
import csv
import praw

subreddit = "SkincareAddiction"

url = "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&subreddit={}&before="

start_time = datetime.utcnow()

reddit = praw.Reddit(
    client_id="rQ7jg1bvuSI9PA",
    client_secret="k5YVDGG2FcrjavT8gDNqAoiSGhgSaQ",
    user_agent="my user agent"
    )

csv_delimiter = "|"
def getSubComments(comment, allComments):
    if not comment.author == "AutoModerator":
        allComments.append(comment.body)
        if not hasattr(comment, "replies"):
            replies = comment.comments()
        else:
            replies = comment.replies
        for child in replies:
            getSubComments(child, allComments)

def downloadComment(r, submissionId):
    submission = r.submission(submissionId)
    comments = submission.comments
    commentsList = []
    for comment in comments:
        getSubComments(comment, commentsList)
    return commentsList

def downloadFromUrl(filename, object_type):
    print(f"Saving {object_type}s to {filename}")

    csv_columns = ['time', 'score', 'flair', 'title', 'selftext', 'comments']
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter= csv_delimiter)
        writer.writeheader()

    count = 0
    previous_epoch = int(start_time.timestamp())

    while True:
        new_url = url.format(object_type, subreddit)+str(previous_epoch)
        print(new_url)
        try:
            get_data = requests.get(new_url)
        except:
            print('!!!Get link failed')
            pass
        try:
            json_data = get_data.json()
        except:
            print('!!!Parse request as json failed')
            pass

        # pushshift has a rate limit, if we send requests too fast it will start returning error messages            
        time.sleep(1)

        if 'data' not in json_data:
            break
        objects = json_data['data']
        if len(objects) == 0:
            break

        for object in objects:
            previous_epoch = object['created_utc'] - 1
            count += 1
            if object_type == 'submission':
                if object['is_self']:
                    if 'selftext' not in object or object['selftext'] == '[removed]' or object['selftext'] == '[deleted]':
                        continue
                    try:
                        submission_id = object['id']
                         
                        title_ = object['title'].encode(encoding='utf-8', errors='ignore').decode()
                        title  = ''
                        not_include = False
                        for ch in title_:
                            if ch =='[':
                                not_include = True
                            elif ch == ']':
                                not_include = False
                            if not_include:
                                pass
                            else:
                                title += ch
                        title = title.strip(']').strip(' ')
                            

                        if object['selftext']:
                            selftext = object['selftext'].encode(encoding='utf-8', errors='ignore').decode()
                            selftext = selftext.replace('\n', ' ').replace('|', ' ')
                        else:
                            selftext = "None"

                        if 'link_flair_text' in object:
                            if object['link_flair_text']:
                                flair = object['link_flair_text']
                        else:
                            flair = "None"

                        comments = downloadComment(reddit, submission_id)

                        data = {'time'    : datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d"),
                                'score'   : object['score'],
                                'flair'   : flair,  
                                'title'   : title, 
                                'selftext': selftext,
                                'comments': comments}


                        with open(filename, "a") as csvfile:  
                            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=csv_delimiter)
                            writer.writerow(data)      
                    except:
                        print(f"Failed to unpack and save submission: {object['url']}")
                        print(traceback.format_exc())

        print("Saved {} {}s through {}".format(count, object_type, datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))

    print(f"Saved {count} {object_type}s")

downloadFromUrl("posts.csv", "submission")

