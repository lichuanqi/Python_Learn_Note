import json
import yaml
import base64
import requests

import cv2


def read_yaml(yaml_path='config.yaml'):
    """
    读取yaml文件
    """
    with open(yaml_path, 'rb') as f:
        cfg = yaml.load(f.read(), Loader=yaml.FullLoader)

    return cfg


def fetch_token(API_KEY, SECRET_KEY):
    """
    鉴权获取token
    """
    host = host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
    response = requests.get(host)

    try:
        return response.json()['access_token']
    except:
        return 'ERR'

def object_detect(token, img_path=None, img_data=None):
    """
    图像主体检测
    """
        
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect"
    if img_path is not None:
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read())
    elif img_data is not None:
        img = img_data

    params = {"image":img,"with_face":1}
    request_url = url + "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    
    return response.json()['result']


if __name__ == '__main__':

    cfg = read_yaml()
    API_KEY = cfg['api']['bd_img']['API_KEY']
    SECRET_KEY = cfg['api']['bd_img']['SECRET_KEY']
    token = fetch_token(API_KEY, SECRET_KEY)
    print(f'toben: {token}')

    img_path = 'D:/Data/Expressbox/1.jpg'
    img = cv2.imread(img_path)
    img = cv2.resize(img,None,fx=0.2,fy=0.2)

    # cv2 -> base64
    img_base64 = cv2.imencode('.jpg',img)[1].tobytes()
    img_base64 = base64.b64encode(img_base64)

    res = object_detect(token, img_data=img_base64)
    print(f'res: {res}')

    x1, y1 = res['left'], res['top']
    x2, y2 = (res['left'] + res['width']), (res['top'] + res['height'])

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow('img', img)

    cv2.waitKey(0)



