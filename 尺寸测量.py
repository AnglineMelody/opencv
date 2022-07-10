#引用库函数
import cv2
from scipy.spatial import distance as dist
from imutils import contours
import imutils#图像操作函数
import math
import Preprocess.preprocess as pp
import numpy as np
import argparse
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)#读取视频，设置好参数
count = 1
modhi=2
while True:
    _,image=cap.read()
    #引用argparse创建对象参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--width", required=True,
        help="width of the left most (standard) object")
    args = vars(ap.parse_args())
    #获取宽度
    width = float(args["width"])
    edged = pp.init(image)
    contour = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contour)
    (cnts, _) = contours.sort_contours(cnts)
    for c in cnts:
        #使用条件语句去除一些噪音
        if cv2.contourArea(c) < 2000:
            continue
        #定义了轮廓线边缘的精确程度
        epsilon = 0.02 * cv2.arcLength(c, True)#cv2.arcLength()计算轮廓的周长
        approx = cv2.approxPolyDP(c, epsilon, True)#cv2.approxPolyDP()主要功能是一个连续光滑曲线折线化
        # 如果轮廓是参考对象
        if count == 1:
            #cv2.convexHull（）得到一系列的凸点
            c = cv2.convexHull(c)
            epsilon = 0.0001 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            left_most = approx[0]     '''取第一个点为左边，取最后一个点为右边'''
            right_most = approx[-1]
            # 遍历引用对象的点以查找
            for i in range(len(approx)):
                if approx[i][0][0] < left_most[0][0]:
                    left_most = approx[i]
                if approx[i][0][0] > right_most[0][0]:
                    right_most = approx[i]
            # 定义了图像中像素个数的比例到真正物体的距离
            pixelsPerMetric = abs(left_most[0][0] - right_most[0][0]) / width
            # 显示比例
            print('Pixel Per Metric Ratio is: ', (pixelsPerMetric))
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)#绘制轮廓
        # 如果轮廓不是参考对象
        else:
            # 如果等轮廓是圆
            if (len(approx) >= 8):
                # 检查凸度缺陷并纠正它们
                c = cv2.convexHull(c)
                # 找出与轮廓拟合的中心和最小半径
                center, radius = cv2.minEnclosingCircle(approx)#cv2.minEnclosingCircle()寻找包裹轮廓的最小圆
                s2 = cv2.arcLength(c, True) / math.pi
                if cv2.isContourConvex(c):#检测返回轮廓是否为凸性的，其实就是检测是不是圆
                    cv2.circle(image, (int(center[0]), int(center[1])),
                               int(radius), (0, 255, 0), thickness=2,
                               lineType=8, shift=0)#画圆形
                    cv2.putText(image, "{:.2f}".format(s2 / pixelsPerMetric),
                                (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                                (0, 0, 255), 2)#把尺寸写入图像
            #如果等轮廓不是圆
            # moshi都为2，此时将计算两种尺寸，可以修模式的值选定一种方式测量
            elif modhi==2 :
                for i in range(len(approx)):#遍历图像顶点
                    # 获取现在和上一个顶点的坐标
                    tlblX, tlblY = approx[i - 1][0][0], approx[i - 1][0][1]
                    tlblX1, tlblY1 = approx[i][0][0], approx[i][0][1]
                    # 再去求这两个顶点的中点
                    x = int((tlblX + tlblX1) / 2) - 15
                    y = int((tlblY + tlblY1) / 2) - 10
                    cv2.putText(image, "{:.2f}".format((dist.euclidean
                                                        (approx[i - 1], approx[i])) / pixelsPerMetric),
                                (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (0, 0, 255), 2)
                    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)#绘制图像轮廓线
            if modhi == 2:
                rect = cv2.minAreaRect(c)#cv2.minAreaRect()求出在点集下最小面积矩形
                (x, y), (w, h), angle = rect
                # 画一个标准矩形
                object_width=w/pixelsPerMetric
                object_height=h/pixelsPerMetric
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.polylines(image, [box], True, (255, 0, 0), 2)
                cv2.putText(image, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                cv2.putText(image, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        count = count + 1
    cv2.imshow("imaga",image)
    key=cv2.waitKey(1)
    if key==27:#按下空格键代表退出
        break
cv2.destroyAllWindows()#关闭所有窗口

