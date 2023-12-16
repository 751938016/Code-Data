from cdt.data import load_dataset
from autoEureqa import *
from TwoStep import *

t_data, t_labels = load_dataset('tuebingen')

for jj in range(1,100):
    TotalRootPath = 'D:/工作/函数因果模型1121/code/mycode/Data/现实数据/因果对/pair'+str(jj)+'/'
    mkdir(TotalRootPath)
    df = pd.DataFrame()
    df['x1'] = list(t_data['A']['pair1'])
    df['x2'] = list(t_data['B']['pair1'])
    DataFileName = "data.xlsx"
    df.to_excel(TotalRootPath+DataFileName,index=False)
    

    df = pd.read_excel(TotalRootPath+DataFileName)
    n = df.shape[0]

    #nbootstraps = 500
    RunTimeDelUnoriented = 30
    Thereshold = 0.01

    b = 0
    # for b in range(nbootstraps):

    # 创建符号回归的保存目录
    sspath = TotalRootPath+'符号回归/'
    mkdir(sspath)
    # 创建最终符号回归的保存路径
    FinalResultsPath = sspath + '/FinalResults/'
    mkdir(FinalResultsPath)
    # 定向过程结果的保存路径
    PairChose = sspath + '/PairChose/'
    mkdir(PairChose)

    # 每一轮保存的bootstrap数据
    DataSave = TotalRootPath + 'bootstrap' + str(b) + '.txt'
    # 随机有放回的抽取与原数据相同大小的数据
    train_idxs = np.random.choice(range(n), size = n, replace = True)
    tempdf = df.iloc[list(train_idxs),:]
    tempdf.to_csv(DataSave,index=False,float_format='%.5f')

    # 将数据拷到eureqa
    AutoAddData(DataSave)

    # x1->x2
    ResultsPair1 = PairChose + 'Graph'+str(jj) + '_x1-x2.txt'
    with open(ResultsPair1,'w') as f:
        pass
    Expression = GetTargetExpression('x2',['x1']) # 第一个参数是因变量
    AutoEureqa(Expression, ResultsPair1, RunTime = RunTimeDelUnoriented)

    # x2->x1
    ResultsPair2 = PairChose + 'Graph'+str(jj) + '_x2-x1.txt'
    with open(ResultsPair2,'w') as f:
        pass
    Expression = GetTargetExpression('x1',['x2'])
    AutoEureqa(Expression, ResultsPair2, RunTime = RunTimeDelUnoriented)

    dfModel1 = pd.read_csv(ResultsPair1,sep='\t',header=None,names=['complexity','error','function'])
    dfModel2 = pd.read_csv(ResultsPair2,sep='\t',header=None,names=['complexity','error','function'])
    
    Direction1 = round(JudgementUnoriented(dfModel1,tempdf,'x2'),3)
    #print(eachParent+'->'+target+':'+str(Direction1))
    Direction2 = round(JudgementUnoriented(dfModel2,tempdf,'x1'),3)
    #print(target+'->'+eachParent+':'+str(Direction2))
    # 相关系数越小 越独立 更应该被保存
    if Direction1 < Direction2: # 保存x1->x2
        print('x1->x2')
    elif Direction1 > Direction2: # 保存x2->x1
        print('x2->x1')
    else:
        continue