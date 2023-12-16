import pyautogui as pg
import time 
import os
import pandas as pd
import xlwt
import copy
import numpy as np
import re

# 因为Eureqa API已经不再开放 所以使用模拟鼠标点击的方式进行操作
# Eureqa在windows下的按钮位置
eureqaMenuX = 4702
eureqaMenuY = 112
TxtX = 3280
TxtY = 133
RunX = 4774 # 运行按钮的位置
RunY = 79
first = False

# 小心的处理结果保存的excel
def PreReslutsFile(TempDfCol,SavePath):
    writer = pd.ExcelWriter(SavePath)
    for OutVar in TempDfCol:
        dftemp = pd.DataFrame()
        dftemp.to_excel(writer,sheet_name = OutVar)
    writer.save()

def mkdir(path): # 如果不存在文件夹则创建
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path) 
    else: pass
    
# 从excel中复制数据
def AutoAddData(input_file):
    
    os.startfile(input_file)
    time.sleep(2);pg.click(TxtX,TxtY) # 不睡也可以，因为只有上一个结束之后，才会运行下一个
    time.sleep(1);pg.hotkey('ctrl','a')
    time.sleep(1);pg.hotkey('ctrl','c')
    # time.sleep(2);pg.hotkey('ctrl','pgdn') # 切换excel的sheet

    # 输入数据框位置
    # eureqaMenuX = 4570 # x轴，eureqa中的坐标原点
    # eureqaMenuY = 125 # y轴,

    pg.click(eureqaMenuX,eureqaMenuY) # 输入数据框
    pg.click(eureqaMenuX,eureqaMenuY+200) # 这个不需要太精准
    pg.hotkey('ctrl','a')
    pg.press('del')
    #print(eureqaMenuX,eureqaMenuY+126)
    pg.click(eureqaMenuX,eureqaMenuY+126) # 这个需要精准一些
    time.sleep(1);pg.hotkey('ctrl','v')
    
    time.sleep(2);pg.click(TxtX,TxtY)
    time.sleep(1);pg.hotkey('alt','f4') # 关闭窗口

# 定义需要循环操作的函数
def AutoEureqa(FunctionPRE, SaveTxt, RunTime = 60):
    
    time.sleep(0.5);pg.click(eureqaMenuX+244,eureqaMenuY) # 方程定义框
    pg.hotkey('ctrl','a')
    pg.press('del')
    if first:
        pg.press('shift')  # 第一次运行一次即可，切换一下输入法#
    time.sleep(0.5);pg.click(eureqaMenuX+244,eureqaMenuY+128) # 输入方程
    
    time.sleep(1);pg.typewrite(FunctionPRE) #'x4=f(x1,x2,x3,x0)'
    time.sleep(2) # 必须的
    pg.press('enter');time.sleep(0.5)
    
    # 运行程序
    pg.click(RunX,RunY)
    pg.press('right');pg.press('enter') # 点击是否根据以前的结果运行
    time.sleep(RunTime)
    pg.click(RunX+51,RunY) # 结束运行
    
    # 拷贝结果
    pg.click(eureqaMenuX+471,eureqaMenuY) # 点击results窗口
    pg.click(eureqaMenuX,eureqaMenuY+120) # 复制结果
    time.sleep(0.5);pg.hotkey('ctrl','a')
    pg.hotkey('ctrl','c')

    # 粘贴到结果excel
    os.startfile(SaveTxt) # 打开存储结果txt
    time.sleep(2);pg.click(TxtX,TxtY) 
    time.sleep(1);pg.hotkey('ctrl','v')
    time.sleep(1);pg.hotkey('ctrl','s')
    time.sleep(1);pg.hotkey('alt','f4') # 关闭窗口

# 获取eureqa中需要的函数计算形式
def GetTargetExpression(eachTarget,COL):
    FORMATION = str()
    TempCOL = copy.deepcopy(list(COL))
    if eachTarget in TempCOL:
        TempCOL.remove(eachTarget)      

    FORMATION = FORMATION + eachTarget + '=' + 'f('
    for __ in TempCOL:
        FORMATION = FORMATION + __ + ','
    return FORMATION[:-1] + ')'

# 获取自变量个数
def GetVar(function):
    p2 = r'x\d+L*\d*[\^\d]*' 
    return re.findall(p2, function)

# TEST
# NumNodes = 10 # 5，10，20，30
# Length = 500 # 50，100，200，500
# noiserate = 0.1 # 0.05，0.1，0.3，0.5
# CrossDegree = 1 # 1，1.2，1.6，2

# for noiserate in [0.5]: #
#     if noiserate == 0.5:
#         StartofNetwork = 9
#     else:
#         StartofNetwork = 1
    
#     for eachNetworks in range(StartofNetwork,11):
#         path = 'C:/实验数据/密度'+str(CrossDegree) \
#                 +'_数据量'+str(Length)+'_变量数'+str(NumNodes)+'_噪声'+str(noiserate) \
#                 +'/Networks' + str(eachNetworks) + '/'
#         # 创建符号回归的保存目录
#         sspath = 'C:/实验数据/密度'+str(CrossDegree) \
#                 +'_数据量'+str(Length)+'_变量数'+str(NumNodes)+'_噪声'+str(noiserate) \
#                 +'_符号回归/Networks' + str(eachNetworks) + '/'
#         mkdir(sspath)
#         StartofGraph = 1
#         # 如果中途断掉的话，从断点处开始
#         if (noiserate == 0.5) and (eachNetworks == 9):
#            StartofGraph = 24
#         else:
#            StartofGraph = 1
            
#         for jj in range(StartofGraph,51):
#             input_file = path + 'Graph'+str(jj)+'.xlsx'
#             FunctionSave = path + 'Graph'+str(jj)+'Function.npy'
#             NetworkStructure = path +'NetworksLinksDict.npy'
#             FunctionDict = np.load(FunctionSave,allow_pickle=True).tolist()
#             exvar = np.load(NetworkStructure,allow_pickle=True).tolist()['exvar']
            
#             TempDf = pd.read_excel(input_file)
#             SavePath = sspath + 'Graph'+str(jj)+'.xlsx'
#             PreReslutsFile(TempDf.columns,SavePath)
            
#             # 将数据拷到eureqa
#             AutoAddData(input_file)
            
#             # 对每一个输出变量进行计算
#             NextSheet = 0
#             Nexteva = 0
#             for eachTarget in TempDf.columns:
#                 if eachTarget in exvar:
#                     Nexteva += 1
#                     continue
#                 if 'L' in eachTarget: # 循环到滞后变量则停止
#                     break

#                 if len(GetVar(FunctionDict[eachTarget])) <= 2:
#                     if 'exp' in FunctionDict[eachTarget]:
#                         RunTime = 10
#                     else:
#                         RunTime = 5
                    
#                 else:
#                     RunTime = 60
                
            
#                 Expression = GetTargetExpression(eachTarget,TempDf.columns)
#                 AutoEureqa(Expression, SavePath,NextSheet,Nexteva, RunTime = RunTime)
#                 Nexteva = 0
#                 NextSheet += 1





    
