import sys
sys.path.append('project/chatbot_wenxin')

from api import ACCESS_TIME, ACCESS_TOKEN
from api import get_access_token, update_access_token


access_time, access_token = update_access_token(ACCESS_TIME, ACCESS_TOKEN)
# print(access_time, access_token)