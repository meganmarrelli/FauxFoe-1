
# coding: utf-8

# In[50]:

# FauxFoe is being produced by myself and Megan Marelli, a colleague and fellow CJS student. 

# The premise is quite simple. We will leverage Google's new ClaimReview to monitor Twitter. First and foremost, 
# if a Twitter user publishes a link that has been subjected to Google's ClaimReview, FauxFoe will comment on that 
# tweet or DM the user responsible for the tweet notifying them that the claim has been reviewed. 

# As FauxFoe continues to grow, we plan to parse each tweet so that we can address users that rely on 'fake news' 
# for information rather than for direct posts. For instance, if somebody uses a ClaimReviewed fact in a Twitter 
# argument, but does not post the exact link, FauxFoe will be able to address that claim. 

# Alas, for now, FauxFoe is in its infancy. Below is some of the base code that will be used to operate FauxFoe. 


# In[51]:

# The guideliens to the metadata can be found here... 
# http://schema.org/ClaimReview


# In[52]:

import requests
# Requests documentation: http://docs.python-requests.org/en/master/

url = 'http://feeds.washingtonpost.com/rss/rss_fact-checker'
# As an example of FauxFoe's leveraging ClaimReview, we will pull the rss feed from the Washington Post's Fact 
# Checker, which includes articles that utilize Google's ClaimReview. 

r = requests.get(url)

print r.text
# Below is the HTML text from the WaPo Fact Checker RSS feed. 


# In[53]:

from bs4 import BeautifulSoup
# BeautifulSoup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

soup = BeautifulSoup(r.text)

print soup


# In[54]:

url_list = []
# Create a new, empty array in which we can store the URL's for each of the ClaimReviewed articles featured on the 
# WaPo Fact Checker site. 

for a in soup.find_all('a', href=True): 
    print "Found the URL:", a['href']
    url_list.append(a['href'])


# In[55]:

url_list


# In[57]:

for i in url_list: 
# For every URL...
    x = requests.get(i)
    soup = BeautifulSoup(x.text)
    print(soup)
    # Print the 'soup' (aka 'BeautifulSoup the URL')


# In[58]:

# We will now pull aspects of the ClaimReview micro data (which can be found at schema.org) for each URL so that we
# can later put that data into a dataframe (it'll all make sense in a moment!)

x = requests.get(i)
soup = BeautifulSoup(x.text)
l = (soup(itemprop="claimReviewed"))
m = (soup(itemprop="ratingValue"))
n = (soup(itemprop="datePublished"))
o = str(i)


# In[59]:

print l
print m 
print n
print o


# In[60]:

# To explore the rating scale, visit: https://developers.google.com/search/docs/data-types/factcheck


# In[61]:

import pandas as pd
from pandas import DataFrame


# In[62]:

print "claimReviewed: " + l[0].text
print "ratingValue: " + m[0].text
print "datePublished: " + n[0].text
print "url: " + o


# In[63]:

column_names = ["claimReviewed","datePublished","ratingValue","url"]
# Generate the column names for our data frame... 

rows = []
# Generate an empty array titled 'rows' (which we will import our ClaimReview data into in a moment)

for i in url_list: 
    x = requests.get(i)
    soup = BeautifulSoup(x.text)
    
    l = (soup(itemprop="claimReviewed"))
    m = (soup(itemprop="ratingValue"))
    n = (soup(itemprop="datePublished"))
    o = str(i)
    # Note that this is the same code as before, only now we are importing it into the data frame! 
    
    rows.append([l[0].text,n[0].text,m[0].text,o]) 

df = DataFrame(rows,columns=column_names)


# In[64]:

pd.options.display.max_colwidth = 300

df


# In[19]:

CONSUMER_KEY = "TKTKTK"
CONSUMER_SECRET = "TKTKTK"
ACCESS_TOKEN = "TKTKTK"
ACCESS_TOKEN_SECRET = "TKTKTK"


# In[20]:

from tweepy import OAuthHandler, API
# Tweepy documentation: http://docs.tweepy.org/en/v3.5.0/

# Setup the authentication
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create an object we will use to communicate with the Twitter API
api = API(auth)


# In[27]:

from tweepy import Cursor
# A brief introduction to Tweepy's Cursor: http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html#introduction

query = df["claimReviewed"][9]

ids = []
texts = []
times  = []
retweets = []
screen_names = []
followers_counts = []
friends_counts = []

# Only iterate through the first 3 pages (for now!)
for page in Cursor(api.search, q=query, result_type='recent', count=100, until="2017-04-26").pages(170):
    
    for tweet in page:

        ids.append(tweet.id)
        texts.append(tweet.text)
        times.append(tweet.created_at)
        retweets.append(tweet.retweet_count)
        screen_names.append(tweet.user.screen_name)
        friends_counts.append(tweet.user.friends_count)
        followers_counts.append(tweet.user.followers_count)


# In[29]:

texts


# In[65]:

# The above 'texts' is every tweet from the Tweepy Cursor pull earlier, and it shows us all the tweets that FauxFoe 
# can reply to - tweets that directly reference an article that has been fact checked, whether or not the user 
# tweeting the article knows about ClaimReview at all! 


# In[ ]:



