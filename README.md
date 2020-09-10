# RedditBot

Created a Reddit Bot using the PRAW package as well as pandas and sklearn libraries. This bot collects data on each submission in the r/rutgers subreddit. It then uses 
machine learning algorithms to be able to predict the number of upvotes future submissions to the subreddit will receive based on that information (the model is trained on that gathered information). 
The final method of the program scans all new submissions to the subreddit, and, if the submissions or their titles mention any cs courses, the bot replies the link to the appropriate Rutgers CS discord to them. 
