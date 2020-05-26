from tkinter import *
import tkinter as tkinter
import math as math
import time
import numpy as np

#圖片的 軸是從左上角開始 x 是正 y 是負 
#theta car_angle

class rbfNet(object):
    def __init__(self, thegma, weight, m, theta):

        self.theta = theta
        self.thegma = thegma
        self.m = m
        self.weight = weight


    def output (self, x):
        fx = self.add_thegma(0)
        # print('nn = ', nn.shape)
        # print('row of m', np.size(self.m, 0))
        for i in range(np.size(self.m, 0)):
            # print('i = ', i)
            m = self.m[i:i+1, ]
            # print('in put gaussan value', m, m.shape)
            g = self.gaussan(x, i, m)
            # print('g = ', g)
            w = self.mul_weight(g, i)
            # print('fx, w = ', fx, w)
            fx  = fx + w
            # print('return value = ', fx)
        return fx          

    def gaussan(self, x, i, m):
        theta = self.theta[0][i]
        # print('theta = ', theta, m.shape)
        n =  np.exp(-((np.sum(np.square(x-m)) / (2 * np.square(theta)))))
        return n

    def mul_weight(self, n, i):
        weight = self.weight[0][i]
        # print('weight = ', weight, n.shape)
        n = n * weight
        return n

    def add_thegma(self, n):
        n = n + self.thegma[0][0]
        return n

class car:
    #  初始化資料 主要是輸入座標和實際座標上的轉換
    def __init__(self, zero_x, zero_y, multiply_x, multiply_y, car_x, car_y, car_angle , car_r=3, car_collar="red"):
        self.zero_x = zero_x
        self.zero_y = zero_y
        self. multiply_x = multiply_x
        self. multiply_y = multiply_y
        self.car_x = zero_x + car_x * multiply_x
        self.car_y = zero_y + (car_y * -1 )*multiply_y
        self.car_r = car_r
        self.car_collar = car_collar
        self.car_orangle = car_angle
        self.car_angle = round(math.radians(car_angle),2)
        self.direction = 0
        self.ldirection = 0
        self.rdirection = 0
        self.ld = 0
        self.rd = 0
        self.d = 0
        self.b = car_r * multiply_x
        self.x1 = zero_x + -6 * multiply_x
        self.x2 = zero_x + 6 * multiply_x
        self.x3 = zero_x + 18 * multiply_x
        self.x4 = zero_x + 30 * multiply_x
        self.y1 = zero_y + -10 * multiply_y
        self.y2 = zero_y + -22* multiply_y
        self.y3 = zero_y + -50 * multiply_y
        self.g1 = zero_y + -40 * multiply_y
        self.g2 = zero_y + -37 * multiply_y

    #畫線 方程式
    def create_line(self, x1, y1, x2, y2, color):
        return canvas.create_line(zero_x+x1*multiply_x, zero_y+(y1*-1)*self.multiply_y,
                           zero_x+x2*multiply_x, zero_y+(y2*-1)*self.multiply_y, fill=color, width=3)
    #畫車方程式
    def create_car(self):  
        
        # center coordinates, radius

        x0 = self.car_x - self.car_r*self.multiply_x
        y0 = self.car_y - self.car_r*self.multiply_y
        x1 = self.car_x + self.car_r*self.multiply_x
        y1 = self.car_y + self.car_r*self.multiply_y

        

        return canvas.create_oval(x0, y0, x1, y1, fill=self.car_collar)
    
    #觀測距離方程式 針對每個邊界 做判斷取最小的值
    def sensor_distace(self, angle) :
        #sensor  sensor + angle judge
        x1d = (abs(self.car_x - self.x1 ) * -1 * (1/ math.cos(angle)))
        x1dc = abs((self.car_x - self.x1 ) * (math.tan(angle)))
        
        if(self.car_y - x1dc <= self.y2 or x1d < 0):
            #設為最大值
            x1d = 10000

        else :

            x1d = x1d / self.multiply_x
        
        #print('x1d', x1d)
        
        x2d = (abs(self.car_x - self.x2 ) * (1/ math.cos(angle)))
        x2dc = (abs(self.car_x - self.x2 ) * (math.tan(angle)))
        
        
        if(self.car_y - x2dc <= self.y1 or x2d < 0):
            #設為最大值
            x2d = 10000
            
        else :
            x2d = x2d / self.multiply_x
        
        #print('x2d', x2d)

        x3d = (abs(self.car_x - self.x3 ) * -1 *(1/ math.cos(angle)))
        x3dc = abs((self.car_x - self.x3 ) * (math.tan(angle)))
        
        #print('???? ', x3d, x3dc, self.car_y, self.y1)
        if(self.car_y - x3dc <= self.y3 or x3d < 0):
            #設為最大值
            x3d = 10000
            
        else :
            
            x3d = x3d / self.multiply_x
        
        #print('x3d', x3d)

        x4d = (abs(self.car_x - self.x4 )  * (1/ math.cos(angle)))
        x4dc = abs((self.car_x - self.x4 ) * (math.tan(angle)))
        
        if(self.car_y - x4dc <= self.y3 or x4d < 0):
            #設為最大值
            x4d = 10000
            
        else :
           
            x4d = x4d / self.multiply_x
        
        #print('x4d', x4d)

        y2d = (abs(self.car_y - self.y2) * (1/ math.sin(angle)))
        y2dc = abs((self.car_y - self.y2 ) * abs(1/math.tan(angle)))

        if(self.car_x + y2dc >= self.x3 or y2d < 0 ):
            y2d = 10000
        else :
            y2d = y2d / self.multiply_y
        
        #print('y2d', y2d)

        y1d = (abs(self.car_y - self.y1) * -1 * (1/ math.sin(angle)))
        y1dc = abs((self.car_y - self.y1 ) * (1/math.tan(angle)))

        
        if(self.car_x + y1dc <= self.x2 or y1d < 0):
            y1d = 10000
        else :
            y1d = y1d / self.multiply_y
        
        #print('y1d', y1d)

        
        y3d = (abs(self.car_y - self.y3) * (1/ math.sin(angle)))
        y3dc = abs((self.car_y - self.y3 ) * abs(1/math.tan(angle)))

        if(self.car_x + y3dc >= self.x4 or y3d < 0 ):
            y3d = 10000
        else :
            y3d = y3d / self.multiply_y
        
        #print('y3d', y3d)

        #print('d ', min(x1d, x2d, x3d, x4d, y1d, y2d, y3d))
        d = min(x1d, x2d, x3d, x4d, y1d, y2d, y3d)
        if(d <= 3):
            return 0
        else :
            return d
    #邊界距離觀測
    def distance(self) :
        
        d1 = 100
        d2 = 100
        d3 = 100
        d4 = 100
        d5 = 100
        d6 = 100
        d7 = 100
        if(self.car_x < 6):
            d1 = abs (self.car_x - self.x1)
            d2 = abs (self.car_x - self.x2)
            d6 = abs (self.car_y - self.y2)
        elif(self.car_x < 18):
            d1 = abs (self.car_x - self.x1)
            d4 = abs (self.car_x - self.x4)
            d5 = abs (self.car_y - self.y1)
            d6 = abs (self.car_y - self.y2)
        else :
            d3 = abs (self.car_x - self.x3)
            d4 = abs (self.car_x - self.x4)
            d5 = abs (self.car_y - self.y1)
            d4 = abs (self.car_y - self.y3)

        # print('distance', d1, d2, d3, d4, d5, d6, d7)
        return min(d1, d2, d3, d4, d5, d6, d7)

    #終點線觀測
    def goalLine(self):

        #goal line distance
        if(self.car_x >= self.x3 and self.car_x <= self.x4): 
            x = ( self.car_x - zero_x ) / self.multiply_x
            d =  -1 * (x )/4  +  (44.5 )
            y = -1 *(self.car_y - zero_y) / self.multiply_y
            print('goal d = ', d, y)
            return d - y
        else: 
            return -1
            
    #車子移動 -> 儲存目前車子所在數據, 回傳sensor 數據
    def car_move(self, tk, car, theta):
        
        degree = theta
        #角度換算
        theta = round(math.radians(theta),2)

        #car momenton
        self.car_x = self.car_x + 10*(math.cos(self.car_angle) * math.cos(theta)) 
        self.car_y = self.car_y -  10*(math.sin(self.car_angle) * math.cos(theta))
        self.car_angle = self.car_angle - math.asin(2 * math.sin(theta) / self.car_r)

    
        x0 = self.car_x - self.car_r*self.multiply_x
        y0 = self.car_y - self.car_r*self.multiply_y
        x1 = self.car_x + self.car_r*self.multiply_x
        y1 = self.car_y + self.car_r*self.multiply_y

       
        
        #draw the car
        tk.coords(car, (x0, y0, x1, y1))

        canvas.delete(self.direction)
        canvas.delete(self.ldirection)
        canvas.delete(self.rdirection)
        # direction line 
        #car_x = zero_x + car_x * multiply_x
        #car_y = zero_y + (car_y * -1 )*multiply_y
        car_x1 =  (self.car_x - self.zero_x) / self.multiply_x
        car_y1 = (self.car_y  - self.zero_y) / self.multiply_y * -1
        
        
        x2 = car_x1 + 6* math.cos(self.car_angle)
        y2 = car_y1 + 6* math.sin(self.car_angle)

        
        #draw the direction line
        self.direction = self.create_line(car_x1, car_y1, x2, y2, "red")

        #compute the sensor angle
        round(math.radians(car_angle),2)
        langle =   self.car_angle + round(math.radians(45),2)
        rangle = self.car_angle - round(math.radians(45),2)

        #draw the the sensor line
        x2 = car_x1 + 6* math.cos(langle )
        y2 = car_y1 + 6* math.sin(langle ) 
        self.ldirection = self.create_line(car_x1, car_y1, x2, y2, "black")

        x2 = car_x1 + 6* math.cos(rangle )
        y2 = car_y1 + 6* math.sin(rangle ) 
        self.rdirection = self.create_line(car_x1, car_y1, x2, y2, "black")
        
        #sensor part
        #往回開就是腦袋開抽
        #boundary base

        d = self.sensor_distace(self.car_angle)
        ld = self.sensor_distace(langle)
        rd = self.sensor_distace(rangle)
        gd = self.goalLine()
        dd = self.distance()
      

        if(d == 0.1 or ld == 0.1 or rd == 0.1):
            canvas.delete(self.d)
            canvas.delete(self.ld)
            canvas.delete(self.rd)
            dw = Label(canvas, text = 'stop', fg='white', bg='black')
            dw.pack()
            canvas.create_window(100, 100, window=dw)

        else :
        
            dw = Label(canvas, text = 'd : ' + str(d), fg='white', bg='black')
            dw.pack()
            self.d = canvas.create_window(100, 100, window=dw)
        
            ldw = Label(canvas, text = 'ld : ' + str(ld), fg='white', bg='black')
            ldw.pack()
            self.ld = canvas.create_window(100, 75, window=ldw)
        
            rdw = Label(canvas, text = 'rd : ' + str(rd), fg='white', bg='black')
            rdw.pack()
            self.rd = canvas.create_window(100, 125, window=rdw)
        
        #self.car_x = zero_x + car_x * multiply_x
        #self.car_y = zero_y + (car_y * -1 )*multiply_y
        x = (self.car_x - zero_x)/self.multiply_x
        y = (self.car_y - zero_y)/self.multiply_y * -1
        
        # 開啟檔案
        fp = open("train6D.txt", "a")
 
        #寫入檔案
        p = str(x) + " " + str(y) + " " + str(d) + " " + str(rd) + " " + str(ld) + " " + str(degree) + "\n"
        fp.write(p)
 
        # 關閉檔案
        fp.close()

        fp = open("train4D.txt", "a")
 
        # 寫入檔案
        p = str(d) + " " + str(rd) + " " + str(ld) + " " + str(degree) + "\n"
        fp.write(p)
 
        # 關閉檔案
        fp.close()

        return (x, y, d, ld, rd, gd, dd)

    #模糊演算法
    def fuuzzyRule(self, d, ld, rd):
        #d1, d2 兩個模糊規則判定
        d1 = d
        d2 = ld - rd 
        d1a = 1
        d2a = 1
        al = 25
        am = 40
        ar = 70
        a1 = 0
        a2 = 0
        a3 = 0
        a4 = 0 
        a5 = 0
        a6 = 0
        a7 = 0
        a8 = 0
        a9 = 0
        #d1 is large 
        if(d1 >= 15 ):
            if(d1 < 20 ):
                d1a = 1 * (d1 - 15) / 5
            if(d2 >= 0):
                if(d2 < 8):
                    d2a = 1 * (d2 - 0) / 8
                a1 = min(d1a, d2a)
            if(d2 < 8 and d2 >= -8):
                if(d2 > 0):
                    d2a = 1 * (8- d2) / 8
                else :
                    d2a = 1 * (d2 + 8) / 8
                a2 = min(d1a, d2a)
            if(d2 < 0):
                if(d2 < -8):
                    d2a = 1 * abs(d2) / 8
                a3 = min(d1a, d2a)
        #d1 is middle
        if(d1 < 20 and d1 >= 10 ):
            if(d1 >= 15 ):
                d1a = 1 * (20-d1) / 5
            else:
                d1a = 1 * (d1 - 10) / 5
            if(d2 >= 0):
                if(d2 < 8):
                    d2a = 1 * (d2 - 0) / 8
                a4 = min(d1a, d2a)
            if(d2 < 8 and d2 >= -8):
                if(d2 > 0):
                    d2a = 1 * (8- d2) / 8
                else :
                    d2a = 1 * (d2 + 8) / 8
                a5 = min(d1a, d2a)
            if(d2 < 0):
                if(d2 < -8):
                    d2a = 1 * abs(d2) / 8
                a6 = min(d1a, d2a)
        #d1 is small
        if(d1 < 15):
            if(d1 >= 10 ):
                d1a = 1 * (15-d1) / 5
            
            if(d2 >= 0):
                if(d2 < 8):
                    d2a = 1 * (d2 - 0) / 8
                a7 = min(d1a, d2a)
            if(d2 < 8 and d2 >= -8):
                if(d2 > 0):
                    d2a = 1 * (8- d2) / 8
                else :
                    d2a = 1 * (d2 + 8) / 8
                a8 = min(d1a, d2a)
            if(d2 < 0):
                if(d2 < -8):
                    d2a = 1 * abs(d2) / 8
                a9 = min(d1a, d2a)
        print('a', a1, a2, a3, a4, a5, a6, a7,a8, a9)

        #final output
        output = (a1 * al + a2 * am + a3 *ar +  a4 * al + a5 * am + a6 * am + a7 * al + a8 * am + a9 * ar ) / (a1 + a2 + a3 + a4 + a5 + a6 + a7 +a8 + a9)
        print('return angle ', output - 40)
        return (output - 40)
   
        
        
       


# Initial Form 
tk = Tk()
tk.title('assignment1')
tk.resizable(0, 0)


#Intial Value
width = 500
height = 500

multiply_x = width/60
multiply_y = height/60
zero_x = int(width/4)
zero_y = int(height/1.1)

#讀取檔案資料
f = open(r'case01.txt')
i = 0
for line in f:
    s = line.split(",")
    if(i == 0):
        print('line s ', s)
        car_x = int(s[0])
        car_y = int(s[1])
        car_angle = int(s[2])

    i = i + 1

        
car = car(zero_x, zero_y, multiply_x, multiply_y, car_x, car_y, car_angle)

canvas = Canvas(tk, width=width, height=height, bg='ivory')
canvas.pack(fill=BOTH, expand=1)
canvas.pack()
#讀兩次檔
f = open(r'case01.txt')
i = 0
x1 = 0
y1 = 0 
x2 = 0 
y2 = 0
for line in f:
    s = line.split(",")
    if(i > 0) :
        if(i % 2 != 0):
            x1 = int(s[0])
            y1 = int(s[1])
        else :
            x2 = int(s[0])
            y2 = int(s[1])
    if(i == 2) : 
        print('goal', x1, y1, x2, y2)
        car.create_line(x1, y1, x2, y2, "red")

    if(i > 3):
        car.create_line(x1, y1, x2, y2, "blue")

    i = i + 1

# CAR
car_obj = car.create_car()

#起跑線 0,0
car.create_line(-12, 0, 12, 0, "black")

t = 0




#set rbnf variable

g_data4 = np.array([[   -4.2645438 ,  22.10915504,  10.91203041,   5.83474849,
        26.93762812, -38.50505942,   3.68180169, -17.51594218,
        -0.63084018,  31.69029435, -20.73037229,  21.38580126,
        34.06977064,  10.3459436 ,  18.58443401, -28.03558003,
        -4.67730619,  22.18808445,  12.88442223,   6.67348919,
       -12.99125284,  15.37771472,  14.85683369,  -1.69935296,
       -34.11911344, -21.36198651, -20.18290213,  39.53128822,
       -15.84102794,   8.84937315, -17.52453772,  55.24941591,
        35.47885785,  -0.34617844,  22.02597452, -43.06968114,
       -32.41074412, -37.28121746,  28.02021472,  28.1348629 ,
       -41.03116774, -21.96607592,  -8.78433146,  -2.43319212,
       -45.26943073,  -0.42541792, -26.72101244, -15.66874825,
         8.98066036, -28.04217578,  11.77509578,   6.55165523,
       -18.52575853,  40.65723925,  26.15237946,  11.84451055,
        29.90286668, -39.13290055,  16.43208102,  16.04454567,
       -35.9857023 ,  13.50981601, -23.92349808,   1.72416565,
       -18.22135314, -28.02692636,  -6.71153034,  23.3635479 ,
       -16.46890032,  21.25073285, -30.31000781, -34.53992066,
       -22.07119078, -45.9474352 , -40.8987859 ,  32.47466372,
       -36.1374676 ,  15.66890294,   6.83439899, -13.6899103 ,
       -12.80628519,  20.04733266,  25.72858913,  28.95682172,
        26.39427174, -16.73851559,  -2.10083204,  10.55808482,
       -23.22056737,  18.78084824,  25.13353784,  -3.84072625,
       -34.72948144, -50.37408294,  24.87199041,  -9.37877678,
        -3.80901901,  29.60814092, -14.32549549,  30.53571064,
        32.23972095, -11.30883155,  31.55887073,  13.35599545,
       -21.2791951 ,  34.41451135,  27.48890645, -41.69706604,
        -0.24810759, -20.68037718,   1.16722949,  -6.36823876,
        28.55385396, -53.25365191,  38.84843058, -11.02510711,
        31.01207422,  23.98515053,  17.24315688,  32.06236789,
       -11.18590345,  -6.6409918 ,   1.36291076,   8.50115793,
        28.80971669,   1.26788321,   3.23113289, -35.1364037 ,
        -8.92852571,  -7.48731089,  20.61684776,  11.75103616,
        17.16876948,  27.83402252, -33.39375649,  -0.45382279,
         9.09113984,   5.46228133,  43.13870769,  17.77165801,
        16.84711006,   8.01553605,  24.25721715,  -8.8996879 ,
         2.63624471,  16.87997254,  14.50279147, -19.02245717,
        19.40171528, -16.66854328, -14.46082304,  20.93097404,
         0.38325063,  38.89749016, -27.9849378 , -21.36962706,
       -31.47907227,  -7.81973243, -38.9752166 , -29.35434594,
        -7.58074107,  12.85680385,  34.80348705,  29.44039263,
        38.20810585,  35.20080512,  21.24953217,  29.99245062,
        28.31161401,   2.69146355,  27.14556121,  29.06907956,
         6.11689714,  37.51088874,  18.3986768 ,   2.41515925,
        23.51448082,  27.74201468,   9.36835295,  27.226976  ,
         9.6732251 ,  28.83460039,  36.56610734,  41.97876215,
        29.93211666,  24.65771286,  10.95004976,  28.76526902,
        20.76920403,  29.64678493,  21.46108454,   6.47726244,
        11.07222034,   2.02641687,   1.43342628,  22.13716799,
         1.49112601,  24.92404306,   4.86036319,  40.88768273,
        26.53496317]])
g_data6 = np.array([[  -2.19078241e+00,  2.30558498e+01, -9.13361142e+00,  3.56881865e+01,
        1.51611102e+01, -1.05576511e+01,  7.79540262e-01,  7.43508700e+00,
       -3.79280468e+01, -2.31100845e+01, -1.67115231e+01, -3.93577891e+01,
       -1.60599201e+01,  9.12139531e+00, -1.13034097e+01, -2.64276985e+01,
       -7.48953855e+00,  3.60465498e+01, -1.90571719e+01,  5.51591694e+00,
        1.05754595e+00,  3.94301207e+01, -3.75421843e+01,  1.22445098e+01,
        3.49722391e+01,  3.32286667e+01, -4.03105373e+01, -1.22338884e+01,
       -3.61681322e+01,  1.72943129e+01,  3.76651179e+01,  4.16944779e+01,
        1.23811626e+01,  5.72517283e+00,  3.58253776e+01,  2.09197762e+01,
       -1.50604293e+01,  3.28240877e+01,  1.15820156e+01,  5.91002416e+01,
        3.31839639e+01,  1.79735382e+01, -2.02095204e+01, -2.90741761e+01,
       -2.63156486e+01,  3.70776846e+01,  1.00978144e+01, -1.58112968e+01,
       -2.34529389e+01,  3.08452644e+01, -3.09614512e+00,  1.04401451e+01,
       -1.26393895e+01, -1.78677424e+01, -3.42371375e-01, -6.17956756e-01,
        3.12722745e+01,  2.53747810e+01, -3.52593123e+01,  2.64556054e+00,
       -3.02739839e+01, -3.28664142e+01, -8.67920172e+00, -6.33129279e+00,
       -2.61597611e+00, -5.51343553e+01,  1.15543279e+01, -2.26695231e+01,
       -8.91217947e-02, -1.94478483e+01, -1.25828411e+01, -2.00982363e+01,
        2.86392750e+01, -6.96614983e+00, -3.16683379e+01, -4.35414773e+01,
       -1.44683871e+01, -2.86749859e+01,  2.29534827e+01,  2.97509042e+01,
       -6.43976124e-01,  1.47735670e+01, -1.87776677e+01, -2.64872289e+01,
       -2.43988638e+00,  3.82093661e+01, -3.12814618e+01, -1.72214420e+01,
        5.93557285e+00,  1.09251290e+01, -1.71433916e+00, -3.96515952e+01,
       -1.63957318e+01, -9.78130610e+00, -2.43393419e+01,  4.20820927e+01,
        8.63936685e+00, -3.34903872e+01,  2.43143540e+01,  3.26078592e+01,
        3.57228490e+01,  2.18948439e+01,  3.08050057e+01,  1.71917387e+01,
       -2.64010152e+01, -2.99564400e+01, -3.10127843e+01,  2.80349764e+01,
       -4.83100761e+01,  5.64315109e+00, -2.35947846e+01,  6.36393125e+00,
       -1.25762797e+01, -3.36126584e+01,  3.74366804e+01, -1.30960105e+01,
       -3.37584687e+01, -1.41871814e+01, -3.60833595e+01,  4.37170881e+00,
        1.11907023e+00,  4.17296941e+01, -2.04190732e+01,  1.20835474e+01,
       -4.01212649e+01, -1.61454003e+01, -2.11879150e+00, -3.06757754e+01,
        2.61079917e+01, -6.30929097e+00, -5.13793033e+00,  2.11255688e+01,
        2.07529212e+01, -1.80508567e+01,  5.30429459e+01,  8.35622346e+00,
       -3.61773932e+01, -4.05262529e+01, -3.69425457e+01,  1.94824980e+01,
        5.72634776e+00,  5.76804401e+00,  2.51470144e+01,  6.33425126e+00,
        3.04887206e+01, -1.46403584e-02,  3.71716601e+01, -3.79076910e+01,
       -2.60766231e+01,  2.16943125e+01, -1.85500825e+01,  9.02637449e+00,
        8.86044432e+00, -2.30675871e+01, -5.31158180e+00,  4.45189606e+00,
        2.35172970e+01, -2.50245923e+01, -2.44371179e+01,  9.50716826e+00,
        3.73415353e+01,  1.11932107e+01, -4.32858362e+01,  1.34869752e+00,
        2.07755735e+01,  1.19169365e+01,  1.44871332e+01,  1.15319871e+01,
        2.12667552e+01,  1.62498664e+01,  2.79776119e+00, -4.88547607e+01,
       -2.55126435e-02,  3.91064623e+01, -1.65413066e+01, -2.46519669e+00,
        1.78056503e+01,  3.45034326e+01, -1.51699736e+01,  1.16826406e+01,
        9.01662937e+00,  2.54619713e+01, -2.06247576e+01,  2.68548906e+01,
        5.54577671e+00,  2.58236153e+01,  5.50220658e+00, -7.90851662e+00,
        1.60884100e+01, -4.13908884e+01,  4.30288098e+01, -3.03849798e+01,
       -7.12006332e-01, -3.13938828e+01,  6.51618032e-01, -3.99572175e+00,
        1.00484238e+01, -3.32135853e+00, -1.19342697e+01, -1.74560499e+01,
       -3.84482179e+01,  1.63965428e+01, -1.73885693e+01,  2.24087962e+01,
       -9.48733159e+00, -3.39296024e+01, -2.21160525e+01, -1.71335109e+01,
        3.09529139e+01,  2.74839297e+01, -1.50347886e+01,  2.25868360e+01,
       -2.53948768e+01,  1.99149523e+00, -1.20420001e+01, -1.84329675e+01,
        2.76029508e+01, -8.78360800e+00,  5.05610504e+00,  3.58781293e+01,
        2.14107391e+01, -2.49789851e+01, -1.88721904e+01,  3.41469450e+00,
        1.42957758e+01,  2.78721007e+01,  2.90499033e+01, -3.95181901e-01,
        7.47747414e+00,  2.77367793e+01, -2.27757398e+01,  2.00201906e+00,
        1.64210069e+01,  2.49117495e+01,  8.91702290e+00,  5.65883462e+00,
       -3.89161630e+01, -1.71198848e+01,  8.05116720e+00,  5.18087094e+00,
       -1.85820383e+01,  2.91821461e+01,  1.29321499e+01,  6.86642756e+00,
        3.78162924e+00,  4.04219013e+01,  9.51663569e+00,  1.15094766e+01,
        2.46493924e+01,  1.90182089e+01,  2.55107496e+01,  4.28238186e+01,
        4.10819530e+01,  2.07692127e+01,  1.21041547e+01,  1.02001993e+00,
        1.52976763e+01,  1.75383396e+01,  2.38796598e+01,  1.02979520e+00,
        4.81426013e+00,  2.54350744e+01,  4.25065973e+01,  3.42974846e+01,
        2.51170111e+01,  1.25864197e+01,  8.75235782e+00,  2.65290253e+01,
        4.83082963e+01,  9.89608808e+00,  1.17282055e+01,  4.99330399e+01,
        2.60672509e+01,  4.23668634e+01,  4.46115127e+01,  2.66297245e+01,
        3.50217662e+01,  1.03626600e+01,  5.19349026e+00,  5.27014432e+00,
        3.10582496e+01]])

j = 40

print('Enter the data set you want (4, 6):')
dataChoose = int(input())
# dataChoose = 6
if(dataChoose == 6):

    dim = 1 + j + 5*j + j

    thegma = g_data6[:, 0:1]
    # print('thegma = ', thegma.shape)
    weight = g_data6[:, 1: j+1]
    # print('weight = ', weight.shape)
    theta = g_data6[:, dim-j: dim]
    # print('theta = ', theta.shape)
    m = g_data6[:, j+1: j+1+(5*j )]
    m = np.reshape(m, (j, 5))
    # print('m = ', m.shape)
    print('check input of net = ', thegma, weight, theta, m)

if(dataChoose == 4):
    
    dim = 1 + j + 3*j + j

    thegma = g_data4[:, 0:1]
    # print('thegma = ', thegma.shape)
    weight = g_data4[:, 1: j+1]
    # print('weight = ', weight.shape)
    theta = g_data4[:, dim-j: dim]
    # print('theta = ', theta.shape)
    m = g_data4[:, j+1: j+1+(3*j )]
    m = np.reshape(m, (j, 3))
    # print('m = ', m.shape)
    print('check input of net = ', thegma, weight, theta, m)

# set input data
net = rbfNet(thegma, weight, m, theta)


#初始角度 為 0
x, y, d,ld,rd,gd, dd = car.car_move(canvas, car_obj, 0)

# 輸入設定
if(dataChoose == 6):
    x = np.array([[x, y,d, rd, ld]])
if(dataChoose == 4):
    x = np.array([[d, rd, ld]])

dd = 100
kk = 0

while 1:
    if(gd == -1):
        gd = 100
    if(gd >= 3 ):

        # use rbfn to calculate
        print("input x ",x)

        t = net.output(x)

        print("t  = ", t)
        # move based on rbfn output
        
        x, y, d,ld,rd,gd, dd = car.car_move(canvas, car_obj, t)
        # 輸入設定
        if(dataChoose == 6):
            x = np.array([[x,y,d, rd, ld]])
        if(dataChoose == 4):
            x = np.array([[d, rd, ld]])


        time.sleep(0.7)
        tk.update()
        canvas.update()
    else :
        print('Stop')
        break

print('vvvv = ', theta, m, weight, thegma)
 # 開啟檔案
fp = open("params.txt", "a")
 #寫入檔案
p = str(thegma[0][0]) + "\n"
fp.write(p)
 

for i in range(j):
    print('theta = ', weight[0][i], m[i:i+1], theta[0][i])
    listToStr = ' '.join(map(str, m[i:i+1][0]))
    p = str(weight[0][i]) + " " + listToStr + " " + str(theta[0][i]) + "\n"
    fp.write(p)
# 關閉檔案
fp.close()

