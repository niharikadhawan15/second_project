#client_id=db0568c91948473ab1ed24e07dcdcfdf
#access_token=4982415356.db0568c.d88e476700ec4d5caf3cb4649b183ad9

import requests

#access token generated from instagram.com/developer
app_access_token='4982415356.db0568c.d88e476700ec4d5caf3cb4649b183ad9'

#base url for all the requests
Base_Url='https://api.instagram.com/v1'

data=requests.get('https://api.instagram.com/v1/tags/nofilter/media/recent?access_token=4982415356.db0568c.d88e476700ec4d5caf3cb4649b183ad9')
print data.json()

#This function is used to fetch owner's details
def owner_info():
    url=Base_Url+'/users/self/?access_token='+app_access_token
    my_info=requests.get(url).json()
    print "Details of owner:"
    print "Url is :"
    print url
    print "owner's information in json format is:"
    print my_info
    print my_info['data']['website']
    print my_info['data']['bio']
    print my_info['data']['full_name']
owner_info()

#This function is used to get another user Id on which operations such as like,comment are to be performed.
def user_by_username(insta_user):
    url=Base_Url+'/users/search?q='+insta_user+'&access_token='+app_access_token
    my_info=requests.get(url).json()
    if len(my_info['data']):
        print my_info
        print my_info['data'][0]['id']
        return my_info['data'][0]['id']
    else:
         print "No such user"

user_by_username('visheshdhawan')

#This function is used to fetch user/'s public posts
def get_user_post(insta_username):
    insta_user_id=user_by_username(insta_username)
    request_url=Base_Url+'/users/'+insta_user_id+'/media/recent/?access_token='+app_access_token
    recent_posts=requests.get(request_url).json()
    print "number of recent posts : "+ str(len(recent_posts))
    x=raw_input("Do you want the id of recent posts or any of the public post of the user ? \n \nPress y to get the id of recent posts only.\n Press n to get the id of any public post of the user")
    if x=='y'or x=='Y':
        a = int(raw_input("\nenter post number for which you want to get the id\n"))
        if  len(recent_posts)>a>0:
            print recent_posts
            print "The post_id is " + str(recent_posts['data'][a]['id'])
            print "The link of the post is:" + recent_posts['data'][a]['link']
            return recent_posts['data'][a]['id']
        else:
            print "This post is not in the recent posts"
    else :
        x=raw_input("\nEnter y if you want to get user_id with maximum likes\n")
        if x=='y' or x=='Y':
            print recent_posts
            if len(recent_posts['data']):
                a = []
                for i in (range(len(recent_posts['data']))):
                    a.append(recent_posts['data'][i]['likes']['count'])
                    print recent_posts['data'][i]['likes']['count']
                print a
                b = max(a)
                key=a.index(b)
                print "Maximum likes are " + str(b) + " on recent post no." + str(key)
                z=key
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
    print response_to_like
    if response_to_like['meta']['code'] ==200:
         print "Like operation is successful"
    else:
        print "Like operation is unsuccessful"

#like_post_for_user('api_17790')


# This function is declared to comment on user\'s posts.
def comment_user_post(insta_user):
    post_id = get_user_post(insta_user)
    url = Base_Url + "/media/" + str(post_id) + "/comments"
    text = raw_input("Enter the comment that you want to post : ")
    payload = {'access_token': app_access_token, 'text':text }
    response = requests.post(url, payload).json()
    if response['meta']['code'] == 200:
        print("Your comment has been Posted on the particular post_id.")
    else:
        print("The comment operation was unsuccessful")

#comment_user_post('api_17790')

# This function is used to return comment Id that contains a particular word.
def search_word_in_comment(insta_user):
    post_id = get_user_post(insta_user)
    request_url = Base_Url + "/media/" + str(post_id) + "/comments/?access_token=" + app_access_token
    response = requests.get(request_url).json()
    print response
    word = raw_input("Enter the word you want to search in the comments : ")
    #comments=[]
    #comments.append(comments[word])
    #print comments
    for i in response['data']:
        if i in response['data']:
            print "commeni-id is :"
            print response['data'][1]
            return response['data'][1]
    else:
        print "No such comment is there that contains this word."

search_word_in_comment('visheshdhawan')



