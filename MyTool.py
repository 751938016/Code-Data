import warnings
warnings.filterwarnings('ignore') 
from pandas.api.types import is_numeric_dtype
import pandas as pd 
import numpy as np
import re
import copy
import os

def GetVariables(function):
    '''输入eureqa找到的某个函数模型
    返回模型中存在的自变量（不局限于x）
    '''
    p1 = r'[a-zA-Z]+[L\d]*'
    a1 = re.findall(p1, function)
    a1 = list(set(a1)) #去除列表中相同的变量
    a1.sort()
    a2 = list()
    for _ in a1: # 去除正则表达式错误找到的e
        if ('e' not in _) and ('log' not in _) and ('cos' not in _):
            a2.append(_)

    return a2

def GetVarNum(functionlist,Threshold = 1):
    '''删除小于Threshold出现次数的变量'''
    # 粗略找到方程中所有的变量名
    varnum = dict()
    sqrtnum = dict()
    #print(functionlist)
    for eachfunction in functionlist:
        #print(eachfunction)
        if '=' in eachfunction:
            eachfunction = eachfunction.split("=")[1]
        varlist = GetVariables(eachfunction)
        for eachvar in varlist:
            
            if '^' in eachvar:
                mi = eachvar.split('^')
                addition = int(mi[1]) - 1 # 需要加上的等于高次方减一乘以出现的总次数
                if mi[0] in sqrtnum: # 可能会存在多种高次方
                    sqrtnum[mi[0]] += addition
                else:
                    sqrtnum[mi[0]] = addition
            
            else:
                if eachvar not in varnum:
                    varnum[eachvar] = 1
                else:
                    varnum[eachvar] += 1
    
    #为所有变量加上高次方项
    for eachvar in sqrtnum:
        if eachvar in varnum:
            varnum[eachvar] += sqrtnum[eachvar]
        else:
            varnum[eachvar] = sqrtnum[eachvar]
    
    FewVar = list()
    for eachvar in varnum:
        if varnum[eachvar] <=Threshold:
            FewVar.append(eachvar)

    return varnum,FewVar

def DelOverFitModel(dfModel,Threshold):
    '''传入保存的模型数据
        返回剪枝过的模型'''
    dfModel.sort_values('error',ascending=False,inplace=True,ignore_index=True) # 按照error降序
    ttdf = pd.DataFrame(columns=['complexity','error','function']) # 初始化保存Dataframe
    for i in range(1,dfModel.shape[0]):
        EvsC = (dfModel.iloc[i,1] - dfModel.iloc[i-1,1])/(dfModel.iloc[i,0] - dfModel.iloc[i-1,0])
        if abs(EvsC) >= Threshold:
            aa = dfModel.iloc[i,:]
            aa = pd.DataFrame(aa.values.reshape((1,3)),columns=['complexity','error','function'])
            ttdf = ttdf.append(aa,ignore_index=True)
    return ttdf


# 按加号划分函数模型
def SplitFunctionByPlus(TestStr):
    '''传入去除等号的函数模型
    返回按加号划分的列表'''
    TestStr = TestStr.replace('-','+')
    TestStr = TestStr.replace('e+','e-')
    SplitByPlus = TestStr.split('+')
    i = 0
    SplitByPlusFinal = list()
    MisTermIndex = list()
    for eachSplit in SplitByPlus:
        TempeachSplit = copy.deepcopy(eachSplit)

        if i in MisTermIndex:
            i += 1
            continue
        
        AllRigth = eachSplit.count('(')
        AllLeft = eachSplit.count(')')
        if AllRigth != AllLeft:
            for j in range(i+1,len(SplitByPlus)):
                AllRigth += SplitByPlus[j].count('(')
                AllLeft += SplitByPlus[j].count(')')
                TempeachSplit += '+'
                TempeachSplit += SplitByPlus[j]
                MisTermIndex.append(j)
                if AllRigth == AllLeft:
                    break
            SplitByPlusFinal.append(TempeachSplit)
        else:
            SplitByPlusFinal.append(eachSplit)
        i += 1
    return SplitByPlusFinal


def DelSmallParamaters(TestStr,Par_Thereshold):
    '''传入需要处理的模型 和 系数的阈值'''
    for EachTerm in SplitFunctionByPlus(TestStr):
        if '*' in EachTerm:
            if float(EachTerm.split('*')[0].replace(' ',''))<Par_Thereshold:
                TempStr = '+' + EachTerm
                TestStr = TestStr.replace(TempStr,'')
    return TestStr

# 删除一些复杂的情况
# 包括 复杂相乘 函数嵌套
def AdvanceDelComplexModel(dfModel,DropSmallParmatersTerm=True):
    ttdf = pd.DataFrame(columns=['complexity','error','function']) # 初始化保存Dataframe
    AllComplexOpation = ['sin','cos','exp','^'] #删除函数嵌套 
    for i in range(0,dfModel.shape[0]):

        SplitResults = SplitFunctionByPlus(dfModel.iloc[i,2].split('=')[1])
        Temp = 0
        TempDiv = 0
        for eachSplit in SplitResults:
            CountOpation = 0

            CountVar = 0 # 如果存在复杂相乘 那么每个项中存在变量的个数一定大于1
            for eachOpation in AllComplexOpation:
                CountOpation += eachSplit.count(eachOpation)
            for eachVaribles in GetVariables(eachSplit):
                if 'x' in eachVaribles:
                    CountVar += eachSplit.count(eachVaribles)
            # 不去除函数嵌套和小系数 再查看结果
            if (CountOpation > 1) or (CountVar>1):# 删除出现两次以上操作符或者两个以上乘号
                Temp = 1
                break
            if (CountVar>1) and ('/' not in eachSplit):# 删除出现两次以上操作符或者两个以上乘号
                Temp = 1
                break
            # 如果是个除法，则允许函数嵌套的情况
            if (CountVar>1) and ('/' in eachSplit):
                Temp = 0
        
        if Temp == 1: 
            continue
        else:
            aa = dfModel.iloc[i,:]
            aa = pd.DataFrame(aa.values.reshape((1,3)),columns=['complexity','error','function'])
            # 删除模型中系数小的项
            if DropSmallParmatersTerm:
                # aa['function'] = DelSmallParamaters(aa['function'][0],Par_Thereshold)
                if 'e-' in aa['function'][0]:
                    continue
            ttdf = ttdf.append(aa,ignore_index=True)  

    return ttdf

def GetResidual(EachEquation,dfData,Target):
    EachEquation = EachEquation.split('=')[1]
    EachEquation = EachEquation.replace(' ','')
    EachEquation = EachEquation.replace('^','**')
    EachEquation = EachEquation.replace('sin','np.sin')
    EachEquation = EachEquation.replace('exp','np.exp')
    EachEquation = EachEquation.replace('cos','np.cos')
    EachEquation = EachEquation.replace('log','np.log')
    try:
        float(EachEquation)
        return 0
    except:
        pass

    # 首先按照变量的下标进行排序 大下标在前面
    VarwithSubscriptDict = dict()
    for EachIndependetVar in GetVariables(EachEquation):
        if 'x' not in EachIndependetVar:
            continue
        else:
            VarwithSubscriptDict[EachIndependetVar] = int(EachIndependetVar[1:])
    for VarName,Subscript in sorted(VarwithSubscriptDict.items(), key=lambda item:item[1], reverse=True):

        TempStr = copy.deepcopy(VarName.replace('x','X'))
        TempStr = 'dfData["'+TempStr+'"]'
        EachEquation = EachEquation.replace(VarName,TempStr)
    # 最后再将X替换为x
    EachEquation = EachEquation.replace('X','x')

    # 计算方程的残差
    TempTargetValue = copy.deepcopy(dfData[Target])
    if not is_numeric_dtype(TempTargetValue):
        TempTargetValue = pd.to_numeric(TempTargetValue)
    # EachEquation = Rep(EachEquation, ReplaceDict)
    Target_hat = eval(EachEquation)
    residual =  TempTargetValue - Target_hat
    return residual


# 以字典的形式，获取每个因变量的连接自变量
def getvarlist(FunctionCol):
    '''传入方程列'''
    varlist = list()
    for eachfunction in FunctionCol:
        eachfunction = eachfunction.split('=')[1]
        try: float(eachfunction);continue
        except: 
            variables = GetVariables(eachfunction)
            varlist += variables
    varlist = list(set(varlist))
    return varlist


# 根据发现模型的提升/复杂，筛选模型
def GetConnection(SRFileName,FilterByModels=True,FilterByNumber=False,
                    Threshold1=0.1,Threshold2=1,DelInter=True):

    xl = pd.ExcelFile(SRFileName)
    connection = dict()
    
    for target in xl.sheet_names:
        if 'L' in target:
            break

        dfModel = pd.read_excel(SRFileName,sheet_name=target,
                           header=None,names=['complexity','error','function'])
        dfModel = dfModel.dropna()
        # 删除相乘
        if DelInter == True:
            dfModel = AdvanceDelComplexModel(dfModel)
        # 根据模型的提升比率进行筛选
        if FilterByModels == True:
            ModelDF = DelOverFitModel(dfModel,Threshold1)
            TempList = getvarlist(ModelDF['function'])
        else:
            TempList = getvarlist(dfModel['function'])
        
        # 根据变量出现的次数进行筛选
        if FilterByNumber == True:

            if FilterByModels == True:
                _,FewVar = GetVarNum(ModelDF['function'],Threshold2)
            else:
                _,FewVar = GetVarNum(dfModel['function'],Threshold2)
            
            for eee22 in FewVar:
                TempList.remove(eee22)
        
        connection[target] = TempList # 根据符号回归方程获取连接字典
    return connection
##################################################################################
############################### 小工具 ###########################################

# 建立一个文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path) 
    else: pass

# 使用字典对字符串中的多个字符进行替换
def Rep(str1, dict_rep):
    '''传入需要替换的字符串 替换规则字典'''
    for i in dict_rep:
        str1 = str1.replace(i,dict_rep[i])
    return str1

# 根据字典的值获取排序之后的列表（从小到大）
def DictGenSortedList(OriginDict):
    '''传入原始字典 返回列表'''
    MinValue = min(OriginDict.values())
    TempList = list()
    TempDict = copy.deepcopy(OriginDict)
    while 1:
        for Key,Value in TempDict.items():
            if Value == MinValue:
                TempList.append(Key)
                del TempDict[Key]
                if len(TempDict) > 0:
                    MinValue = min(TempDict.values())
                break
        if len(TempList) == len(OriginDict):
            break
    return TempList


# 对符号回归发现的模型中 分子上和幂的数字进行四舍五入
def ReplaceNumerator(str1):
    p1 = r'\d+\.+\d+/'
    a1 = re.findall(p1, str1)
    templist = list(set(a1))

    ReplaceIntList = dict()
    for each in templist:
        Tempeach = copy.deepcopy(each.replace('/',''))
        try:
            Tempeach = np.around(float(Tempeach),decimals=0) # 四舍五入
            ReplaceIntList[each.replace('/','')] = str(int(Tempeach))
        except:
            print('正则表达式错误找到了：')
            print(each)
            raise ValueError

    for keys,values in ReplaceIntList.items():
        str1 = str1.replace(keys,values)

    return str1

def ReplacePower(str1):
    p1 = r'\^\d+\.+\d+'
    a1 = re.findall(p1, str1)
    templist = list(set(a1))

    ReplaceIntList = dict()
    for each in templist:
        Tempeach = copy.deepcopy(each.replace('^',''))
        try:
            if float(Tempeach) > 1:
                Tempeach = np.around(float(Tempeach),decimals=0) # 四舍五入
                ReplaceIntList[each.replace('^','')] = str(int(Tempeach))
            else:
                Tempeach = np.around(float(Tempeach),decimals=1) # 四舍五入
                ReplaceIntList[each.replace('^','')] = str(Tempeach)
        except:
            print('正则表达式错误找到了：')
            print(each)
            raise ValueError

    for keys,values in ReplaceIntList.items():
        str1 = str1.replace(keys,values)

    return str1
