from slack_webhook import Slack
import datetime
from datetime import datetime
import requests
import json
import math

# Send Message to Channel with Slack WebHook 
def api_call(msg):
    slack = Slack(url='{YOUR_WEBHOOK_URL}')
    slack.post(text=msg)

# Getting Repo List in Project
repo_url = 'https://{YOUR_BITBUCKET_DOMAIN}/rest/api/1.0/projects/{PROJECT_NAME}/repos?limit=1000'
r_repo = requests.get(repo_url, headers= {"Authorization": "Bearer {YOUR_ACCESS_TOKEN}"})
data_repo = json.loads(r_repo.text)

repo_list = []

for repo in range(len(data_repo['values'])):
    repo_list.append(data_repo['values'][repo]['slug'])


# Getting PR Info from Repos
msg = ''
pr_url_list = []
pr_reviewer_list = []
pr_cd_day_list = []
pr_cd_hour_list = []

for repo in repo_list:
    url = 'https://{YOUR_BITBUCKET_DOMAIN}/rest/api/1.0/projects/{PROJECT_NAME}/repos/' + repo + '/pull-requests'
    r = requests.get(url, headers= {"Authorization": "Bearer {YOUR_ACCESS_TOKEN}"})
    data = json.loads(r.text)

    # Getting PR Count in Repo
    pr_count = data['size']

    # Getting PR Info If PR Exists
    if pr_count != 0:
        for i in range(pr_count):

            # Getting PR Info
            pr_url_list.append('https://{YOUR_BITBUCKET_DOMAIN}/projects/{PROJECT_NAME}/repos/' + repo + '/pull-requests/' + str(data['values'][i]['id']))
            
            # Getting PR Reviewer Info
            if 'user' in str(data['values'][i]['reviewers']):
                pr_reviewer_list.append(str(data['values'][i]['reviewers'][0]['user']['name']) + ' :ok:')
            else:
                pr_reviewer_list.append(' Rewiewer yok. :cry:')
            
            # Getting PR Create Day and Hour
            pr_date = datetime_time = datetime.fromtimestamp((data['values'][i]['createdDate'])/1000)
            now = datetime.now()
            days = abs((now - pr_date).days)
            hours = math.floor(((now - pr_date).seconds) / 3600)
            pr_cd_day_list.append(str(days))
            pr_cd_hour_list.append(str(hours))

        # Adding PR Info to Message
        msg += '*Repo:* ' +  repo + '\n' + "  PR Count: " + str(pr_count) + '\n' 
        for i in range(pr_count):
            msg += '  :point_right: PR URL: ' + pr_url_list[i] + '\n'
            msg += '  :nerd_face: Reviewer: @' + pr_reviewer_list[i] + '\n'
            msg += '  :fire: It was opened ' + pr_cd_day_list[i] + ' day(s), ' + pr_cd_hour_list[i] + ' hour(s) ago.\n'

    # Refresh values for new Repo
    pr_count = 0
    pr_url_list = []
    pr_reviewer_list = []
    pr_cd_day_list = []
    pr_cd_hour_list = []

# Print Final Message to Console
print(msg)

# Sending Slack Message
now = datetime.now()
hour = now.hour
if hour >= 9 and hour <= 18:
    api_call(msg)




    

