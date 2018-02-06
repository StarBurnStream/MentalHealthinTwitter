import boto3
import os
MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
MTURK_LIVE = 'https://mturk-requester.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
   aws_access_key_id = "AKIAJSHQWKK2WI7PZ4RA",
   aws_secret_access_key = "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",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
   #endpoint_url = MTURK_LIVE
)




new_hit = mturk.create_hit(
    Title = 'Live Test: Analysis of Tweets and Twitter Habits', #sandbox
    #Title = 'Analysis of Tweets and Twitter Habits', #live
    Description = 'In this HIT you will be asked to fill out questions related to your personal health.  You will also be asked to share your twitter user name and user id',
    Keywords = 'Twitter; personal health',
    Reward = '0.00',
    MaxAssignments = 5,
    LifetimeInSeconds = 604800,
    AssignmentDurationInSeconds = 1200,
    AutoApprovalDelayInSeconds = 604800,
    #Question = question,
    HITLayoutId = '3BBRW2DWDTQPFWKD0KWI9O4E553CSJ' #sandbox
    #HITLayoutId = '3KSK2GNGR05CCNAEWXA34IX5W8MH35' #live
    #HITLayoutId = '38AN5L8GAF652MTDOGY6ZWQERLPYN0' # this one is from the production site
)
#print("A new HIT has been created. You can preview it here:")
#print "https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId']
#print "HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)"

hit_type_id = new_hit['HIT']['HITTypeId']
hit_id = new_hit['HIT']['HITId']
hit_title = new_hit['HIT']['Title']
hit_group_id = new_hit['HIT']['HITGroupId']
print ("\nCreated HIT: {}".format(hit_id))


#work = "https://www.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'] #live
work = "https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'] #sandbox
print ("\nYou can work and preview the HIT here:")
print (work)

#result = "https://requester.mturk.com/mturk/manageHITs" #live
result = "https://requestersandbox.mturk.com/mturk/manageHITs" #sandbox
print ("\nAnd see results here:")
print (result)

if os.path.isfile('Data/MTurk/hitsinfo.csv'):
	hitFile = open('Data/MTurk/hitsinfo.csv','a')
else:
	hitFile = open('Data/MTurk/hitsinfo.csv','a')
	hitFile.write('HitID,HitTypeID,HitGroupID,Title,WorkingLink,ResultLink\n')
hitFile.write(hit_id + ',' + hit_type_id + ',' + hit_group_id + ',' + hit_title + ',' + work + ',' + result + '\n')
