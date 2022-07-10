import cv2
import numpy as np
import matplotlib.pyplot as plt#导入需要的库
plt.rcParams['font.sans-serif'] = ['SimHei']  #正确显示中文
cap=cv2.VideoCapture()#读取视频，若括号内的数字为0则代表使用内置摄像头
cap.open("/Users/yy/PycharmProjects/小张的opencv/4.mp4 ")#读取视频路径
frame_w,frame_h=int(cap.get(3)),int(cap.get(4))#获取设置视频的长度和高度
fourcc=cv2.VideoWriter_fourcc("M","J","P","G")#设置编码格式，（‘M’，‘J’，‘P’，'G '）是一个运动jpeg编解码器
out=cv2.VideoWriter("/Users/yy/PycharmProjects/小张的opencv/4.mp4",fourcc,25,(frame_w,frame_h))
ret,frame=cap.read()#获取视频中第一帧图像，并且利用roi自定义指定目标区间
r,h,c,w=120,80,270,30
window=(c,r,w,h)
roi=frame[r:r+h,c:c+w]#设置感兴趣区域
cv2.imshow("1",roi)
cv2.waitKey()
hsv_roi=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)#将图像转换成hsv格式
mask=cv.inrange(hsv_roi,np.arry((0.,60.,32.)),np.arry((180.,255.,255.)))#利用cv2.inrange()函数，在对应的区域内将图像颜色设置为白色
roi_hist=cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)#归一化处理
term_crit=(cv2.TERM_CRITERIA_EPS|cv2.TermCriteria_COUNT,10,1)#窗口最多利用迭代10次，窗口漂移最小值为1
while True:
    ret,frame=cap.read()#获取视频里面每一帧图像
    if ret:
        #开始进行直方图的反向投影
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#转换图像的格式
        dst=cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)#直方图的反向投影操作
        ret,window=cv2.meanShift(dst,window,term_crit)
        x,y,w,h=window#将追踪的位置显示在视频中
        cv2.rectangle(frame,(x,y),(x+w,x+h),(0,255,0),2)#绘制矩形，给定范围，颜色与粗细
        cv2.imshow("frame",frame)#显示最终结果
        out.write(frame)
        cv2.waitKey()
    else:
        break
#释放
cap.release()
out.release()
cv2.destroyAllWindows()