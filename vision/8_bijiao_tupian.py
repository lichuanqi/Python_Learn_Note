from skimage import measure, io, metrics

img_2_list = [r'E:\model\data\origin_add_np_0.1.jpg',
              r'E:\model\data\300_gaussian.jpg',
              r'E:\model\data\300_mean.jpg',
              r'E:\model\data\300_median.jpg',
              r'E:\model\data\300_shuangbian.jpg']
img_1 = io.imread(r'E:\model\data\300.jpg')


def bijiao(img_1,img_2):
    psnr = metrics.peak_signal_noise_ratio(img_1, img_2)
    mse = metrics.mean_squared_error(img_1, img_2)
    ssim = metrics.structural_similarity(img_1, img_2,multichannel=True)
    print(float('%.2f' % psnr))
    print(float('%.2f' % mse))
    print(float('%.2f' % ssim))
    print('\n')


for img in img_2_list:
    print(img)
    img = io.imread(img)
    bijiao(img_1, img)
