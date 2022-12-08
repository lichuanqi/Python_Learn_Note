import numpy as np
from sklearn.neighbors import NearestNeighbors


def find_nearest_k(data, point, k):
    """查找距离据点的K个点
    
    Params
        data   : 训练集
        point  : 要查找的点
        k      :
    
    Returm
        distances  : 与最近点的最小距离
        indices    : 最近点在训练集中的索引
    """
    neigh = NearestNeighbors(n_neighbors=k,algorithm='ball_tree')
    nbrs = neigh.fit(data)
    distances, indices = nbrs.kneighbors(point)

    print(distances)
    print(indices)


if __name__ == '__main__':
    data = np.array([[0,0], [1,2], [2,3], [8,8]])
    point = np.array([[1,1]])

    find_nearest_k(data, point, 1)