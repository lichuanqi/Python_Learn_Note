import numpy as np
import pymysql


class database():
    """链接数据库，插入检测数据
    
    """
    def __init__(self) -> None:

        self.connect()

    def connect(self):
        """连接数据库"""
        self.db = pymysql.connect(host='192.168.35.221',
            port=3306,
            user='root',
            password='123456',
            database='test')

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()


    def create(self):
        """判断数据库中是否有表，没有的话新建一个"""

        sql = """CREATE TABLE IF NOT EXISTS `camera_info`(
            `camera_id` INT AUTO_INCREMENT comment '摄像头id',
            `camera_sn` VARCHAR(10) NULL comment '摄像头生产序列号',
            `camera_rtsp` VARCHAR(15) NULL comment '摄像头rtsp地址',
            `camera_office` VARCHAR(8) NULL comment '摄像头所在机构',
            `camera_location` VARCHAR(8) NULL comment '摄像头位置',
            `insert_times` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP() comment '插库时间',
            PRIMARY KEY (camera_id));
        """
        r1 = self.cursor.execute(sql)


        sql = """CREATE TABLE IF NOT EXISTS `device_details`(
            `details_id` INT AUTO_INCREMENT comment 'id',
            `camera_id` INT comment '摄像头id',
            `camera_status` VARCHAR(8) not NULL comment '摄像头状态',
            `insert_times` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP() comment '插库时间',
            FOREIGN KEY (camera_id) REFERENCES camera_info(camera_id),
            PRIMARY KEY (details_id));
        """
        r2 = self.cursor.execute(sql)

        return f'创建日志详细表成功: {r1}, {r2}'


    def insert_camera_info(self, camera_sn, 
            camera_rtsp, camera_office, camera_location):
        """设备表的数据插入"""

        sql = """INSERT INTO `camera_info`(camera_sn, 
                    camera_rtsp, camera_office, camera_location)
                VALUES(%s, %s, %s, %s);
        """

        try:
            self.cursor.execute(sql, (camera_sn, 
                    camera_rtsp, camera_office, camera_location))
            log_id = self.cursor.lastrowid
            self.db.commit()

            return True, log_id

        except Exception as f:
            self.db.rollback()
            
            return False, f


    def insert_device_details(self, camera_id, camera_status):
        """详细表的数据插入"""
        
        sql = """INSERT INTO `device_details`(camera_id, camera_status)
                 VALUES(%s, %s);
        """

        try:
            self.cursor.execute(sql, (camera_id, camera_status))
            log_id = self.cursor.lastrowid
            self.db.commit()

            return True, log_id

        except Exception as f:
            self.db.rollback()
            
            return False, f


if __name__ == '__main__':

    db = database()

    # 创建表
    result = db.create()
    print(result)
    
    # 主表插入数据
    camera_sn = '1000002'
    camera_rtsp = '192.168.35.222'
    camera_office = '大平面2'
    camera_location = '东南角'

    status, device_id = db.insert_camera_info(camera_sn, 
            camera_rtsp, camera_office, camera_location)
    print(status, device_id)
    if status:
        print(f'数据已插入, camera_id:{camera_sn} -> id:{camera_sn}')

    # 子表循环插入数据
    for i in range(10):
        
        camera_status_list = ['正常', '异常']
        camera_status = camera_status_list[np.random.randint(0,2)]

        status_, log_id_ = db.insert_device_details(device_id, camera_status)
        print(status_, log_id_)
        if status:
            print(f'数据已插入, status_:{camera_status} -> id:{log_id_}')