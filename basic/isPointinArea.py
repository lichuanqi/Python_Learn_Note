"""
已知多边形区域边界点和某一点坐标，确定此点是否在多边形边界点内

2018-10-07 15:49:37
https://www.cnblogs.com/shld/p/9758303.html
Sheldon (thisisscret@qq.com)
"""

def isinpolygon(point,vertex_lst:list, contain_boundary=True):
    #检测点是否位于区域外接矩形内
    lngaxis, lataxis = zip(*vertex_lst)
    minlng, maxlng = min(lngaxis),max(lngaxis)
    minlat, maxlat = min(lataxis),max(lataxis)
    lng, lat = point
    if contain_boundary:      
        isin = (minlng<=lng<=maxlng) & (minlat<=lat<=maxlat)
    else:
        isin = (minlng<lng<maxlng) & (minlat<lat<maxlat)
    return isin

def isintersect(poi,spoi,epoi):
    #输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    #射线为向东的纬线
    #可能存在的bug，当区域横跨本初子午线或180度经线的时候可能有问题
    lng, lat = poi
    slng, slat = spoi
    elng, elat = epoi
    if poi == spoi:
        #print("在顶点上")
        return None
    if slat==elat: #排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if slat>lat and elat>lat: #线段在射线上边
        return False
    if slat<lat and elat<lat: #线段在射线下边
        return False
    if slat==lat and elat>lat: #交点为下端点，对应spoint
        return False
    if elat==lat and slat>lat: #交点为下端点，对应epoint
        return False
    if slng<lng and elat<lat: #线段在射线左边
        return False
    #求交点
    xseg=elng-(elng-slng)*(elat-lat)/(elat-slat)
    if xseg == lng:
        #print("点在多边形的边上")
        return None
    if xseg<lng: #交点在射线起点的左侧
        return False
    return True  #排除上述情况之后

def isin_multipolygon(poi,vertex_lst, contain_boundary=True): 
    # 判断是否在外包矩形内，如果不在，直接返回false    
    if not isinpolygon(poi, vertex_lst, contain_boundary):
        return False
    sinsc = 0
    for spoi, epoi in zip(vertex_lst[:-1],vertex_lst[1::]):
        intersect = isintersect(poi, spoi, epoi)
        if intersect is None:
            return (False, True)[contain_boundary]
        elif intersect:
            sinsc+=1
            
    return sinsc%2==1


if __name__ == '__main__':
    
    fence = [[
            "116.324286",
            "40.076495"
        ],
        [
            "116.370243",
            "40.076198"
        ],
        [
            "116.375076",
            "40.075867"
        ],
        [
            "116.380484",
            "40.074218"
        ],
        [
            "116.380412",
            "40.074011"
        ],
        [
            "116.381131",
            "40.073196"
        ],
        [
            "116.381544",
            "40.072368"
        ],
        [
            "116.384904",
            "40.072686"
        ],
        [
            "116.392988",
            "40.069649"
        ],
        [
            "116.407218",
            "40.063575"
        ],
        [
            "116.411529",
            "40.061808"
        ],
        [
            "116.411314",
            "40.057445"
        ],
        [
            "116.410020",
            "40.057362"
        ],
        [
            "116.408799",
            "40.057003"
        ],
        [
            "116.408367",
            "40.056976"
        ],
        [
            "116.408367",
            "40.055706"
        ],
        [
            "116.405277",
            "40.055678"
        ],
        [
            "116.405241",
            "40.056562"
        ],
        [
            "116.403732",
            "40.056313"
        ],
        [
            "116.402079",
            "40.053469"
        ],
        [
            "116.401073",
            "40.051260"
        ],
        [
            "116.398055",
            "40.049824"
        ],
        [
            "116.394174",
            "40.048277"
        ],
        [
            "116.390365",
            "40.047421"
        ],
        [
            "116.382263",
            "40.044073"
        ],
        [
            "116.381598",
            "40.045895"
        ],
        [
            "116.380700",
            "40.047836"
        ],
        [
            "116.380664",
            "40.048250"
        ],
        [
            "116.380233",
            "40.048526"
        ],
        [
            "116.379909",
            "40.049382"
        ],
        [
            "116.379658",
            "40.050072"
        ],
        [
            "116.379514",
            "40.050293"
        ],
        [
            "116.376100",
            "40.051591"
        ],
        [
            "116.374412",
            "40.052806"
        ],
        [
            "116.373549",
            "40.054408"
        ],
        [
            "116.372256",
            "40.057335"
        ],
        [
            "116.363632",
            "40.054739"
        ],
        [
            "116.343294",
            "40.051646"
        ]
        ]
    
    vertex_lst = []
    for i in range(len(fence)):
        vertex_lst.append([float(fence[i][0]), float(fence[i][1])])

    # poi = [116.369623,40.080121]
    poi = [116.345620,40.064265]
    print(isin_multipolygon(poi,vertex_lst, contain_boundary=True))