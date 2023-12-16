# 读取数据
from autoEureqa import *
from TwoStep import *

TotalRootPath = 'D:/工作/函数因果模型1121/code/MyCodeFinal/Data/现实数据/tam-technology-acceptance-model/'
DataFileName = "因子分析之后的数据.xlsx"


# TotalRootPath = 'D:/工作/函数因果模型1121/code/MyCodeFinal/Data/现实数据/GSS_spss/'
# DataFileName = "处理之后的数据2.xlsx"


df = pd.read_excel(TotalRootPath+DataFileName)
n = df.shape[0]

nbootstraps = 500
RunTime = 300
RunTimeDelUnoriented = 300
Step2RunTime = 300
FinalRunTime = 300
Thereshold = 0.1
for b in range(1,nbootstraps):
    print('bootstrap' + str(b)+'.......')
    # 创建符号回归的保存目录
    sspath = TotalRootPath+'符号回归/'
    mkdir(sspath)
    # 创建最终符号回归的保存路径
    FinalResultsPath = sspath + '/FinalResults/'
    mkdir(FinalResultsPath)

    # 创建步骤1结果的保存目录
    Step1path = TotalRootPath+'Step1/'
    mkdir(Step1path)

    # 创建步骤2结果的保存目录
    Step2path = TotalRootPath+'Step2/'
    mkdir(Step2path)

    # 每一轮保存的bootstrap数据
    DataSave = TotalRootPath + 'bootstrap' + str(b) + '.txt'
    # 随机有放回的抽取与原数据相同大小的数据
    train_idxs = np.random.choice(range(n), size = n, replace = True)
    tempdf = df.iloc[list(train_idxs),:]

    # 在bootstrap数据上进行因果发现
    tempdf = tempdf.apply(lambda x:(x-np.min(x))/(np.max(x)-np.min(x)))
    tempdf.to_csv(DataSave,index=False,float_format='%.5f')

    # 步骤一结果保存地址
    Step1Save = Step1path + 'bootstrap' + str(b) + '_Step1FunctionList.npy'
    # 将数据拷到eureqa
    AutoAddData(DataSave)
    EquationDictStep1 = dict()
    for eachTarget in tempdf.columns:

        ResultsPath = sspath + 'bootstrap' + str(b) + '_'+eachTarget+'.txt'
        with open(ResultsPath,'w') as f:
            pass
        Expression = GetTargetExpression(eachTarget,tempdf.columns)
        AutoEureqa(Expression, ResultsPath, RunTime = RunTime)

        '''步骤一'''###################################################
        ###############################################################
        MinIndependentEquation = Step1ForRealWorld(ResultsPath,tempdf,eachTarget,Thereshold=Thereshold,
                                                DropSmallParmatersTerm=True,num_resamples=500)
        
        EquationDictStep1[eachTarget] = MinIndependentEquation
        #print(MinIndependentParents)
    np.save(Step1Save,EquationDictStep1)
    #print(EquationDictStep1)
    Step2pathEachRemove = Step2path+ 'bootstrap' + str(b) + '_EachRomve/'
    mkdir(Step2pathEachRemove)


    UnorientedPairs,FinnalStep1LinksDict = GetUnorientedPairs(EquationDictStep1)

    for target,eachParent in UnorientedPairs:
        # 方向1上的结果
        ResultsPair1 = sspath + 'bootstrap' + str(b) + '_'+eachParent+'-'+target+'.txt'
        with open(ResultsPair1,'w') as f:
            pass
        Expression = GetTargetExpression(target,[eachParent]) # 
        AutoEureqa(Expression, ResultsPair1, RunTime = RunTimeDelUnoriented)

        # 方向2上的结果
        ResultsPair2 = sspath + 'bootstrap' + str(b) + '_'+target+'-'+eachParent+'.txt'
        with open(ResultsPair2,'w') as f:
            pass
        Expression = GetTargetExpression(eachParent,[target])
        AutoEureqa(Expression, ResultsPair2, RunTime = RunTimeDelUnoriented)

        dfModel1 = pd.read_csv(ResultsPair1,sep='\t',header=None,names=['complexity','error','function'])
        dfModel2 = pd.read_csv(ResultsPair2,sep='\t',header=None,names=['complexity','error','function'])
        
        Direction1 = round(JudgementUnoriented(dfModel1,tempdf,target),3)
        #print(eachParent+'->'+target+':'+str(Direction1))
        Direction2 = round(JudgementUnoriented(dfModel2,tempdf,eachParent),3)
        #print(target+'->'+eachParent+':'+str(Direction2))
        if Direction1 < Direction2:
            FinnalStep1LinksDict[eachParent].remove(target)
        elif Direction1 > Direction2:
            FinnalStep1LinksDict[target].remove(eachParent)
        else:
            print(1)
            continue


    Step2Results = dict()
    for targetVar,Step1EstimatedParents in FinnalStep1LinksDict.items():
        # 所有的方程中都含有子节点，这是一个外生变量
        if len(Step1EstimatedParents) == 0:
            continue

        Step2Results[targetVar] = Step2(targetVar,Step1EstimatedParents,tempdf,Step2pathEachRemove,RunTime=Step2RunTime,
                                        Thereshold=Thereshold,num_resamples=500,DropSmallParmatersTerm=True,)                
        '''步骤三'''# 最后 根据获取的变量列表 进行最后的符号回归拟合
        # 没有父节点 也是外生变量
        if len(Step2Results[targetVar]) == 0:
            continue

        FinalResultsSave = FinalResultsPath + 'bootstrap' + str(b) + '_' + targetVar + '.txt'
        with open(FinalResultsSave,'w') as f:
            pass

        FinalfunctionPRE = GetTargetExpression(targetVar,Step2Results[targetVar])
        AutoEureqa(FinalfunctionPRE, FinalResultsSave, FinalRunTime)

    Step2ResultsSavePath = Step2path + 'bootstrap' + str(b) + '_Step2FinalList.npy'
    print(Step2Results)
    np.save(Step2ResultsSavePath,Step2Results)









