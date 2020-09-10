import praw
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import time
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

reddit = praw.Reddit(client_id='KUrxlM6Hu1Gk9g', client_secret='rgkh8x0XzfOhCaxFA-tucUWO1-0', username='blizz2016',
                         password='Lightsaber310!', user_agent='mlbot')

subreddit = reddit.subreddit('rutgers')


discordlinalg='https://discord.com/channels/682667655043350528/682682885270143022'
csdiscord='https://discord.com/channels/409134033898045470'
discord111='https://discord.com/channels/409134033898045470/419524665384370186'
discord112='https://discord.com/channels/409134033898045470/419524680106508288'
discord205='https://discord.com/channels/409134033898045470/525140732453978141'
discord206='https://discord.com/channels/409134033898045470/525140740838391808'
discord213='https://discord.com/channels/409134033898045470/552631267653582859'
discord214='https://discord.com/channels/409134033898045470/525140613474156544'
discord314='https://discord.com/channels/409134033898045470/552631003961622529'
discord323='https://discord.com/channels/409134033898045470/580873215359057945'
discord336='https://discord.com/channels/409134033898045470/552630975872499763'
discord344='https://discord.com/channels/409134033898045470/525140715467046932'
discord352='https://discord.com/channels/409134033898045470/552630957296058378'
discord440='https://discord.com/channels/409134033898045470/552630769491640323'
discord416='https://discord.com/channels/409134033898045470/552630835023577118'

commentnumber=[]
score=[]
lengthofsubmissions=[]
lengthoftitle=[]
textbodies=[]
rutgers=[]
#cswords=['cs','CS','Cs','cS','compsci']







def loaddata():


    for submission in subreddit.new(limit=None):
        body=str(submission.selftext)
        title=str(submission.title)
        t=re.split('[,.!?\s]\s*', title)
        x=re.split('[,.!?\s]\s*', body)
        count=0

        for element in x:
            if element=="Rutgers" or element=="rutgers" or element=="RU" or element=="ru" or element=="Ru" or element=="rut":
                count=count+1
        for element in t:
            if element == "Rutgers" or element == "rutgers" or element == "RU" or element == "ru" or element == "Ru" or element == "rut":
                count = count + 1

        rutgers.append(count)
        textbodies.append(x)
        lengthofsubmissions.append(len(x))
        lengthoftitle.append((len(t)))
        commentnumber.append(submission.num_comments)
        score.append(submission.score)

def runmodels(df):


    X=df[['CommentNumber','TitleLength','Rutgers']]
    Y=df[['Score']]
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2, shuffle=False)

    linearmodel=LinearRegression()
    linearmodel.fit(X_train,Y_train)
    linpredict=linearmodel.predict(X_test)
    linscore=r2_score(Y_test,linpredict)

    svrmodel=SVR(kernel='rbf')
    svrmodel.fit(X_train,Y_train)
    svrpredict=svrmodel.predict(X_test)
    svrscore = r2_score(Y_test, svrpredict)

    treemodel=DecisionTreeRegressor(random_state=0)
    treemodel.fit(X_train,Y_train)
    treepredict=treemodel.predict(X_test)
    treescore=r2_score(Y_test, treepredict)

    r2scores = [linscore,svrscore,treescore]

    for i in r2scores:
        print(i)

    if linscore>=svrscore and linscore>=treescore :
        print("linearmodel")
        return linearmodel
    elif svrscore>=linscore and svrscore>=treescore:
        print("SVR")
        return svrmodel
    else:
        print("tree")
        return treemodel

def replypred(model):


    for submission in subreddit.stream.submissions():
        commentsnum=submission.num_comments
        submissionid=(str)(submission.id)
        body = str(submission.selftext)
        title = str(submission.title)
        tmessage = re.split('[,.!?\s]\s*', title)
        xmessage = re.split('[,.!?\s]\s*', body)
        countmessage=0
        for element in xmessage:
            if element=="Rutgers" or element=="rutgers" or element=="RU" or element=="ru" or element=="Ru" or element=="rut":
                countmessage=countmessage+1
        for element in tmessage:
            if element == "Rutgers" or element == "rutgers" or element == "RU" or element == "ru" or element == "Ru" or element == "rut":
                countmessage = countmessage + 1
        tlength=len(tmessage)
        prediction=(str)((model.predict([[commentsnum,tlength,countmessage]]))[0])
        author=(str)(submission.author)
        message="Based on the number of comments, title length, the number of times Rutgers is mentioned in your submission ID "+submissionid + " and body length of this submission, the expected score of this submission is "+prediction
        reddit.redditor(author).message("Fun Upvote Prediction:", message)
        print("Replied:"+message+"to redditor"+author)
        time.sleep(90)


def csbothelper():

    for submission in subreddit.stream.submissions():
        body3=(str(submission.selftext)).lower()
        title3=(str(submission.title)).lower()
        titlearray = re.split('[,.!?\s]\s*', title3)
        bodyarray = re.split('[,.!?\s]\s*', body3)
        commentlist=submission.comments.list()

        fullwordcstitle=False

        alreadyreplied=[]



        doreply=False
        messagesegments=[]


        message="The General Rutgers CS Discord is (please log into discord before clicking the link):"+csdiscord+"."
        messagesegments[0]=message
        additionaldiscord=0
        for index in range(len(titlearray)):
            if titlearray[index]=='science' and titlearray[index-1]=='computer':
                fullwordcstitle=True


        for element in titlearray:
            if element=='cs' or element=='coding' or element=='programming' or fullwordcstitle==True:
                doreply=True

            if element=='111' or element=='cs111' or element=='introcs' or element=='01:198:111' or element=='198:111' or title3.find("introduction to computer science")!=-1:
                doreply=True
                if(additionaldiscord==0):
                    messagesegments.append("Based on your post, you should also specifically visit discords (separated by commas and spaces): "+discord111+" ,")
                else:
                    messagesegments.append(discord111 + " , ")
                additionaldiscord=additionaldiscord+1
                alreadyreplied.append('111')
            if element == '112' or element == 'cs112' or element == 'ds' or element == '01:198:112' or element == '198:112' or title3.find("data structures") != -1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord112 + " ,")
                else:
                    messagesegments.append(discord112 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('112')
            if element == '205' or element == 'cs205' or element == 'discrete' or element == '01:198:205' or element == '198:205' or title3.find("introduction to discrete structures") != -1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord205 + " ,")
                else:
                    messagesegments.append(discord205 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('205')
            if element == '206' or element == 'cs206' or element == 'discrete' or element == '01:198:206' or element == '198:206' or title3.find("introduction to discrete structures") != -1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord206 + " ,")
                else:
                    messagesegments.append(discord206 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('206')
            if element == '213' or element == 'cs213' or title3.find("softmeth") != -1 or title3.find("soft meth") != -1 or element == '01:198:213' or element == '198:213' or title3.find("software methodology") != -1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord213 + " ,")
                else:
                    messagesegments.append(discord213 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('213')
            if element=='214' or element=='cs214' or (element=='systems' and title3.find('operating')==-1) or element=='01:198:214' or element=='198:214' or title3.find("systems programming")!=-1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord214 + " ,")
                else:
                    messagesegments.append(discord214 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('214')
            if element=='314' or element=='cs314' or element=='prin' or element=='prog' or element=='01:198:314' or element=='198:314' or title3.find("principles of programming")!=-1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord314 + " ,")
                else:
                    messagesegments.append(discord314 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('314')
            if element=='323' or element=='cs323' or title3.find("num anal")!=-1 or element=='01:198:323' or element=='198:323' or title3.find("numerical analysis")!=-1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord323 + " ,")
                else:
                    messagesegments.append(discord323 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('323')
            if element=='336' or element=='cs336' or element=='databases' or element=='01:198:336' or element=='198:336' or title3.find("principles of information and database management")!=-1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord336 + " ,")
                else:
                    messagesegments.append(discord336 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('336')
            if element=='344' or element=='cs344' or element=='algo' or element=='01:198:344' or element=='198:344' or title3.find("design and analysis of computer algorithms")!=-1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord344 + " ,")
                else:
                    messagesegments.append(discord344 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('344')
            if element=='440' or element=='cs440' or element=='ai' or element=='01:198:440' or element=='198:440' or title3.find("artificial intelligence")!=-1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord440 + " ,")
                else:
                    messagesegments.append(discord440 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('440')
            if element=='416' or element=='cs416' or element=='os' or element=='01:198:416' or element=='198:416' or title3.find("operation systems")!=-1:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord416 + " ,")
                else:
                    messagesegments.append(discord416 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('416')
            if element=='250' or element=='linalg' or element=='01:640:250' or element=='640:250' or body3.find("Introduction to Linear Algebra")!=-1:
                doreply = True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord111 + " ,")
                else:
                    messagesegments.append(discord111 + " , ")
                additionaldiscord = additionaldiscord + 1
                alreadyreplied.append('250')
        for element in bodyarray:
            if element=='cs' or element=='coding' or element=='programming' or fullwordcstitle==True:
                doreply=True
            if element=='250' or element=='linalg' or element=='01:640:250' or element=='640:250' or body3.find("Introduction to Linear Algebra")!=-1 and '250' not in alreadyreplied:
                doreply = True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord111 + " ,")
                else:
                    messagesegments.append(discord111 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='111' or element=='cs111' or element=='introcs' or element=='01:198:111' or element=='198:111' or body3.find("introduction to computer science")!=-1 and '111' not in alreadyreplied:
                doreply=True
                if(additionaldiscord==0):
                    messagesegments.append("Based on your post, you should also specifically visit discords (separated by commas and spaces): "+discord111+" ,")
                else:
                    messagesegments.append(discord111 + " , ")
                additionaldiscord=additionaldiscord+1
            if element == '112' or element == 'cs112' or element == 'ds' or element == '01:198:112' or element == '198:112' or body3.find("data structures") != -1 and '112' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord112 + " ,")
                else:
                    messagesegments.append(discord112 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element == '205' or element == 'cs205' or element == 'discrete' or element == '01:198:205' or element == '198:205' or body3.find("introduction to discrete structures") != -1 and '205' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord205 + " ,")
                else:
                    messagesegments.append(discord205 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element == '206' or element == 'cs206' or element == 'discrete' or element == '01:198:206' or element == '198:206' or body3.find("introduction to discrete structures") != -1 and '206' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord206 + " ,")
                else:
                    messagesegments.append(discord206 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element == '213' or element == 'cs213' or body3.find("softmeth") != -1 or body3.find("soft meth") != -1 or element == '01:198:213' or element == '198:213' or body3.find("software methodology") != -1 and '213' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord213 + " ,")
                else:
                    messagesegments.append(discord213 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='214' or element=='cs214' or (element=='systems' and body3.find('operating')==-1) or element=='01:198:214' or element=='198:214' or body3.find("systems programming")!=-1 and '214' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord214 + " ,")
                else:
                    messagesegments.append(discord214 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='314' or element=='cs314' or element=='prin' or element=='prog' or element=='01:198:314' or element=='198:314' or body3.find("principles of programming")!=-1 and '314' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord314 + " ,")
                else:
                    messagesegments.append(discord314 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='323' or element=='cs323' or body3.find("num anal")!=-1 or element=='01:198:323' or element=='198:323' or body3.find("numerical analysis")!=-1 and '323' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord323 + " ,")
                else:
                    messagesegments.append(discord323 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='336' or element=='cs336' or element=='databases' or element=='01:198:336' or element=='198:336' or body3.find("principles of information and database management")!=-1 and '336' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord336 + " ,")
                else:
                    messagesegments.append(discord336 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='344' or element=='cs344' or element=='algo' or element=='01:198:344' or element=='198:344' or body3.find("design and analysis of computer algorithms")!=-1 and '344' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord344 + " ,")
                else:
                    messagesegments.append(discord344 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='440' or element=='cs440' or element=='ai' or element=='01:198:440' or element=='198:440' or body3.find("artificial intelligence")!=-1 and '440' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord440 + " ,")
                else:
                    messagesegments.append(discord440 + " , ")
                additionaldiscord = additionaldiscord + 1
            if element=='416' or element=='cs416' or element=='os' or element=='01:198:416' or element=='198:416' or body3.find("operation systems")!=-1 and '416' not in alreadyreplied:
                doreply=True
                if (additionaldiscord == 0):
                    messagesegments.append(
                        "Based on your post, you should also specifically visit discords (separated by commas and spaces): " + discord416 + " ,")
                else:
                    messagesegments.append(discord416 + " , ")
                additionaldiscord = additionaldiscord + 1


        if doreply==True:

                finalreply=(str)(messagesegments.join())
                submission.reply(finalreply)
                time.sleep(90)








def main():
    loaddata()
    df = pd.DataFrame(
        {'CommentNumber': commentnumber, 'SubmissionLength': lengthofsubmissions, 'TitleLength': lengthoftitle,
         'Rutgers': rutgers, 'Score': score})

    modeltobeused=runmodels(df)
    print(df)
    replypred(modeltobeused)
    csbothelper()


if __name__ == "__main__":
    main()


