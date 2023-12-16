from autoEureqa import *
from TwoStep import *
'''首先对所有数据运行SR'''

# 针对外生变量 重新运行第二步 查看是否可以帮助修剪错误的因果关系
NumNodes = 10
Length = 500
noiserate = 0.1 # 0.05,0.1,0.3,0.5
CrossDegree = 1
NumberofNetworks = 11
NumberofDatasets = 51
TotalRootPath = 'C:/Users/dell/Desktop/mycode'
RunTime = 30

for noiserate in [0.05,0.1,0.3,0.5]:
    StartofNetwork = 1

    RunType = '密度'+str(CrossDegree) +'_数据量'+str(Length)+'_变量数'+str(NumNodes)+'_噪声'+str(noiserate) 
    print(RunType)


    for eachNetworks in range(StartofNetwork,NumberofNetworks):
        print(eachNetworks)
        # 原始数据保存目录
        path = TotalRootPath+'/Data/人工数据/密度'+str(CrossDegree) \
                +'_数据量'+str(Length)+'_变量数'+str(NumNodes)+'_噪声'+str(noiserate) \
                +'/Networks' + str(eachNetworks) + '/'
        # 创建符号回归的保存目录
        sspath = TotalRootPath+'/Data/人工数据/密度'+str(CrossDegree) \
                +'_数据量'+str(Length)+'_变量数'+str(NumNodes)+'_噪声'+str(noiserate) \
                +'_符号回归/Networks' + str(eachNetworks) + '/'
        
        Step1path = TotalRootPath+'/Data/人工数据/密度'+str(CrossDegree) \
                +'_数据量'+str(Length)+'_变量数'+str(NumNodes)+'_噪声'+str(noiserate) \
                +'_Step1/Networks' + str(eachNetworks) + '/'
        mkdir(Step1path)

        # 创建步骤2结果的保存目录
        Step2path = TotalRootPath+'/Data/人工数据/密度'+str(CrossDegree) \
                +'_数据量'+str(Length)+'_变量数'+str(NumNodes)+'_噪声'+str(noiserate) \
                +'_Step2/Networks' + str(eachNetworks) + '/'
             
        # 创建最终符号回归的保存路径
        FinalResultsPath = sspath + '/FinalResults/'

        # 创建定向过程的保存路径
        PairChose = sspath + '/PairChose/'
        mkdir(PairChose)
         # 获取网络的连接字典
        LinksSave = path + 'NetworksLinksDict.npy'
        LinksSaveDict = np.load(LinksSave,allow_pickle=True).tolist()

        StartofGraph = 1
        for jj in range(StartofGraph,51):
            # 读取真实数据
            input_file = path + 'Graph'+str(jj)+'.txt'
            TempDf = pd.read_csv(input_file)
            
            # 保存要包含单数索引列 不能是双数 否则使用txt打开会是乱码
            TempDf.to_csv(input_file,float_format='%.5f')
            TempDf = pd.read_csv(input_file)
            # 读入数据并且删除索引列
            UnNamedColum = list()
            for eeeach in TempDf .columns:
                if 'Unnam' in eeeach:
                    UnNamedColum.append(eeeach)
            # 如果数据中的索引列大于等于2
            # 那么删除所有索引列 并且重新保存一份（只含有一个索引列）
            if len(UnNamedColum) >= 2:
                TempDf.drop(UnNamedColum,axis=1,inplace=True)
                TempDf.to_csv(input_file,float_format='%.5f')
            else:
                TempDf.drop(UnNamedColum,axis=1,inplace=True)

            # 将数据拷到eureqa
            AutoAddData(input_file)

            FunctionSave = path + 'Graph'+str(jj)+'Function.npy' # 真实的模型
            FunctionDict = np.load(FunctionSave,allow_pickle=True).tolist()

            Step2Results = dict()
            Step2pathEachRemove = Step2path + '/Graph'+str(jj)+'_EachRomve/'
            # 获取之前运行的内生变量的第一步
            Step1InnerEquationDict = np.load(Step1path + 'Graph'+str(jj)+'_Step1FunctionList.npy',allow_pickle=True).tolist()
            EquationDict = copy.deepcopy(Step1InnerEquationDict)

            '''步骤一''' # 只针对运行错误的外生变量
            for eachTarget in TempDf.columns:

                if 'Unnam' in eachTarget:
                    continue

                # 初次运行的符号回归结构
                ResultsPath = sspath + 'Graph'+str(jj)+'_'+eachTarget+'.txt'
                with open(ResultsPath,'w') as f:
                    pass

                Expression = GetTargetExpression(eachTarget,TempDf.columns)
                AutoEureqa(Expression, ResultsPath, RunTime = RunTime)                

                TempEquationlist1,AllIndependentVar = Step1(ResultsPath,TempDf,eachTarget,Thereshold=0.1,
                                                            DropSmallParmatersTerm=True)
                EquationDict[eachTarget] = TempEquationlist1

            # 第一步结束之后 判断是否存在未定向的因果邻接
            '''中间步 定向步'''
            UnorientedPairs,FinnalStep1LinksDict = GetUnorientedPairsForExo(EquationDict)
            #print(UnorientedPairs)

            for target,eachParent in UnorientedPairs:
                # 方向1上的结果
                ResultsPair1 = PairChose + 'Graph'+str(jj) + '_'+eachParent+'-'+target+'.txt'
                with open(ResultsPair1,'w') as f:
                    pass
                Expression = GetTargetExpression(target,[eachParent]) # 
                AutoEureqa(Expression, ResultsPair1, RunTime = RunTime)

                # 方向2上的结果
                ResultsPair2 = PairChose + 'Graph'+str(jj) + '_'+target+'-'+eachParent+'.txt'
                with open(ResultsPair2,'w') as f:
                    pass
                Expression = GetTargetExpression(eachParent,[target])
                AutoEureqa(Expression, ResultsPair2, RunTime = RunTime)

                dfModel1 = pd.read_csv(ResultsPair1,sep='\t',header=None,names=['complexity','error','function'])
                dfModel2 = pd.read_csv(ResultsPair2,sep='\t',header=None,names=['complexity','error','function'])
                
                Direction1 = round(JudgementUnoriented(dfModel1,TempDf,target),3) # 选择保留两个方向中更独立的方向
                #print(eachParent+'->'+target+':'+str(Direction1))
                Direction2 = round(JudgementUnoriented(dfModel2,TempDf,eachParent),3)
                #print(target+'->'+eachParent+':'+str(Direction2))
                if Direction1 < Direction2:
                    FinnalStep1LinksDict[eachParent].remove(target)
                elif Direction1 > Direction2:
                    FinnalStep1LinksDict[target].remove(eachParent)
                else:
                    continue

            '''步骤二'''
            Step2Results = dict()
            ClearFinalResult(FinalResultsPath,'Graph'+str(jj))
            for targetVar,EquationlistStep1 in FinnalStep1LinksDict.items():
                # 所有的方程中都含有子节点，这是一个外生变量
                if len(EquationlistStep1) == 0:
                    continue

                Step2Results[targetVar] = Step2(targetVar,EquationlistStep1,TempDf,Step2pathEachRemove,LinksSaveDict,
                                            Thereshold=0.1,num_resamples=500,DropSmallParmatersTerm=True,RunTime=RunTime)  

                '''步骤三'''# 最后 根据获取的变量列表 进行最后的符号回归拟合
                # 经过剪枝之后没有父节点 也是外生变量
                if len(Step2Results[targetVar]) == 0:
                    continue

                FinalResultsSave = FinalResultsPath + 'Graph'+str(jj)+'_'+targetVar+'.txt'

                with open(FinalResultsSave,'w') as f:
                    pass

                FinalfunctionPRE = GetTargetExpression(targetVar,Step2Results[targetVar])
                AutoEureqa(FinalfunctionPRE, FinalResultsSave, RunTime)

