from Imports import *
from utils import *
from DownSampling import *

path = 'D:\semestre9\gp\Dataset'
try:
    os.makedirs("D:\semestre9\gp\Dataset_LowQuality")
except:
    shutil.rmtree("D:\semestre9\gp\Dataset_LowQuality")
    os.makedirs("D:\semestre9\gp\Dataset_LowQuality")

PathOfLowQuality = 'D:\semestre9\gp\Dataset_LowQuality'
h = gkern(13, 1.6)  # 13 and 1.6 for x4

files = os.listdir(path)
for i in range(len(files)):
    os.makedirs(PathOfLowQuality + "\\" + files[i])
    VideoFile = os.listdir(path + "\\" + files[i])
    for j in range(len(VideoFile)):
        os.makedirs(PathOfLowQuality + "\\" + files[i] + "\\" + VideoFile[j])
        images = os.listdir(path + "\\" + files[i] + "\\" + VideoFile[j])
        for l in range(len(images)):
            #Giving assumption that the last frame would have the same portion of motion as his before frame
            if l == len(images)-1:
                image = io.imread(path + "\\" + files[i] + "\\" + VideoFile[j] + '\\' + images[l])
                AfterGaussian_0 = convolve2D(image[i_pixel:i_pixel + 144, j_pixel:j_pixel + 144, 0], h)
                AfterGaussian_1 = convolve2D(image[i_pixel:i_pixel + 144, j_pixel:j_pixel + 144, 1], h)
                AfterGaussian_2 = convolve2D(image[i_pixel:i_pixel + 144, j_pixel:j_pixel + 144, 2], h)

                newimage = np.zeros((144, 144, 3), dtype="uint8")

                newimage[..., 0] = AfterGaussian_0
                newimage[..., 1] = AfterGaussian_1
                newimage[..., 2] = AfterGaussian_2

                newimage = quarter_res_avg(newimage)
                # x = LoadImage(path + "\\" + files[i] + "\\" + VideoFile[j] + '\\' + images[l])
                cv2.imwrite(PathOfLowQuality + "\\" + files[i] + "\\" + VideoFile[j] + '\\' + images[l], cv2.cvtColor(newimage, cv2.COLOR_RGB2BGR))
            else:
                image = io.imread(path + "\\" + files[i] + "\\" + VideoFile[j] + '\\' + images[l])
                image_next = io.imread(path + "\\" + files[i] + "\\" + VideoFile[j] + '\\' + images[l+1])
                #####################Motion Detection########################
                mag_matrix = getMotionMatrix(image, image_next)
                i_pixel, j_pixel = get144OfMostMotion(mag_matrix)

                AfterGaussian_0 = convolve2D(image[i_pixel:i_pixel + 144, j_pixel:j_pixel + 144, 0], h)
                AfterGaussian_1 = convolve2D(image[i_pixel:i_pixel + 144, j_pixel:j_pixel + 144, 1], h)
                AfterGaussian_2 = convolve2D(image[i_pixel:i_pixel + 144, j_pixel:j_pixel + 144, 2], h)

                newimage = np.zeros((144, 144, 3), dtype="uint8")

                newimage[..., 0] = AfterGaussian_0
                newimage[..., 1] = AfterGaussian_1
                newimage[..., 2] = AfterGaussian_2

                newimage = quarter_res_avg(newimage)
                # x = LoadImage(path + "\\" + files[i] + "\\" + VideoFile[j] + '\\' + images[l])
                cv2.imwrite(PathOfLowQuality + "\\" + files[i] + "\\" + VideoFile[j] + '\\' + images[l], cv2.cvtColor(newimage, cv2.COLOR_RGB2BGR))

