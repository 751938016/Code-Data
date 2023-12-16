import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
# 绘制主要结果（变密度和变噪声在一张图上）
def PlotRate(y_value,y_value1,y_value3,TitleName,AllrowNum,AllColNum,positioni,positionj):
    '''传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
            方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('seaborn-deep') # 设置风格
    plt.boxplot(y_value,positions=[1,2.25,3.5,4.75],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    # 在同一个图上绘制多个箱型图
    plt.boxplot(y_value1,positions=[0.75,2,3.25,4.5],patch_artist=True,showmeans=True,
                boxprops={"facecolor": "#FFBE7A","edgecolor": "#FFBE7A","linewidth": 0.5},
                medianprops={"color": "black", "linewidth": 2},
                meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                widths = 0.2) # 注意显示平均值时，线段和图形不一样
    plt.boxplot(y_value3,positions=[1.25,2.5,3.75,5],patch_artist=True,showmeans=True,
                boxprops={"facecolor": "#FA7F6F","edgecolor": "#FA7F6F","linewidth": 0.5},
                medianprops={"color": "black", "linewidth": 2},
                meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                widths = 0.2) # 注意显示平均值时，线段和图形不一样
    plt.axvline(x=1.625, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    plt.axvline(x=2.875, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    plt.axvline(x=4.125, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positioni == 0:
        # 标题 pad表示与图像的距离
        plt.title(TitleName,fontproperties = 'Times New Roman',fontsize=20,pad=15)
    if positionj == 0:
        if positioni == 0:
            plt.ylabel('True positivies\n Linear',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 1:
            plt.ylabel('True positivies\n Quadratic',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 2:
            plt.ylabel('True positivies\n Exponential',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 3:
            plt.ylabel('False positivies',fontproperties = 'Times New Roman',fontsize=20)
    if positioni == 3:
        plt.ylim(0,1) # y轴范围
        plt.yscale('symlog',linthreshy=0.05*2) # 实现纵坐标刻度的非线性显示
        plt.yticks([0.01,0.05,0.1,0.25,0.5,1.0],['0.01','0.05','0.1','0.25','0.5','1.0'],fontproperties = 'Times New Roman',fontsize=11)
        # x轴标签 固定的位置 标上文本
        plt.xticks([1,2.25,3.5,4.75],['0.05','0.1','0.3','0.5'],fontproperties = 'Times New Roman',fontsize=11)
        # 生成水平线
        plt.axhline(y=0.1, xmin=0, xmax=5,color='red')
        plt.axhline(y=0.05, xmin=0, xmax=5,color='grey')
        #plt.xlabel('Noise Rate',fontproperties = 'Times New Roman',fontsize=20)
    else:
        plt.ylim(0,1) # y轴范围
    
    if positionj == 0:
        
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])

# 绘制补充文件中的图 只变一个维度

# 绘制补充文件中的图 只变一个维度
def PlotRateSI(y_value,TitleName,AllrowNum,AllColNum,positioni,positionj,NumberofCompareType):
    '''传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
            方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格
    f = plt.boxplot(y_value,positions=[i for i in range(1,NumberofCompareType+1)],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']  # 颜色代码列表
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positioni == 0:
        # 标题 pad表示与图像的距离
        plt.title(TitleName,fontproperties = 'Times New Roman',fontsize=20,pad=15)
    if positionj == 0:
        if positioni == 0:
            plt.ylabel('True positivies\n Linear',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 1:
            plt.ylabel('True positivies\n Quadratic',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 2:
            plt.ylabel('True positivies\n Exponential',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 3:
            plt.ylabel('False positivies',fontproperties = 'Times New Roman',fontsize=20)
    if positioni == 3:
        plt.ylim(0,1) # y轴范围
        plt.yscale('symlog',linthreshy=0.05*2) # 实现纵坐标刻度的非线性显示
        plt.yticks([0.01,0.05,0.1,0.25,0.5,1.0],['0.01','0.05','0.1','0.25','0.5','1.0'],fontproperties = 'Times New Roman',fontsize=11)
        # x轴标签 固定的位置 标上文本
        plt.xticks([1,2,3,4],['50','100','200','500'],fontproperties = 'Times New Roman',fontsize=11)
        # plt.xticks([1,2,3,4,5],['0.1','0.2','0.5','1','2'],fontproperties = 'Times New Roman',fontsize=11)
        # 生成水平线
        plt.axhline(y=0.1, xmin=0, xmax=5,color='red')
        plt.axhline(y=0.05, xmin=0, xmax=5,color='grey')
        #plt.xlabel('Noise Rate',fontproperties = 'Times New Roman',fontsize=20)
    else:
        plt.ylim(0,1) # y轴范围
    
    if positionj == 0:
        
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])



def PlotRateOnlySRIT(y_value,AllrowNum,AllColNum,positioni,positionj,NumberofCompareType):
    '''传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
            方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格

    f = plt.boxplot(y_value,positions=[i for i in range(1,NumberofCompareType+1)],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']  # 颜色代码列表
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    # if positioni == 0:
    #     # 标题 pad表示与图像的距离
    #     plt.title(TitleName,fontproperties = 'Times New Roman',fontsize=20,pad=15)

    

    if positionj == 0:
        plt.ylabel('Rates',fontproperties = 'Times New Roman',fontsize=20)
        plt.title('True positivies\n Linear',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 1:
        plt.title('True positivies\n Quadratic',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 2:
        plt.title('True positivies\n Exponential',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 3:
        plt.title('False positivies',fontproperties = 'Times New Roman',fontsize=20)

    
    if positionj != 3:
        plt.ylim(0,1) # y轴范围
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    elif positionj == 3:
        plt.ylim(0,1) # y轴范围
        plt.yscale('symlog',linthreshy=0.05*2) # 实现纵坐标刻度的非线性显示
        plt.yticks([0.01,0.05,0.1,0.25,0.5,1.0],['0.01','0.05','0.1','0.25','0.5','1.0'],fontproperties = 'Times New Roman',fontsize=11)
        # x轴标签 固定的位置 标上文本
        
        # plt.xticks([1,2,3,4],['1','1.2','1.6','2'],fontproperties = 'Times New Roman',fontsize=11)
        # 生成水平线
        plt.axhline(y=0.1, xmin=0, xmax=5,color='red')
        plt.axhline(y=0.05, xmin=0, xmax=5,color='grey')
        #plt.xlabel('Noise Rate',fontproperties = 'Times New Roman',fontsize=20)
    else:
        plt.gca().yaxis.set_ticklabels([])

    # plt.xticks([1,2,3,4,5],['0.1','0.2','0.5','1','2'],fontproperties = 'Times New Roman',fontsize=11)
    plt.xticks([1,2,3,4,5],['5','20','30','40','80'],fontproperties = 'Times New Roman',fontsize=11)


def PlotRateVariousFunction(y_value,AllrowNum,AllColNum,positioni,positionj,NumberofCompareType):
    '''传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
            方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格

    f = plt.boxplot(y_value,positions=[i for i in range(1,NumberofCompareType+1)],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']  # 颜色代码列表
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    # if positioni == 0:
    #     # 标题 pad表示与图像的距离
    #     plt.title(TitleName,fontproperties = 'Times New Roman',fontsize=20,pad=15)

    if positionj == 0:
        plt.ylabel('Rates',fontproperties = 'Times New Roman',fontsize=20)
        plt.title('True positivies\n Linear',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 1:
        plt.title('True positivies\n Log',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 2:
        plt.title('False positivies',fontproperties = 'Times New Roman',fontsize=20)

    
    if positionj != 2:
        plt.ylim(0,1) # y轴范围
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    elif positionj == 2:
        plt.ylim(0,1) # y轴范围
        plt.yscale('symlog',linthreshy=0.05*2) # 实现纵坐标刻度的非线性显示
        plt.yticks([0.01,0.05,0.1,0.25,0.5,1.0],['0.01','0.05','0.1','0.25','0.5','1.0'],fontproperties = 'Times New Roman',fontsize=11)
        # x轴标签 固定的位置 标上文本
        
        # plt.xticks([1,2,3,4],['1','1.2','1.6','2'],fontproperties = 'Times New Roman',fontsize=11)
        # 生成水平线
        plt.axhline(y=0.1, xmin=0, xmax=5,color='red')
        plt.axhline(y=0.05, xmin=0, xmax=5,color='grey')
        #plt.xlabel('Noise Rate',fontproperties = 'Times New Roman',fontsize=20)
    else:
        plt.gca().yaxis.set_ticklabels([])

    # plt.xticks([1,2,3,4,5],['0.1','0.2','0.5','1','2'],fontproperties = 'Times New Roman',fontsize=11)
    plt.xticks([1,2,3,4,5,6],['LiNGAM','DirectLiNGAM','GES','PC','RESIT','SRIT'],
                fontproperties = 'Times New Roman',fontsize=11,rotation=30)

def PlotRateallFunction(y_value,AllrowNum,AllColNum,positioni,positionj,NumberofCompareType):
    '''传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
            方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格

    f = plt.boxplot(y_value,positions=[i for i in range(1,NumberofCompareType+1)],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']  # 颜色代码列表
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    # if positioni == 0:
    #     # 标题 pad表示与图像的距离
    #     plt.title(TitleName,fontproperties = 'Times New Roman',fontsize=20,pad=15)
    if positionj == 0:
        plt.ylabel('Rates',fontproperties = 'Times New Roman',fontsize=20)

    if positioni == 0 and positionj == 0:
        plt.title('True positivies (Linear)',fontproperties = 'Times New Roman',fontsize=20)
    elif positioni == 0 and positionj == 1:
        plt.title('True positivies (Division)',fontproperties = 'Times New Roman',fontsize=20)
    elif positioni == 0 and positionj == 2:
        plt.title('True positivies (Log)',fontproperties = 'Times New Roman',fontsize=20)
    elif positioni == 0 and positionj == 3:
        plt.title('True positivies (Square Root)',fontproperties = 'Times New Roman',fontsize=20)
    elif positioni == 1 and positionj == 0:
        plt.title('True positivies (Cosine)',fontproperties = 'Times New Roman',fontsize=20)
    elif positioni == 1 and positionj == 1:
        plt.title('True positivies (Quadratic)',fontproperties = 'Times New Roman',fontsize=20)
    elif positioni == 1 and positionj == 2:
        plt.title('True positivies (Exponential)',fontproperties = 'Times New Roman',fontsize=20)
    elif positioni == 1 and positionj == 3:
        plt.title('False positivies',fontproperties = 'Times New Roman',fontsize=20)

    if positioni == 1 and positionj == 3:
        plt.ylim(0,1) # y轴范围
        plt.yscale('symlog',linthreshy=0.05*2) # 实现纵坐标刻度的非线性显示
        plt.yticks([0.01,0.05,0.1,0.25,0.5,1.0],['0.01','0.05','0.1','0.25','0.5','1.0'],fontproperties = 'Times New Roman',fontsize=11)
        # x轴标签 固定的位置 标上文本
        
        # plt.xticks([1,2,3,4],['1','1.2','1.6','2'],fontproperties = 'Times New Roman',fontsize=11)
        # 生成水平线
        plt.axhline(y=0.1, xmin=0, xmax=5,color='red')
        plt.axhline(y=0.05, xmin=0, xmax=5,color='grey')
        #plt.xlabel('Noise Rate',fontproperties = 'Times New Roman',fontsize=20)
    else:
        plt.ylim(0,1) # y轴范围
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)

    if positioni == 1:
        plt.xticks([1,2,3,4,5,6],['LiNGAM','DirectLiNGAM','GES','PC','RESIT','SRIT'],
                    fontproperties = 'Times New Roman',fontsize=11,rotation=30)



def PlotFunctionFindRateVariousFunction(y_value,AllrowNum,AllColNum,positioni,positionj,NumberofCompareType):
    '''
        传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
        方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格
    f = plt.boxplot(y_value,positions=[i for i in range(1,NumberofCompareType+1)],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#3B49927F','#EE00007F','#008B457F','#6318797F','#0082807F','#BB00217F','#5F559B7F','#A200567F']  # 颜色代码列表
    
    # ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']
    #8081807F,#1B19197F
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positionj == 0:
        plt.title('Linear',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 1:
        plt.title('Quadratic',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 2:
        plt.title('Exponential',fontproperties = 'Times New Roman',fontsize=20)

    plt.ylim(0,1) # y轴范围

    # plt.xticks([1,2,3,4,5],['0.01','0.05','0.1','0.2','0.4'],fontproperties = 'Times New Roman',fontsize=11)
    plt.xticks([1,2,3,4,5],['0.1','0.2','0.5','1','2'],fontproperties = 'Times New Roman',fontsize=11)
    # plt.xticks([1,2,3,4],['1','1.2','1.6','2'],fontproperties = 'Times New Roman',fontsize=11)
    if positionj == 0:
        plt.ylabel('Coorect Functional\n Model Found Rate',fontproperties = 'Times New Roman',fontsize=20)
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])


# 绘制函数发现率
def PlotFunctionFindRate(y_value,y_value1,y_value3,AllrowNum,AllColNum,positioni,positionj):
    '''
        传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
        方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('seaborn-deep') # 设置风格
    plt.boxplot(y_value,positions=[1,2.25,3.5,4.75],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    # 在同一个图上绘制多个箱型图
    plt.boxplot(y_value1,positions=[0.75,2,3.25,4.5],patch_artist=True,showmeans=True,
                boxprops={"facecolor": "#FFBE7A","edgecolor": "#FFBE7A","linewidth": 0.5},
                medianprops={"color": "black", "linewidth": 2},
                meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                widths = 0.2) # 注意显示平均值时，线段和图形不一样
    plt.boxplot(y_value3,positions=[1.25,2.5,3.75,5],patch_artist=True,showmeans=True,
                boxprops={"facecolor": "#FA7F6F","edgecolor": "#FA7F6F","linewidth": 0.5},
                medianprops={"color": "black", "linewidth": 2},
                meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                widths = 0.2) # 注意显示平均值时，线段和图形不一样
    plt.axvline(x=1.625, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    plt.axvline(x=2.875, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    plt.axvline(x=4.125, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positionj == 0:
        plt.title('Linear',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 1:
        plt.title('Quadratic',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 2:
        plt.title('Exponential',fontproperties = 'Times New Roman',fontsize=20)

    plt.ylim(0,1) # y轴范围

    plt.xticks([1,2.25,3.5,4.75],['0.05','0.1','0.3','0.5'],fontproperties = 'Times New Roman',fontsize=11)

    if positionj == 0:
        plt.ylabel('Coorect Functional\n Model Found Rate',fontproperties = 'Times New Roman',fontsize=20)
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])

# 计算真假阳性率
def CalculatePositiveNegative(ReslutsPath,Sheet,MethodName,NumberofCompareType): 
    # AllNegtiveNum不应当只传入一个数值
    '''
    传入 文件地址  sheetname 要计算真假阳性的方法 所有假阳性值
    返回 分函数的真阳性率 假阳性率
    '''
    DFResults = pd.read_excel(ReslutsPath,Sheet)
    DFResultsReal = DFResults['Real']
    DFResultsRealNegative = DFResults['negative']
    DFResultsMethod = DFResults[MethodName]
    # 不同的情况个数 需要修改这个地方
    CompareType = list() # 中间过程 可以任意命名
    for TempI in range(NumberofCompareType):
        CompareType.append(str(TempI+1))
    
    CalculatedMethod = copy.deepcopy(DFResultsMethod) # 要计算的方法
    # AllNegtiveNum = (4*5-5)*50 #所有的假阳性值
    PositveNumf1df = pd.DataFrame(columns=CompareType) 
    PositveNumf2df = pd.DataFrame(columns=CompareType) 
    PositveNumf3df = pd.DataFrame(columns=CompareType) 
    NegativeNumdf = pd.DataFrame(columns=CompareType) 

    colj = -1
    for row in CalculatedMethod:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue

        PositveNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        PositveNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        PositveNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        NegativeNumdf.loc[rowi,CompareType[colj]] = int(row.split(' ')[4])
        rowi += 1
    # print(NegativeNumdf)

    # 获取真实的不同函数形式的连接个数
    RealNumf1df = pd.DataFrame(columns=CompareType) 
    RealNumf2df = pd.DataFrame(columns=CompareType) 
    RealNumf3df = pd.DataFrame(columns=CompareType) 
    Negativedf = pd.DataFrame(columns=CompareType) 
    
    # 获取真实连接
    colj = -1
    for row in DFResultsReal:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue

        RealNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        RealNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        RealNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        rowi += 1

    # 获取全部的假阳性个数
    # print(DFResultsRealNegative)
    colj = -1
    for row in DFResultsRealNegative:
        # 不同类别
        if '_' in str(row):
            rowi = 0
            colj += 1
            continue

        Negativedf.loc[rowi,CompareType[colj]] = int(row)
        rowi += 1
    # print(Negativedf)
    PositveNumf1Rate = PositveNumf1df.values/RealNumf1df.values
    PositveNumf2Rate = PositveNumf2df.values/RealNumf2df.values
    PositveNumf3Rate = PositveNumf3df.values/RealNumf3df.values
    NegativeRate = NegativeNumdf.values/Negativedf.values
    return PositveNumf1Rate,PositveNumf2Rate,PositveNumf3Rate,NegativeRate



# 计算真假阳性率
def CalculatePositiveNegativeOnlySRIT(ReslutsPath,Sheet,TestName,NumberofCompareType): 
    # AllNegtiveNum不应当只传入一个数值
    '''
    传入 文件地址  sheetname 要计算真假阳性的方法 所有假阳性值
    返回 分函数的真阳性率 假阳性率
    '''
    DFResults = pd.read_excel(ReslutsPath,Sheet)
    DFResultsReal = DFResults['Real']
    DFResultsRealNegative = DFResults['negative']
    DFResultsMethod = DFResults[TestName]
    # 不同的情况个数 需要修改这个地方
    CompareType = list() # 中间过程 可以任意命名
    for TempI in range(NumberofCompareType):
        CompareType.append(str(TempI+1))
    
    CalculatedMethod = copy.deepcopy(DFResultsMethod) # 要计算的方法
    # AllNegtiveNum = (4*5-5)*50 #所有的假阳性值
    PositveNumf1df = pd.DataFrame(columns=CompareType) 
    PositveNumf2df = pd.DataFrame(columns=CompareType) 
    PositveNumf3df = pd.DataFrame(columns=CompareType) 
    NegativeNumdf = pd.DataFrame(columns=CompareType) 

    colj = -1
    for row in CalculatedMethod:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue

        PositveNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        PositveNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        PositveNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        NegativeNumdf.loc[rowi,CompareType[colj]] = int(row.split(' ')[4])
        rowi += 1
    # print(NegativeNumdf)

    # 获取真实的不同函数形式的连接个数
    RealNumf1df = pd.DataFrame(columns=CompareType) 
    RealNumf2df = pd.DataFrame(columns=CompareType) 
    RealNumf3df = pd.DataFrame(columns=CompareType) 
    Negativedf = pd.DataFrame(columns=CompareType) 
    
    # 获取真实连接
    colj = -1
    for row in DFResultsReal:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue

        RealNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        RealNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        RealNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        rowi += 1

    # 获取全部的假阳性个数
    # print(DFResultsRealNegative)
    colj = -1
    for row in DFResultsRealNegative:
        # 不同类别
        if '_' in str(row):
            rowi = 0
            colj += 1
            continue

        Negativedf.loc[rowi,CompareType[colj]] = int(row)
        rowi += 1
    # print(Negativedf)
    PositveNumf1Rate = PositveNumf1df.values/RealNumf1df.values
    PositveNumf2Rate = PositveNumf2df.values/RealNumf2df.values
    PositveNumf3Rate = PositveNumf3df.values/RealNumf3df.values
    NegativeRate = NegativeNumdf.values/Negativedf.values
    return PositveNumf1Rate,PositveNumf2Rate,PositveNumf3Rate,NegativeRate

# 计算真假阳性率 更改为适合多种不同函数形式的样式
def CalculatePositiveNegativeVariousFunction(ReslutsPath,Sheet,TestName,NumberofCompareType): 
    # AllNegtiveNum不应当只传入一个数值
    '''
    传入 文件地址  sheetname 要计算真假阳性的方法 所有假阳性值
    返回 分函数的真阳性率 假阳性率
    '''
    DFResults = pd.read_excel(ReslutsPath,Sheet)
    DFResultsReal = DFResults[TestName+'_Real']
    DFResultsRealNegative = DFResults['negative']
    DFResultsMethod = DFResults[TestName]
    # 不同的情况个数 需要修改这个地方
    CompareType = list() # 中间过程 可以任意命名
    for TempI in range(NumberofCompareType):
        CompareType.append(str(TempI+1))
    
    CalculatedMethod = copy.deepcopy(DFResultsMethod) # 要计算的方法
    # AllNegtiveNum = (4*5-5)*50 #所有的假阳性值
    PositveNumf1df = pd.DataFrame(columns=CompareType) 
    PositveNumf2df = pd.DataFrame(columns=CompareType) 
    NegativeNumdf = pd.DataFrame(columns=CompareType) 

    colj = -1
    # print(CalculatedMethod)
    for row in CalculatedMethod:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue
        # print(row.split(' '))
        PositveNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        PositveNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        NegativeNumdf.loc[rowi,CompareType[colj]] = int(row.split(' ')[3])
        rowi += 1
    # print(NegativeNumdf)

    # 获取真实的不同函数形式的连接个数
    RealNumf1df = pd.DataFrame(columns=CompareType) 
    RealNumf2df = pd.DataFrame(columns=CompareType) 
    RealNumf3df = pd.DataFrame(columns=CompareType) 
    Negativedf = pd.DataFrame(columns=CompareType) 
    
    # 获取真实连接
    colj = -1
    
    for row in DFResultsReal:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue
        
        RealNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        RealNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        rowi += 1

    # 获取全部的假阳性个数
    # print(DFResultsRealNegative)
    colj = -1
    for row in DFResultsRealNegative:
        # 不同类别
        if '_' in str(row):
            rowi = 0
            colj += 1
            continue

        Negativedf.loc[rowi,CompareType[colj]] = int(row)
        rowi += 1
    # print(Negativedf)
    PositveNumf1Rate = PositveNumf1df.values/RealNumf1df.values
    PositveNumf2Rate = PositveNumf2df.values/RealNumf2df.values

    NegativeRate = NegativeNumdf.values/Negativedf.values
    # print(PositveNumf1df)
    # print(PositveNumf2df)
    # print(NegativeNumdf)
    return PositveNumf1Rate,PositveNumf2Rate,NegativeRate


# 计算真假阳性率 更改为适合多种不同函数形式的样式
def CalculatePositiveNegativeAllFunction(ReslutsPath,Sheet,TestName,NumberofCompareType): 
    # AllNegtiveNum不应当只传入一个数值
    '''
    传入 文件地址  sheetname 要计算真假阳性的方法 所有假阳性值
    返回 分函数的真阳性率 假阳性率
    '''
    DFResults = pd.read_excel(ReslutsPath,Sheet)
    DFResultsReal = DFResults['Real']
    DFResultsRealNegative = DFResults['negative']
    DFResultsMethod = DFResults['all']
    # 不同的情况个数 需要修改这个地方
    CompareType = list() # 中间过程 可以任意命名
    for TempI in range(NumberofCompareType):
        CompareType.append(str(TempI+1))
    
    CalculatedMethod = copy.deepcopy(DFResultsMethod) # 要计算的方法
    # AllNegtiveNum = (4*5-5)*50 #所有的假阳性值
    PositveNumf1df = pd.DataFrame(columns=CompareType) 
    PositveNumf2df = pd.DataFrame(columns=CompareType) 
    PositveNumf3df = pd.DataFrame(columns=CompareType) 
    PositveNumf4df = pd.DataFrame(columns=CompareType) 
    PositveNumf5df = pd.DataFrame(columns=CompareType) 
    PositveNumf6df = pd.DataFrame(columns=CompareType) 
    PositveNumf7df = pd.DataFrame(columns=CompareType) 
    NegativeNumdf = pd.DataFrame(columns=CompareType) 

    colj = -1
    # print(CalculatedMethod)
    for row in CalculatedMethod:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue
        # print(row.split(' '))
        PositveNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        PositveNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        PositveNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        PositveNumf4df.loc[rowi,CompareType[colj]] = int(row.split(' ')[3])
        PositveNumf5df.loc[rowi,CompareType[colj]] = int(row.split(' ')[4])
        PositveNumf6df.loc[rowi,CompareType[colj]] = int(row.split(' ')[5])
        PositveNumf7df.loc[rowi,CompareType[colj]] = int(row.split(' ')[6])
        NegativeNumdf.loc[rowi,CompareType[colj]] = int(row.split(' ')[7])
        rowi += 1
    # print(NegativeNumdf)

    # 获取真实的不同函数形式的连接个数
    RealNumf1df = pd.DataFrame(columns=CompareType) 
    RealNumf2df = pd.DataFrame(columns=CompareType) 
    RealNumf3df = pd.DataFrame(columns=CompareType) 
    RealNumf4df = pd.DataFrame(columns=CompareType) 
    RealNumf5df = pd.DataFrame(columns=CompareType) 
    RealNumf6df = pd.DataFrame(columns=CompareType) 
    RealNumf7df = pd.DataFrame(columns=CompareType) 
    Negativedf = pd.DataFrame(columns=CompareType) 
    
    # 获取真实连接
    colj = -1
    
    for row in DFResultsReal:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue
        
        RealNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        RealNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        RealNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        RealNumf4df.loc[rowi,CompareType[colj]] = int(row.split(' ')[3])
        RealNumf5df.loc[rowi,CompareType[colj]] = int(row.split(' ')[4])
        RealNumf6df.loc[rowi,CompareType[colj]] = int(row.split(' ')[5])
        RealNumf7df.loc[rowi,CompareType[colj]] = int(row.split(' ')[6])
        rowi += 1

    # 获取全部的假阳性个数
    # print(DFResultsRealNegative)
    colj = -1
    for row in DFResultsRealNegative:
        # 不同类别
        if '_' in str(row):
            rowi = 0
            colj += 1
            continue

        Negativedf.loc[rowi,CompareType[colj]] = int(row)
        rowi += 1
    # print(Negativedf)
    PositveNumf1Rate = PositveNumf1df.values/RealNumf1df.values
    PositveNumf2Rate = PositveNumf2df.values/RealNumf2df.values
    PositveNumf3Rate = PositveNumf3df.values/RealNumf3df.values
    PositveNumf4Rate = PositveNumf4df.values/RealNumf4df.values
    PositveNumf5Rate = PositveNumf5df.values/RealNumf5df.values
    PositveNumf6Rate = PositveNumf6df.values/RealNumf6df.values
    PositveNumf7Rate = PositveNumf7df.values/RealNumf7df.values
    NegativeRate = NegativeNumdf.values/Negativedf.values


    return PositveNumf1Rate,PositveNumf2Rate,PositveNumf3Rate,\
        PositveNumf4Rate,PositveNumf5Rate,PositveNumf6Rate,PositveNumf7Rate,NegativeRate


# 计算函数发现率
def CalculateFunctionAllFunction(DFFunctionNum,TestName):
    '''
    传入 正确函数发现个数 正确连接发现的个数
    返回 分函数的真阳性率 假阳性率
    '''

    FunctionFound = copy.deepcopy(DFFunctionNum[TestName]) # 正确函数发现个数
    LinksFound = copy.deepcopy(DFFunctionNum[TestName+'_'])

    # AllNegtiveNum = (4*5-5)*50 #所有的假阳性值
    PositveNumf1df = pd.DataFrame(columns=['1']) 
    PositveNumf2df = pd.DataFrame(columns=['1']) 
    PositveNumf3df = pd.DataFrame(columns=['1']) 
    PositveNumf4df = pd.DataFrame(columns=['1']) 
    PositveNumf5df = pd.DataFrame(columns=['1']) 
    PositveNumf6df = pd.DataFrame(columns=['1']) 
    PositveNumf7df = pd.DataFrame(columns=['1']) 
    rowi = 0
    for row in FunctionFound:
        # print(row)
        PositveNumf1df.loc[rowi,'1'] = int(row.split(' ')[0])
        PositveNumf2df.loc[rowi,'1'] = int(row.split(' ')[1])
        PositveNumf3df.loc[rowi,'1'] = int(row.split(' ')[2])
        PositveNumf4df.loc[rowi,'1'] = int(row.split(' ')[3])
        PositveNumf5df.loc[rowi,'1'] = int(row.split(' ')[4])
        PositveNumf6df.loc[rowi,'1'] = int(row.split(' ')[5])
        PositveNumf7df.loc[rowi,'1'] = int(row.split(' ')[6])
        rowi += 1
    # print(NegativeNumdf)

    # 获取真实的不同函数形式的连接个数
    RealNumf1df = pd.DataFrame(columns=['1']) 
    RealNumf2df = pd.DataFrame(columns=['1']) 
    RealNumf3df = pd.DataFrame(columns=['1']) 
    RealNumf4df = pd.DataFrame(columns=['1']) 
    RealNumf5df = pd.DataFrame(columns=['1']) 
    RealNumf6df = pd.DataFrame(columns=['1']) 
    RealNumf7df = pd.DataFrame(columns=['1']) 
    rowi = 0
    for row in LinksFound:
        # 不同类别
        RealNumf1df.loc[rowi,'1'] = int(row.split(' ')[0])
        RealNumf2df.loc[rowi,'1'] = int(row.split(' ')[1])
        RealNumf3df.loc[rowi,'1'] = int(row.split(' ')[2])
        RealNumf4df.loc[rowi,'1'] = int(row.split(' ')[3])
        RealNumf5df.loc[rowi,'1'] = int(row.split(' ')[4])
        RealNumf6df.loc[rowi,'1'] = int(row.split(' ')[5])
        RealNumf7df.loc[rowi,'1'] = int(row.split(' ')[6])
        rowi += 1

    PositveNumf1Rate = PositveNumf1df.values/RealNumf1df.values
    PositveNumf2Rate = PositveNumf2df.values/RealNumf2df.values
    PositveNumf3Rate = PositveNumf3df.values/RealNumf3df.values
    PositveNumf4Rate = PositveNumf4df.values/RealNumf4df.values
    PositveNumf5Rate = PositveNumf5df.values/RealNumf5df.values
    PositveNumf6Rate = PositveNumf6df.values/RealNumf6df.values
    PositveNumf7Rate = PositveNumf7df.values/RealNumf7df.values

    return PositveNumf1Rate,PositveNumf2Rate,PositveNumf3Rate,\
        PositveNumf4Rate,PositveNumf5Rate,PositveNumf6Rate,PositveNumf7Rate



# 计算函数发现率
def CalculateFunctionFindRate(DFCorrectFunctionNum,DFCorrectLinksNum,NumberofCompareType):
    '''
    传入 正确函数发现个数 正确连接发现的个数
    返回 分函数的真阳性率 假阳性率
    '''

    CompareType = list() # 中间过程 可以任意命名
    for TempI in range(NumberofCompareType):
        CompareType.append(str(TempI+1))
    CalculatedMethod = copy.deepcopy(DFCorrectFunctionNum[0]) # 正确函数发现个数
    # AllNegtiveNum = (4*5-5)*50 #所有的假阳性值
    PositveNumf1df = pd.DataFrame(columns=CompareType) 
    PositveNumf2df = pd.DataFrame(columns=CompareType) 
    PositveNumf3df = pd.DataFrame(columns=CompareType) 

    colj = -1
    for row in CalculatedMethod:
        # print(row)
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue

        PositveNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        PositveNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        PositveNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        rowi += 1
    # print(NegativeNumdf)

    # 获取真实的不同函数形式的连接个数
    RealNumf1df = pd.DataFrame(columns=CompareType) 
    RealNumf2df = pd.DataFrame(columns=CompareType) 
    RealNumf3df = pd.DataFrame(columns=CompareType) 

    colj = -1
    for row in DFCorrectLinksNum:
        # 不同类别
        if '_' in row:
            rowi = 0
            colj += 1
            continue

        RealNumf1df.loc[rowi,CompareType[colj]] = int(row.split(' ')[0])
        RealNumf2df.loc[rowi,CompareType[colj]] = int(row.split(' ')[1])
        RealNumf3df.loc[rowi,CompareType[colj]] = int(row.split(' ')[2])
        rowi += 1

    PositveNumf1Rate = PositveNumf1df.values/RealNumf1df.values
    PositveNumf2Rate = PositveNumf2df.values/RealNumf2df.values
    PositveNumf3Rate = PositveNumf3df.values/RealNumf3df.values

    return PositveNumf1Rate,PositveNumf2Rate,PositveNumf3Rate


# 计算函数发现率
def CalculateFunctionvariousFunction(DFFunctionNum,TestName):
    '''
    传入 正确函数发现个数 正确连接发现的个数
    返回 分函数的真阳性率 假阳性率
    '''

    FunctionFound = copy.deepcopy(DFFunctionNum[TestName]) # 正确函数发现个数
    LinksFound = copy.deepcopy(DFFunctionNum[TestName+'_'])

    # AllNegtiveNum = (4*5-5)*50 #所有的假阳性值
    PositveNumf1df = pd.DataFrame(columns=['1']) 
    PositveNumf2df = pd.DataFrame(columns=['1']) 

    rowi = 0
    for row in FunctionFound:
        # print(row)
        PositveNumf1df.loc[rowi,'1'] = int(row.split(' ')[0])
        PositveNumf2df.loc[rowi,'1'] = int(row.split(' ')[1])
        rowi += 1
    # print(NegativeNumdf)

    # 获取真实的不同函数形式的连接个数
    RealNumf1df = pd.DataFrame(columns=['1']) 
    RealNumf2df = pd.DataFrame(columns=['1']) 

    rowi = 0
    for row in LinksFound:
        # 不同类别
        RealNumf1df.loc[rowi,'1'] = int(row.split(' ')[0])
        RealNumf2df.loc[rowi,'1'] = int(row.split(' ')[1])
        rowi += 1

    PositveNumf1Rate = PositveNumf1df.values/RealNumf1df.values
    PositveNumf2Rate = PositveNumf2df.values/RealNumf2df.values

    return PositveNumf1Rate,PositveNumf2Rate




# 绘制函数发现率
def PlotFunctionFindRateVariousFunction(y_value,AllrowNum,AllColNum,positioni,positionj,NumberofCompareType):
    '''
        传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
        方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格
    f = plt.boxplot(y_value,positions=[i for i in range(1,NumberofCompareType+1)],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#3B49927F','#EE00007F','#008B457F','#6318797F','#0082807F','#BB00217F','#5F559B7F','#A200567F']  # 颜色代码列表
    
    # ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']
    #8081807F,#1B19197F
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")

    plt.ylim(0,1) # y轴范围

    # plt.xticks([1,2,3,4,5],['0.01','0.05','0.1','0.2','0.4'],fontproperties = 'Times New Roman',fontsize=11)
    # plt.xticks([1,2],['Linear','Square root'],fontproperties = 'Times New Roman',fontsize=11)
    plt.xticks([1,2,3,4,5,6,7],['Linear','Division','Log','Square root','Cosine','Quadratic','Exponential'],\
               fontproperties = 'Times New Roman',fontsize=11,rotation=30)
    # plt.xticks([1,2,3,4],['1','1.2','1.6','2'],fontproperties = 'Times New Roman',fontsize=11)

    # plt.ylabel('Model Found Rate',fontproperties = 'Times New Roman',fontsize=20)
    plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    plt.title('Model found rate',fontproperties = 'Times New Roman',fontsize=20)


# 绘制函数发现率
def PlotFunctionFindRateSI(y_value,AllrowNum,AllColNum,positioni,positionj):
    '''
        传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
        方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格
    f = plt.boxplot(y_value,positions=[1,2,3,4],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#3B49927F','#EE00007F','#008B457F','#6318797F','#0082807F','#BB00217F','#5F559B7F','#A200567F']  # 颜色代码列表
    
    # ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']
    #8081807F,#1B19197F
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positionj == 0:
        plt.title('Linear',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 1:
        plt.title('Quadratic',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 2:
        plt.title('Exponential',fontproperties = 'Times New Roman',fontsize=20)

    plt.ylim(0,1) # y轴范围

    plt.xticks([1,2,3,4],['50','100','200','500'],fontproperties = 'Times New Roman',fontsize=11)
    # plt.xticks([1,2,3,4],['1','1.2','1.6','2'],fontproperties = 'Times New Roman',fontsize=11)
    if positionj == 0:
        plt.ylabel('Coorect Functional\n Model Found Rate',fontproperties = 'Times New Roman',fontsize=20)
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])

# 绘制函数发现率
def PlotFunctionFindRateOnlySRIT(y_value,AllrowNum,AllColNum,positioni,positionj,NumberofCompareType):
    '''
        传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
        方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格
    f = plt.boxplot(y_value,positions=[i for i in range(1,NumberofCompareType+1)],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#3B49927F','#EE00007F','#008B457F','#6318797F','#0082807F','#BB00217F','#5F559B7F','#A200567F']  # 颜色代码列表
    
    # ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']
    #8081807F,#1B19197F
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)
    # plt.axvline(x=1.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=2.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # plt.axvline(x=3.5, ymin=0, ymax=1,color='grey',linewidth=0.5,linestyle='--')
    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positionj == 0:
        plt.title('Linear',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 1:
        plt.title('Quadratic',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 2:
        plt.title('Exponential',fontproperties = 'Times New Roman',fontsize=20)

    plt.ylim(0,1) # y轴范围

    # plt.xticks([1,2,3,4,5],['0.01','0.05','0.1','0.2','0.4'],fontproperties = 'Times New Roman',fontsize=11)
    plt.xticks([1,2,3,4,5],['5','20','30','40','80'],fontproperties = 'Times New Roman',fontsize=11)
    # plt.xticks([1,2,3,4],['1','1.2','1.6','2'],fontproperties = 'Times New Roman',fontsize=11)
    if positionj == 0:
        plt.ylabel('Coorect Functional\n Model Found Rate',fontproperties = 'Times New Roman',fontsize=20)
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])

    
# 绘制主要结果
# 主要结果是高维变量
def PlotRateNumberNodes(y_value,TitleName,AllrowNum,AllColNum,positioni,positionj):
    '''传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
            方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    # plt.style.use('seaborn-deep') # 设置风格
    plt.style.use('bmh') # 设置风格
    
    f = plt.boxplot(y_value,positions=[1,2,3,4,5,6],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#3B49927F','#EE00007F','#008B457F','#6318797F','#0082807F','#BB00217F','#5F559B7F','#A200567F']  # 颜色代码列表
    
    # ['#A40545', '#F46F44', '#FDD985','#E9F5A1', '#7FCBA4', '#4B65AF', '#7FCBA4', '#4B65AF']
    #8081807F,#1B19197F
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)

    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positioni == 0:
        # 标题 pad表示与图像的距离
        plt.title(TitleName,fontproperties = 'Times New Roman',fontsize=20,pad=15)
    if positionj == 0:
        if positioni == 0:
            plt.ylabel('True positivies\n Linear',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 1:
            plt.ylabel('True positivies\n Quadratic',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 2:
            plt.ylabel('True positivies\n Exponential',fontproperties = 'Times New Roman',fontsize=20)
        elif positioni == 3:
            plt.ylabel('False positivies',fontproperties = 'Times New Roman',fontsize=20)
    if positioni == 3:
        plt.ylim(0,1) # y轴范围
        plt.yscale('symlog',linthreshy=0.05*2) # 实现纵坐标刻度的非线性显示
        plt.yticks([0.01,0.05,0.1,0.25,0.5,1.0],['0.01','0.05','0.1','0.25','0.5','1.0'],fontproperties = 'Times New Roman',fontsize=11)
        # x轴标签 固定的位置 标上文本
        plt.xticks([1,2,3,4,5,6],['2','5','10','20','50','100'],fontproperties = 'Times New Roman',fontsize=11)
        # plt.xticks([1,2,3,4,5,6,7,8],['0.05','0.1','0.3','0.5','0.7','0.9','1','2'],fontproperties = 'Times New Roman',fontsize=11)
        # 生成水平线
        plt.axhline(y=0.1, xmin=0, xmax=5,color='red')
        plt.axhline(y=0.05, xmin=0, xmax=5,color='grey')
        #plt.xlabel('Noise Rate',fontproperties = 'Times New Roman',fontsize=20)
    else:
        plt.ylim(0,1) # y轴范围
    
    if positionj == 0:
        
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])

# 绘制函数发现率
# 主要结果是高维变量
def PlotFunctionFindRateNumberNodes(y_value,AllrowNum,AllColNum,positioni,positionj):
    '''
        传入 y的值(箱型图中的散点) 这些散点在x轴上的定位
        方法名 总共需要的行数 列数 当前子图的行位置 列位置'''
    fig = plt.subplot2grid((AllrowNum,AllColNum), (positioni,positionj))
    plt.style.use('bmh') # 设置风格
    f = plt.boxplot(y_value,positions=[1,2,3,4,5,6],patch_artist=True,showmeans=True,
                        boxprops={"facecolor":'#8ECFC9',"edgecolor": "#8ECFC9","linewidth": 0.5},
                        medianprops={"color": "black", "linewidth": 2},
                        meanprops={'marker':'x','markersize':5,"markeredgecolor": "k"},
                        widths = 0.2) # 注意显示平均值时，线段和图形不一样
    c_list = ['#3B49927F','#EE00007F','#008B457F','#6318797F','#0082807F','#BB00217F','#5F559B7F','#A200567F']  # 颜色代码列表
    for box, c in zip(f['boxes'], c_list):  # 对箱线图设置颜色
        box.set(color=c, linewidth=2)
        box.set(facecolor=c)

    # 不显示右边和上边的坐标线
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # 不显示x轴标签
    plt.gca().xaxis.set_ticklabels([])
    # y轴网格线
    plt.grid(axis="y")
    if positionj == 0:
        plt.title('Linear',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 1:
        plt.title('Quadratic',fontproperties = 'Times New Roman',fontsize=20)
    elif positionj == 2:
        plt.title('Exponential',fontproperties = 'Times New Roman',fontsize=20)

    plt.ylim(0,1) # y轴范围
    
    plt.xticks([1,2,3,4,5,6],['2','5','10','20','50','100'],fontproperties = 'Times New Roman',fontsize=11)
    # plt.xticks([1,2,3,4,5,6,7,8],['0.05','0.1','0.3','0.5','0.7','0.9','1','2'],fontproperties = 'Times New Roman',fontsize=11)

    if positionj == 0:
        plt.ylabel('Correct Functional\n Model Found Rate',fontproperties = 'Times New Roman',fontsize=20)
        plt.yticks(fontproperties = 'Times New Roman',fontsize=11)
    else:
        plt.gca().yaxis.set_ticklabels([])


