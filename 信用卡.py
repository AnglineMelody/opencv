import cv2
import numpy as np
from imutils import contours
import myutils
#首先引用本次操作需要的库
#定义一个img_函数，其实三将每次需要显示图片操作简化
def img_(img, name):
    cv2.imshow('name', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
img=cv2.imread("/Users/yy/PycharmProjects/小张的opencv/a2.jpg")#读取图片
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#转换为灰度图片
ret,img_2=cv2.threshold( img_gray,10, 255, cv2.THRESH_BINARY_INV)#阈值处理
refCnts,hierarchy=cv2.findContours(img_2.copy(),cv2.RETR_EXTERNA,cv2.CHAIN_APPROX_SIMPLEL)
#绘制图片轮廓.cv2.RETR_EXTERNAL只检测外轮廓， cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
len(contours)#计算轮廓个数
cv2.drawContours(img,refCnts,-1,(0,0,255),3)#绘制轮廓
''' 给的模版不一定就是按照0-9的顺序排列的，所以定义一个sort_conturs函数去保证轮廓是按照0-9排列的'''
def sort_contours(cnts,method="left-to-right"):
    reverse=False
    i=0
    if method=="right-to-left"or  method=="bottom-to-top":
        reverse=True
    if method=="top-to-bottom" or method =="bottom-to-top":
        i=1
    boundingBoxes=[cv2.boundingRect(c) for c in cnts]
    '''这里使用了cv2.boundingRects,是为用一个最小矩形，把找到的包起来'''
    (cnts,boundingBoxes)=zip(*sorted(zip(cnts,boundingBoxes),key=lambda b:b[1][i],reverse=reverse))
'''zip(*zip(a,b)代表将压缩后的元祖解压，key=lambda b:b[1][i] b只是一个变量名，可以是任何一个变量，b[1][i]指按第二元素中的第i个元素就行排序也就是按boundingBoxes中的第i个元素进行排序；reverse是反转，'''
    return cnts, boundingBoxes
refCnts = myutils.sort_contours(refCnts, method="left-to-right")[0]
digit2cnt={}
for i,c in enumerate(refCnts):#遍历每一个轮廓，
# enumerate()是python的内置函数enumerate在字典上是枚举、列举的意思对于一个可迭代的（iterable）/可遍历的对象（如列表、字符串）
    (x,y,w,h)=cv2.boundingRect(c)
    roi=template[y:y+h,x:x+w]
    roi=cv2.resize(roi,(57,88))#利用resize重新制定大小
    dihits2Cnt[i]=roi
#自定义需要的卷积核
ntKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
ffKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#处理信用卡照片，利用resize改变图像大小，并且将图片变成灰度图像
a1 = cv2.imread("/Users/yy/PycharmProjects/小张的opencv/a1.jpg")
a1 = myutils.resize(a1, width=300)
a1_gray = cv2.cvtColor(a1, cv2.COLOR_BGR2GRAY)
#进行顶帽操作，突出明亮区域
a1_tophat=cv2.morphologyEx(a1_gray,cv2.MORPH_TOPHAT,ntKernel)
#进行边缘操作，把图像边缘突出出来
gradx=cv2.Sobel(a1_tophat,ddepth=cv2.CV_32F,dx=1,dy=0,ksize=-1)
gradx=np.absolute(gradx)
minVal,maxVal=np.min(gradx),np.max(gradx)
gradx=255*(gradx-minVal)/(maxVal-minVal)
gradX = gradX.astype('uint8')
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, ntKernel)
thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# 再执行一个闭操作，白色填充黑色区域
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, ffKernel)
#查找轮廓，绘制轮廓，-1代表绘制所有轮廓
threshCnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = threshCnts
cur_img = a1.copy()
cv2.drawContours(cur_img, cnts, -1, (0, 0, 255), 3)
'''将本次程序需要得到的轮廓添加到自定义的列表里面'''
locs=[]
for i ,c in enumerate(cnts):
    (x,y,w,h)=cv2.boundingRect(c)#计算矩形
    ar=w/float(h)
    '''通过长宽高的要求，把符合条件的添加近列表里面'''
    if 2.5<ar<4.0:
        if(40<2<55)and(10<h<20):
            LOCS.APPEND((x,y,w,h))
locs=sorted(locs,key=lambda x:x[0])#将得到的轮廓从左到右进行排序
#遍历得到每一个轮廓中的数字，然后将信用卡中的图像与模版中的数字进行匹配
for (i,(gx,gy,gw,gh)) in enumerate(locs):
    group_out=[]#定义一个空列表
    group_out=a1_gray[gy-5:gy+gh+5,gx-5:gx+gw+5]#根据坐标一组一组去提取
    group=cv2.threshold(group,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)#图像进行二值化处理并且自定义阈值处理
    digitCnts,hierarchy=cv2.findContours(group.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#检测到轮廓
    digitCnts=contours.sort_contours(digitCnts,method="left to right")[0]#将轮廓进行排序
    for c in digitCnts:
        (x,y,w,h)=cv2.boundingRect(c)#得到每一组轮廓中的数字并且进行模版匹配
        roi=group[y:y+h,x:x+w]
        roi=cv2.resize(roi,(57,88))#利用resize将轮廓调整成合适大小
        scores=[]#定义空列表
        #进行模版匹配
        for (digit,digitROI)in digit2cnt.items():
            result=cv2.matchTemplate(roi,digitROI,cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            #将每次识别得到的数字结果储存到列表里
            scores.append(score)
            groupOutput.append(str(np.argmax(scores)))
            cv2.rectangle(a1, (gX - 5, gY - 5), (gX + gW + 5, gY + gH + 5), (0, 0, 255), 1)#cv2.redtangle是绘制矩形的函数，参数代表的是长方形左上角坐标和右下角坐标，字体颜色，和笔的粗细
            cv2.putText(a1, "".join(groupOutput), (gX, gY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255),2)
            outputs.extend(groupOutput)
img_(a1,"a1")#显示图像