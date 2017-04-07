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
    print url
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
    a=int(raw_input("enter post number for which you want to get the id"))
    insta_user_id=user_by_username(insta_username)
    request_url=Base_Url+'/users/'+insta_user_id+'/media/recent/?access_token='+app_access_token
    print request_url
    recent_posts=requests.get(request_url).json()
    print recent_posts
    print "The post_id is " +str(recent_posts['data'][a]['id'])
    return recent_posts['data'][a]['id']
get_user_post('visheshdhawan')


