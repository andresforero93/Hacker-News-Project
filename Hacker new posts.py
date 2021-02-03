#!/usr/bin/env python
# coding: utf-8

# # ANALYSING HACKER NEWS POSTS 

# ## Introduction

# This project aims to analyze Hacker News posts, it is a web site where  users submitted stories( kwnow as "posts") and they are voted and coomented upon. posts can get hundreds of thousands of visitors.
# 
# We will focus on posts whose titles being with "Ask HN" or " Show HN".
# 
# Users submit Ask Hn posts to ask the Hacker News community a specific question. Also, users submit Show HN posts to show the Hacker News community projects,products or any other interesting matter.
# 
# we will compare Ask HN and Show HN posts to determine which of them receive more comments on average and whether certain time of posts created receive more comments on average.
# 
# Here it is the [link](https://www.kaggle.com/hacker-news/hacker-news-posts) to the database used for this project.
# 
# The database used here have reduced from 300,000 rows to approximately 20,000 rows by removing all submissions that did not receive any comments.

# In[1]:


# import reader, reading file and displaying first 5 rows
from csv import reader
open_file= open("hacker_news.csv")
read_file= reader(open_file)
hn=list(read_file)
hn[:5]


# The first list in the inner lists contains the column headers, and the lists after contain the data for one row. In order to analyze our data, we need to first remove the row containing the column headers.

# In[2]:


#storing columns headers in a variable
headers= hn[0]


# In[3]:


#removing the first row from hn and displaying the variable
hn=hn[1:]
print(headers)


# In[4]:


#checking data without headers
hn[:5]


# We are only concerned with post titles beginning with Ask HN or Show HN. for this we will create new lists that contain just the data for those tittles.
# 

# In[5]:


ask_posts=[]
show_posts=[]
other_posts=[]


# In[6]:


for row in hn:
    title=row[1]
    if title.lower().startswith("ask hn"):
        ask_posts.append(row)
    elif title.lower().startswith("show hn"):
        show_posts.append(row)
    else:
        other_posts.append(row)
        
print("Number of asks posts:", len(ask_posts))
print("Number of show posts:", len(show_posts))
print("Number of other posts:", len(other_posts))      


# Now let's figure out if ask posts or show posts receive more comments on average

# In[7]:


#ASK POSTS
total_ask_comments=0
for row in ask_posts:
    comment=int(row[4])
    total_ask_comments +=comment    
print("total comments of ask posts:",total_ask_comments)       


# In[8]:


avg_ask_comments=total_ask_comments/(len(ask_posts))
print(avg_ask_comments)


# In[9]:


#SHOW COMMENTS
total_show_comments=0
for row in show_posts:
    comment=int(row[4])
    total_show_comments +=comment    
print("total comments of show comments:",total_show_comments)  


# In[10]:


avg_show_comments=total_show_comments/(len(show_posts))
print(avg_show_comments)


# In[11]:


print("Average number of comments on ask posts:",avg_ask_comments)
print("Average number of comments on show posts:",avg_show_comments)


# We can find that ask posts has in average more comments per post that show posts.Since ask posts are more likely to receive comments, we'll focus our remaining analysis just on these posts

# Next, we'll determine if ask posts created at a certain time are more likely to attract comments. We'll use the following steps to perform this analysis:
# 
# 1. Calculate the amount of ask posts created in each hour of the day, along with the number of comments received.
# 2. Calculate the average number of comments ask posts receive by hour created.

# In[12]:


import datetime as dt


# In[13]:


result_list=[]
# store amount of comments for ask posts with created date
for row in ask_posts:
    created=row[6]
    num_comments=int(row[4])
    result_list.append([created,num_comments]) # create list of lists
    
print(result_list)


# In[14]:


#now let's find amount of posts and comments taking 
#hour of creation into account 

counts_by_hour= {}
comments_by_hour={}

for row in result_list:
    hour=row[0]
    n_comment=row[1]
    date=dt.datetime.strptime(hour,"%m/%d/%Y %H:%M").strftime("%H")
    if date not in counts_by_hour:
        counts_by_hour[date]=1
        comments_by_hour[date]=n_comment
    else:
        counts_by_hour[date]+=1
        comments_by_hour[date]+=n_comment
        
print(counts_by_hour)
print("\n")
print(comments_by_hour)


# Next, we'll use these two dictionaries to calculate the average number of comments for posts created during each hour of the day.

# In[15]:


avg_by_hour=[]
for hour in comments_by_hour:
    posts=counts_by_hour
    comments=comments_by_hour
    avg_by_post=round(comments[hour]/posts[hour],2)
    avg_by_hour.append([hour,avg_by_post])
    
print(avg_by_hour)


# This format makes it hard to identify the hours with the highest values. Let's finish by sorting the list of lists and printing the five highest values in a format that's easier to read.

# In[16]:


# first let's swap columns of avg_by_hour list
swap_avg_by_hour=[]
for row in avg_by_hour:
    hour=row[0]
    n_comment=row[1]
    swap_avg_by_hour.append([n_comment,hour])
print(swap_avg_by_hour)


# In[17]:


sorted_swap= sorted(swap_avg_by_hour,reverse=True)
print(sorted_swap[:5])
print("Top 5 Hours for Ask Posts Comments")


# In[18]:


for average,hour in sorted_swap[:5]:
    avg= average
    date=dt.datetime.strptime(hour,"%H").strftime("%H:%M:")
    final="{} {} average comments per post".format(date,avg)                                                
    
    
    print(final)


# ## CONCLUSION
# 
# Revising the results we can say that users on Hackers News for Ask posts have more comments at 15:00 with 38.9 comments per posts (the time zone is Eastern Time in the US), so at this hour you have a higher chance of receiving comments if you want to ask something to Hackers News community. However, the next best average comments per post are after 15:00 and the second place  is really far away of the top but the second place to down is closer among them on average. Then you can try to post an Ask post from 16:00 to 02:00 hours but you will get more chance to receive more comments at 15:00, this is a better hour to post.
