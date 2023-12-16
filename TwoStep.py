from autoEureqa import *
from MyTool import *
from hsic import hsic_test_gamma


def Step1(ResultsPath,dfData,target,Thereshold=0.1,DropSmallParmatersTerm=True):
    '''传入
            符号回归保存文件 数据文件 目标变量 p值上限 是否删除小模型 独立性测试中的参数(太大运行慢 太小似乎不准确)
       返回
            Step1后剩余的模型列表    Step1后模型中存在的自变量列表'''
    dfModel = pd.read_csv(ResultsPath,sep='\t',
                            header=None,names=['complexity','error','function'])

    dfModel = dfModel.dropna()
    # 删除一些复杂的情况 包括 复杂相乘 函数嵌套
    dfModel = AdvanceDelComplexModel(dfModel,DropSmallParmatersTerm) # 现在删除小系数是直接删除含有e的模型

    TempEquationlist1 = list() # Step1后剩余的模型
    IndependentVarEachModel = list() # Step1后模型中存在的自变量
    DescentNodeList = list() # 存储

    for EachEquation in dfModel['function']:

        # 跳过只有一个常数的模型
        try: 
            float(EachEquation.split('=')[1])
            continue
        except:pass

        residual = GetResidual(EachEquation,dfData,target)
        #print(2)
    # STEP1 判断每一个方程残差与自变量的独立性 删除所有相关的方程 （删除了所有含有子节点的模型）
        IndependentList = GetVariables(EachEquation.split('=')[1])
        #print(IndependentList)
        hsic_stat, hsic_p = hsic_test_gamma(residual.values, dfData[IndependentList].values)
        # 保存完全独立的函数模型
        #print(hsic_p)
        if hsic_p <= Thereshold:
            continue
        else:
            TempEquationlist1.append(EachEquation)
            IndependentVarEachModel.append(IndependentList)
        
    AllIndependentVar = list(set(sum(IndependentVarEachModel, []))) # 所有模型中存在的自变量
    return TempEquationlist1,AllIndependentVar


def Step2(targetVar,EquationlistStep1,dfData,Step2path,LinksSaveDict,Thereshold=0.1,num_resamples=500,DropSmallParmatersTerm=True,RunTime = 30):
    '''传入
            版本1 第一步获取的模型字典 原始数据列表 运行时间 保存路路径 是否删除小模型 
            版本2 循环在外部做 现在是针对一个目标变量和其函数列表进行的测试
        返回
            '''

        
    FullVarNum,FewVar = GetVarNum(EquationlistStep1,Threshold=1)
    SortedList = DictGenSortedList(FullVarNum) # 变量出现次数从小到大排列
 
    TempVarList = copy.deepcopy(SortedList)
    

    for EachParent in SortedList:
        if len(TempVarList) == 1:
            hsic_stat, hsic_p = hsic_test_gamma(dfData[targetVar].values,dfData[TempVarList[0]].values)
            if hsic_p > Thereshold:
                TempVarList = []
            break
        # 在某次内部循环中没有出现的自变量 不参与接下来的循环
        # 删除某一个父节点 
        if EachParent in TempVarList:
            TempVarList.remove(EachParent)
        else:
            continue
        # 使用autoeureqa
        functionPRE = GetTargetExpression(targetVar,TempVarList)
        # print(functionPRE)
        # 创建一个空的文本文件以存储结果
        ResultsPath = Step2path + targetVar + '_Remove_' + EachParent + '.txt'
        with open(ResultsPath,'w') as f:
            pass

        AutoEureqa(functionPRE, ResultsPath, RunTime)

        # 独立性判断过程
        dfResults = pd.read_csv(ResultsPath,sep='\t',
                                header=None,names=['complexity','error','function'])
        dfResults = dfResults.dropna()
        dfResults = AdvanceDelComplexModel(dfResults,DropSmallParmatersTerm) # 现在删除小系数是直接删除含有e的模型
        # 在某次内部循环中没有出现的自变量 不参与接下来的循环
        FullVarNum,FewVar = GetVarNum(dfResults['function'],Threshold=0)
        TempVarList = copy.deepcopy(list(FullVarNum.keys()))
        #print(TempVarList)
        tempp = 0
        for EachEquation in dfResults['function']:
            #print(EachEquation)
            residual = GetResidual(EachEquation,dfData,targetVar)
            try: 
                float(residual)
                continue
            except:pass
            hsic_stat, hsic_p = hsic_test_gamma(residual.values,dfData[EachParent].values)

            if hsic_p > Thereshold: 
                tempp = 1 # tempp=1则删除该变量
                break

        if tempp == 0: #如果是真父节点则添加回去
            TempVarList.append(EachParent)

    return TempVarList

def Step1ForRealWorld(ResultsPath,dfData,target,Thereshold=0.1,DropSmallParmatersTerm=True,num_resamples=500):
    '''传入
            符号回归保存文件 数据文件 目标变量 p值上限 是否删除小模型 独立性测试中的参数(太大运行慢 太小似乎不准确)
       返回
            Step1后剩余的模型列表    Step1后模型中存在的自变量列表'''
    # dfModel = pd.read_csv(ResultsPath,sep='\t',
    #                         header=None,names=['complexity','error','function'])
    # 真实世界数据是由pandas直接保存的 所以不用
    dfModel = pd.read_csv(ResultsPath,header=None,names=['complexity','error','function'])   

    dfModel = dfModel.dropna()
    # 删除一些复杂的情况 包括 复杂相乘 函数嵌套
    dfModel = AdvanceDelComplexModel(dfModel,DropSmallParmatersTerm) # 现在删除小系数是直接删除含有e的模型

    return list(dfModel['function'])

# 对双向因果的判断
def JudgementUnoriented(dfModel,dfData,target):
    '''计算任意一个符号回归保存结果的最小相关系数
    传入 符号回归保存的结果 原始数据Dataframe 目标变量
    返回所有模型中最小的相关系数'''
    IndependentMeasureValueList = list()
    IndependentMeasureP_valueList = list()
    for EachEquation in dfModel['function']:
        #print(EachEquation)
        # 跳过只有一个常数的模型
        try: 
            float(EachEquation.split('=')[1])
            continue
        except:pass

        residual = GetResidual(EachEquation,dfData,target)
        #print(2)
        # STEP1 判断每一个方程残差与自变量的独立性 删除所有相关的方程 （删除了所有含有子节点的模型）
        tempp = 0
        IndependentList = list()
        for each in GetVariables(EachEquation.split('=')[1]):
            if 'x' in each:
                IndependentList.append(each)
        
        # RESIT中是使用hsic的值来衡量独立性水平 越小 越独立
        #print(IndependentList)
        hsic_stat, hsic_p = hsic_test_gamma(residual.values, dfData[IndependentList].values)
        #print(hsic_p)
        IndependentMeasureValueList.append(hsic_stat)
        IndependentMeasureP_valueList.append(hsic_p)
    if len(IndependentMeasureValueList)==0:
        return -99
    else:
        return min(IndependentMeasureValueList)
    #print(IndependentMeasureValueDict)
    
def GetUnorientedPairsForExo(EquationDict):
    '''
        传入 因变量 自变量对应的函数列表
        返回 去除exp sin等错误的变量列表 找到的未定向的边
    '''
    LinksDict = dict()
    for targetVar,IndependentEquationList in EquationDict.items():
        FullVarNum,FewVar = GetVarNum(IndependentEquationList,Threshold=1)
        LinksDict[targetVar] = list(FullVarNum.keys())
    
    # 去除错误的exp sin 等
    FinnalLinksDict = dict()
    for target,EstimatedParentList in LinksDict.items():
        # 初始化
        FinnalLinksDict[target] = list()
        for eachParent in EstimatedParentList:
            if 'x' in eachParent:
                FinnalLinksDict[target].append(eachParent)
            
    UnorientedPair = list()

    for target,EstimatedParentList in FinnalLinksDict.items():
        for eachParent in EstimatedParentList:
            if eachParent in FinnalLinksDict:
                if target in FinnalLinksDict[eachParent]:
                    if (eachParent,target) not in UnorientedPair:
                        UnorientedPair.append((target,eachParent))

    UnorientedPair = list(set(UnorientedPair))
    return UnorientedPair,FinnalLinksDict

def GetUnorientedPairs(EquationDictStep1):
    StepLinksDict = dict()
    for targetVar,MinIndependentEquation in EquationDictStep1.items():
        EquationlistStep1 = [MinIndependentEquation[0]]
        FullVarNum,FewVar = GetVarNum(EquationlistStep1,Threshold=1)
        StepLinksDict[targetVar] = list(FullVarNum.keys())
    FinnalStep1LinksDict = dict()
    for target,EstimatedParentList in StepLinksDict.items():
        FinnalStep1LinksDict[target] = list()
        for eachParent in EstimatedParentList:
            if 'x' in eachParent:
                FinnalStep1LinksDict[target].append(eachParent)
            
    UnorientedPair = list()

    for target,EstimatedParentList in FinnalStep1LinksDict.items():
        for eachParent in EstimatedParentList:
            if eachParent in FinnalStep1LinksDict:
                if target in FinnalStep1LinksDict[eachParent]:
                    if (eachParent,target) not in UnorientedPair:
                        UnorientedPair.append((target,eachParent))
                    
    UnorientedPair = list(set(UnorientedPair))
    return UnorientedPair,FinnalStep1LinksDict

# 清空之前运行结果的小程序
def ClearFinalResult(RootFinalPath,GraphName):
    '''
    传入 最终结果的保存路径 需要删除的数据集图名
    '''
    aa = os.listdir(RootFinalPath)
    for EachFile in aa:
        if GraphName in EachFile:
            os.remove(RootFinalPath+EachFile)