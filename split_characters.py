from cv2 import cv2
import numpy as np
from PIL import Image, ImageEnhance
 
'''水平投影'''
def getHProjection(image):
    hProjection = np.zeros(image.shape,np.uint8)
    #图像高与宽
    (h,w)=image.shape
    #长度与图像高度一致的数组
    h_ = [0]*h
    #循环统计每一行白色像素的个数
    for y in range(h):
        for x in range(w):
            if image[y,x] == 255:
                h_[y]+=1
    #绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y,x] = 255
    #cv2.imshow('hProjection2',hProjection)
 
    return h_
 
def getVProjection(image):
    vProjection = np.zeros(image.shape,np.uint8)
    #图像高与宽
    (h,w) = image.shape
    #长度与图像宽度一致的数组
    w_ = [0]*w
    #循环统计每一列白色像素的个数
    for x in range(w):
        for y in range(h):
            if image[y,x] == 255:
                w_[x]+=1
    #绘制垂直平投影图像
    for x in range(w):
        for y in range(h-w_[x],h):
            vProjection[y,x] = 255
    #cv2.imshow('vProjection',vProjection)
    return w_

def resize_keep_aspectratio(image_src,dst_size):
    src_h,src_w = image_src.shape[:2]
    #print(src_h,src_w)
    dst_h,dst_w = dst_size 
   
    #判断应该按哪个边做等比缩放
    h = dst_w * (float(src_h)/src_w)#按照ｗ做等比缩放
    w = dst_h * (float(src_w)/src_h)#按照h做等比缩放
   
    h = int(h)
    w = int(w)
   
    if h <= dst_h:
        image_dst = cv2.resize(image_src,(dst_w,int(h)))
    else:
        image_dst = cv2.resize(image_src,(int(w),dst_h))
   
    h_,w_ = image_dst.shape[:2]
    #print(h_,w_)
   
    top = int(((dst_h - h_) / 2)+10)
    down = int(((dst_h - h_+1) / 2)+10)
    left = int(((dst_w - w_) / 2)+10)
    right = int(((dst_w - w_+1) / 2)+10)
   
    value = [255,255,255]
    borderType = cv2.BORDER_CONSTANT
    #print(top, down, left, right)
    image_dst = cv2.copyMakeBorder(image_dst, top, down, left, right, borderType, None, value)
    
    return image_dst

def inverse_color(image):

    height,width,temp = image.shape
    img2 = image.copy()

    for i in range(height):
        for j in range(width):
            img2[i,j] = (255-image[i,j][0],255-image[i,j][1],255-image[i,j][2]) 
    return img2

def enhance(image):
    img = image.convert('L')
    #enhancer = ImageEnhance.Brightness(image)
    #img = enhancer.enhance(16)
    threshold = 96
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # convert to binary image by the table
    img = img.point(table, '1' )
    return img
 
def Spliting(Path):
    #读入原始图像
    origineImage = cv2.imread(Path)
    # 图像灰度化   
    #image = cv2.imread('test.jpg',0)
    image = cv2.cvtColor(origineImage,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',image)
    # 将图片二值化
    retval, img = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('binary',img)
    #图像高与宽
    (h,w)=img.shape
    Position = []
    #水平投影
    H = getHProjection(img)
 
    start = 0
    H_Start = []
    H_End = []
    #根据水平投影获取垂直分割位置
    for i in range(len(H)):
        if H[i] > 0 and start ==0:
            H_Start.append(i)
            start = 1
        if H[i] <= 0 and start == 1:
            H_End.append(i)
            start = 0
    #分割行，分割之后再进行列分割并保存分割位置
    for i in range(len(H_Start)):
        #获取行图像
        cropImg = img[H_Start[i]:H_End[i], 0:w]
        #cv2.imshow('cropImg',cropImg)
        #对行图像进行垂直投影
        W = getVProjection(cropImg)
        Wstart = 0
        Wend = 0
        W_Start = 0
        W_End = 0
        for j in range(len(W)):
            if W[j] > 0 and Wstart ==0:
                W_Start =j
                Wstart = 1
                Wend=0
            if W[j] <= 0 and Wstart == 1:
                W_End =j
                Wstart = 0
                Wend=1
            if Wend == 1:
                Position.append([W_Start,H_Start[i],W_End,H_End[i]])
                Wend =0
    #根据确定的位置分割字符
    num = 0
    for m in range(len(Position)):
        num = num + 1
        a = Position[m][0]
        b = Position[m][1]
        c = Position[m][2]
        d = Position[m][3]
        cropped = origineImage[b:d, a:c]  # 裁剪坐标为[y0:y1, x0:x1]
        dst_size = (128,128)
        image = resize_keep_aspectratio(cropped,dst_size)
        image = inverse_color(image)
        cv2.imwrite("./temp/{}.jpg".format(num), image)
        img = Image.open("./temp/{}.jpg".format(num))
        img = enhance(img)
        imagefile = "./temp/{}.jpg".format(num)
        img.save(imagefile)
    #     cv2.rectangle(origineImage, (Position[m][0],Position[m][1]), (Position[m][2],Position[m][3]), (0 ,229 ,238), 1)
    # cv2.imshow('image',origineImage)
    # cv2.waitKey(0)

if __name__ == '__main__':
    path = 'test.png'
    Spliting(path)