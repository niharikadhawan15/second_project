
#client_id=db0568c91948473ab1ed24e07dcdcfdf
#access_token=4982415356.db0568c.d88e476700ec4d5caf3cb4649b183ad9

import requests

#access token generated from instagram.com/developer
app_access_token='4982415356.db0568c.d88e476700ec4d5caf3cb4649b183ad9'

#base url for all the requests
Base_Url='https://api.instagram.com/v1'

data=requests.get('https://api.instagram.com/v1/tags/nofilter/media/recent?access_token=4982415356.db0568c.d88e476700ec4d5caf3cb4649b183ad9')
print "JSON data of the owner is ",data.json()

#This function is used to fetch owner's details
def owner_info():
    url=Base_Url+'/users/self/?access_token='+app_access_token
    my_info=requests.get(url).json()
    print "\nDetails of owner:"
    print "\nUrl is :"
    print url
    print "\nowner's information in json format is:"
    print my_info
    print "\nUsername is  : ", my_info['data']['username']
    print "\nName of the user is :",my_info['data']['full_name']
    print "\nThe link to profile picture is : ", my_info['data']['profile_picture']
    print "\nThe owner is followed By : ", my_info['data']['counts']['followed_by']
    print "\nThe followers of the owner are : ", my_info['data']['counts']['follows']



#This function is used to get another user Id on which operations such as like,comment are to be performed.
def user_by_username(insta_user):
    url=Base_Url+'/users/search?q='+insta_user+'&access_token='+app_access_token
    my_info=requests.get(url).json()
    if len(my_info['data']):
        print "The user id is :\n"
        print my_info
        print my_info['data'][0]['id']
        return my_info['data'][0]['id']
    else:
         print "No such user"



#This function is used to fetch user/'s public posts
def get_user_post(insta_username):
    insta_user_id=user_by_username(insta_username)
    request_url=Base_Url+'/users/'+insta_user_id+'/media/recent/?access_token='+app_access_token
    recent_posts=requests.get(request_url).json()
    print "\nNumber of recent posts : "+ str(len(recent_posts))
    x=raw_input("\nDo you want the id of recent posts or any of the public post of the user ? \nPress y to get the id of recent posts only.\nPress n to get the id of interesting posts.")
    if x=='y'or x=='Y':
        a = int(raw_input("\nenter post number for which you want to get the id\n"))
        if  len(recent_posts)>a>=0:
            print recent_posts
            print "The post_id is " + str(recent_posts['data'][a]['id'])
            print "The link of the post is:" + recent_posts['data'][a]['link']
            return recent_posts['data'][a]['id']
        else:
            print "This post is not in the recent posts....You will be getting the defaul id"
            return recent_posts['data'][0]['id']
    else :
        x=raw_input("\nEnter y if you want to get user_id with maximum likes\nEnter n if you want id with maximum comment")
        if x=='y' or x=='Y':
            print recent_posts
            if len(recent_posts['data']):
                a = []
                for i in (range(len(recent_posts['data']))):
                    a.append(recent_posts['data'][i]['likes']['count'])
                    print "\nThe numbers of like on posts are"
                    print recent_posts['data'][i]['likes']['count']
                print a
                b = max(a)
                key=a.index(b)
                print "\nMaximum likes are " + str(b) + " on recent post no." + str(key)
                z=key
                return recent_posts['data'][z]['id']
        elif x=='n' or x=='Y':
            print recent_posts
            if len(recent_posts['data']):
                a = []
                for i in (range(len(recent_posts['data']))):
                    a.append(recent_posts['data'][i]['comments']['count'])
                    print "\nThe numbers of like on posts are"
                    print recent_posts['data'][i]['comments']['count']
                print a
                b = max(a)
                key = a.index(b)
                print "\nMaximum comments are " + str(b) + " on recent post no." + str(key)
                z = key
                return recent_posts['data'][z]['id']

        else:
            return recent_posts['data'][0]['id']


#This function is declared to like a post.
def like_post_for_user(insta_username):
    post_id= get_user_post(insta_username)
    print post_id
    payload={"aceess_token":app_access_token}
    request_url=Base_Url+"/media/"+str(post_id)+"/likes/?access_token="+app_access_token
    response_to_like=requests.post(request_url).json()
    print response_to_like['meta']['code']
    print "\n The response to like is\n"
    print response_to_like
    if response_to_like['meta']['code'] ==200:
         print "Like operation is successful"
    else:
        print "Like operation is unsuccessful"




# This function is declared to comment on user\'s posts.
def comment_user_post(insta_user):
    post_id = get_user_post(insta_user)
    url = Base_Url + "/media/" + str(post_id) + "/comments"
    text = raw_input("Enter the comment that you want to post : ")
    payload = {'access_token': app_access_token, 'text':text }
    response = requests.post(url, payload).json()
    if response['meta']['code'] == 200:
        print "Your comment has been Posted on the particular post_id."
    else:
        print "The comment operation was unsuccessful"



# This function is used to return comment Id that contains a particular word.
def search_word_in_comment(insta_user):
    post_id = get_user_post(insta_user)
    request_url = Base_Url + "/media/" + str(post_id) + "/comments/?access_token=" + app_access_token
    response = requests.get(request_url).json()
    print response
    word = raw_input ("\nEnter the word you want to search in the comments : ")
    comments = []
    comments_id = []
    for a in response['data']:
        comments.append(a['text'])
        comments_id.append(a['id'])
    comments_found = []
    comments_id_found = []
    for i in range(len(comments)):
        if word in comments[i]:
            comments_found.append(comments[i])
            comments_id_found.append(comments_id[i])
    if len(comments_found) == 0:
        print "There is no such comment"
    else:
        return comments_id_found,post_id


#search_word_in_comment('visheshdhawan')
def delete_comment(insta_user):
    comments_id_found,post_id=search_word_in_comment(insta_user)
    print post_id
    for i in range(len(comments_id_found)):
        url = Base_Url + "/media/" + str(post_id) + "/comments/" + str(
        comments_id_found[i]) + "/?access_token=" + app_access_token
        comments_response = requests.delete(url).json()
        print comments_response
        if comments_response['meta']['code'] == 200:
            print "Comment deleted successfully"
        else:
            print "The delete comment operation unsuccessful"


# This function prints the average number of words per comment
def average_words(ipost_id):
    print post_id
    request_url = Base_Url + "/media/" + str(post_id) + "/comments/?access_token=" + app_access_token
    response = requests.get(request_url).json()
    if len(response['data']) == 0:
        print("There are no comments on this post")
    else:
        total=0
        comments=[]
        for comment in response['data']:
          comments.append(comment['text'])
          total += len(comment['text'].split())
        average = float(total) / len(comments)
        print "Average no. of words per comment in the post is :",average

#post_id = get_user_post(insta_user)

a=raw_input("Select the user_name for which you want to perform operations such as like and comment\nEnter 1 for api_17790\nEnter 2 for visheshdhawan")
if a=='1':
    insta_user='api_17790'
    b=raw_input("\nselect the operation you want to perform\nEnter 1 to get owner_info\nEnter 2 for user_detail\nEnter 3 for getting user_post_id\nEnter 4 for like\nEnter 5 for comment\nEnter 6 to search word in comment\nEnter 7 for delete.\nEnter 8 to find the average words")
    if b=='1':
        owner_info()
    elif b=='2':
        user_by_username(insta_user)
    elif b=='3':
        get_user_post(insta_user)
    elif b=='4':
        like_post_for_user(insta_user)
    elif b=='5':
        comment_user_post(insta_user)
    elif b=='6':
        search_word_in_comment(insta_user)
    elif b=='7':
        delete_comment(insta_user)
    elif b=='8':
        post_id = get_user_post(insta_user)
        average_words(post_id)
    else:
        print "wrong choice \nExit"
elif a=='2':
    insta_user='visheshdhawan'
    b = raw_input( "\nselect the operation you want to perform\nEnter 1 to get owner_info\nEnter 2 for user_detail\nEnter 3 for getting user_post_id\nEnter 4 for like\nEnter 5 for comment\nEnter 6 to search word in comment\nEnter 7 for delete.\nEnter 8 to find the average words")
    if b == '1':
        owner_info()
    elif b == '2':
        user_by_username(insta_user)
    elif b == '3':
        get_user_post(insta_user)
    elif b == '4':
        like_post_for_user(insta_user)
    elif b == '5':
        comment_user_post(insta_user)
    elif b == '6':
        search_word_in_comment(insta_user)
    elif b == '7':
        delete_comment(insta_user)
    elif b == '8':
        post_id = get_user_post(insta_user)
        average_words(post_id)
    else:
        print "wrong choice \nExit"
else:
    print "wrong choice\nExit"