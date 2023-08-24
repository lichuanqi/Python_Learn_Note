from pathlib import Path
import cv2
from pyzbar import pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol
import pandas as pd 


def barcode_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    texts = pyzbar.decode(gray)

    if len(texts) > 0:
        for text in texts:
            tt = text.data.decode("utf-8")
    else:
        tt = 'None'

    return tt


def main():
    dir_path = "D:/DATASET/Miandan-0824"
    extensions = ['jpg', 'jpeg']
    save_name = 'D:/DATASET/Miandan-0824/001.txt'

    df = pd.DataFrame(columns=['dir_name', 'file_name', 'barcode'])

    image_paths = []
    for extension in extensions:
        image_paths.extend(Path(dir_path).glob('*/*.%s'%extension))

    for path in image_paths:
        parent = path.parent.name
        name = path.name
        path_str = str(path)

        # 识别条形码
        result = barcode_image(path_str)

        # 保存到数据结构
        df = df.append({
            'dir_name': dir_path, 
            'file_name': '', 
            'barcode': result}, ignore_index=True)

        print('%s, %s: %s'%(parent, name, result))

    # 保存为csv文件
    df.to_csv(save_name, index=False)
    

def test_barcode_image():
    image_path = "D:/DATASET/Miandan500/a.jpg"
    result = barcode_image(image_path)
    print(result)


if __name__ == '__main__':
    # test_barcode_image()
    main()