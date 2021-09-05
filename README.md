
# Python note

Python学习笔记


# 文件结构

```
├── camera                    # 读取摄像机rtsp码流并显示
├── mardown                   # markdown语法
├── basic                     # 基础代码
│   ├── array_save_load.py    # 列表的保存和读取
│   ├── csv_read_write.py     # CSV文件的保存和读取
│   ├── get_filename.py       # 读取文件夹内的名
│   ├── test_sympy.py
│   ├── txt_read.py            
│   └── txt_write.py
├── cv2                       # opencv-python
│   ├── read_and_show.py      # 图像的读写和展示
│   ├── huidu.py
│   ├── erzhihua.py
│   ├── pinghua_quzao.py      # 加噪
│   ├── pinghua_jiazao.py     # 去噪
│   ├── bianyuan.py           # 边缘检测
│   ├── bijiao_tupian.py      # 比较图片
│   ├── color_convert.py      # 颜色模式的转换
│   ├── candidate_area.py
│   ├── contour_draw.py
│   ├── get_iou.py
│   ├── gray_projection.py    # 像素值灰度投影
│   ├── img_add_text.py       # 图片添加文本信息
│   ├── img_labled.py         # 图像添加矩形框
│   ├── logic_operation.py    # 逻辑运算
│   └── resize_image.py       # 尺寸修改
├── numpy
│   ├── basic.py
│   ├── distance_point.py
│   ├── distance_tracker.py   
│   ├── leastSquare.py        # 最小二乘法线性拟合
│   └── qiujunzhi.py
├── pyplot
│   ├── 3d.py
│   ├── density_map.py
│   ├── plot_01.py
│   ├── plot_02.py
│   ├── scienceplot.py
│   └── set_font.py
├── port                      # 端口相关
├── preprocessing             # 预处理
├── signal                    # 信号相关
│   ├── data_fit.py           # 数据拟合                  
│   └── SG.py                 # SG平滑
├── test                       
│   ├── test_jit.py
│   └── vpi.py
└── tools                     # 小工具
    ├── create_gif.py         # 图片转动图
    └── video_to_image.py     # 视频转图片
```

# Requirments

```
opencv-python
numpy
...
```