import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import seaborn as sns


def random_flips():
    random_float=random.random()
    if random_float < 0.5:
        return '正'
    else:
        return '反'


def simulate_coin_flip(candidate_1,candidate_2):
    candidate_1['wincount']=[]      #存放8轮实验中赢的次数
    candidate_1['average_throws_when_win']=[]   #8轮中平均获胜需要的抛硬币次数
    candidate_2['wincount']=[]
    candidate_2['average_throws_when_win']=[]

    for Round in range(8):  #8轮重复实验
        # 为列表开辟存储空间
        candidate_1['wincount'].append(0)    
        candidate_1['average_throws_when_win'].append(0) 
        candidate_2['wincount'].append(0)  
        candidate_2['average_throws_when_win'].append(0)  


        for n in range(100000):  #10万次模拟实验
            queue=[]
            len=0
            while(1):
                queue.append(random_flips())
                len+=1
                if len<3:
                    continue
                else:
                    Last_three=queue[len-3]+queue[len-2]+queue[len-1]     #这里看看能否得到正确的最后三个

                    if Last_three==candidate_1['queue']:
                        candidate_1['wincount'][Round]+=1
                        candidate_1['average_throws_when_win'][Round]+=len
                        break
                    if Last_three==candidate_2['queue']:
                        candidate_2['wincount'][Round]+=1
                        candidate_2['average_throws_when_win'][Round]+=len
                        break
                    
        if candidate_1['wincount'][Round]:
            candidate_1['average_throws_when_win'][Round]/=candidate_1['wincount'][Round]
        if candidate_2['wincount'][Round]:
            candidate_2['average_throws_when_win'][Round]/=candidate_2['wincount'][Round]

    return candidate_1['wincount'], candidate_1['average_throws_when_win'], candidate_2['wincount'], candidate_2['average_throws_when_win']


if __name__=='__main__':
    candidates=['正正正','正正反','正反正','正反反','反正正','反正反','反反正','反反反' ]
    result_set={}
    all_results = {}  # 保存用于t检验和方差分析的数据
    for i in range(8):
        result_set[candidates[i]]={}    # 作为字典使用得先声明字典
    # 创建统计结果的存储结构
    all_mean_var = []    

    for i in range(8):
        candidate_1={}
        candidate_1['queue']=candidates[i]

        for j in range(i+1,8):            
            candidate_2={}
            candidate_2['queue']=candidates[j]

            result_list=simulate_coin_flip(candidate_1,candidate_2)
            # 对总共取个平均值
            result_set[candidate_1['queue']][candidate_2['queue']]=[]
            result_set[candidate_1['queue']][candidate_2['queue']]=result_list
            result_set[candidate_2['queue']][candidate_1['queue']]=[]
            result_set[candidate_2['queue']][candidate_1['queue']]=[result_list[2],result_list[3],result_list[0],result_list[1]]
            #all_results[(candidate_1['queue'], candidate_2['queue'])] = (result_list[0], result_list[2])        #
            mean_1 = np.mean(result_list[0])
            var_1 = np.var(result_list[0])
            mean_2 = np.mean(result_list[2])
            var_2 = np.var(result_list[2])

            # 保存统计信息
            all_mean_var.append([candidate_1['queue'], candidate_2['queue'], mean_1, var_1, mean_2, var_2])

    # 保存统计信息到 CSV 表格
    df_statistics = pd.DataFrame(all_mean_var, columns=['候选1', '候选2', '候选1均值', '候选1方差', '候选2均值', '候选2方差'])
    df_statistics.to_csv('C:\\Users\\hejiyun\\Desktop\\不要删的文件\\作业\\python\\fig_of_flip_coins\\统计结果.csv', index=False)
    print(result_set)
    # 这里绘制的是每个类别与其它类别的比较柱状图

    # 使用中文支持的字体
    rcParams['font.sans-serif'] = ['SimHei']  # 在 Windows 上使用
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


    for candidate,dataset in result_set.items():    #此处dataset为candidate对应的字典
        other_candidates=[other for other in dataset.keys()]  #此处的的other_data为candidate与other产生的比较数据列表
        
        values_candidate=[sum(other_data[0])/8 for  other_data in dataset.values()]    #candidate的平均获胜次数
        values_other_candidates=[sum(other_data[2])/8 for other_data in dataset.values()] #other_candidate的平均获胜次数

        bar_width=0.35

        index=np.arange(len(other_candidates))

        plt.figure(figsize=(10,6))

        bars1=plt.bar(index, values_candidate, width=bar_width, label=candidate, color='skyblue')

        bars2=plt.bar(index+bar_width, values_other_candidates,width=bar_width, label='待选方案', color='salmon')

        # 在柱子上方添加数值标记
        for bar in bars1:
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # X 位置：柱子的中心
                bar.get_height(),  # Y 位置：柱子的高度
                f'{bar.get_height():.0f}',  # 显示数值
                ha='center',  # 水平对齐方式
                va='bottom'  # 垂直对齐方式
            )

        for bar in bars2:
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # X 位置：柱子的中心
                bar.get_height(),  # Y 位置：柱子的高度
                f'{bar.get_height():.0f}',  # 显示数值
                ha='center',  # 水平对齐方式
                va='bottom'  # 垂直对齐方式
            )
        

        plt.xticks(index+bar_width/2, other_candidates)

        plt.title(f"'{candidate}'与其它待选方案比较")
        plt.xlabel('待选方案')
        plt.ylabel('10万次实验平均获胜次数')
        plt.legend()
        plt.savefig(f'C:\\Users\\hejiyun\\Desktop\\不要删的文件\\作业\\python\\fig_of_flip_coins\\{candidate}与其它方案比较.png')
        #plt.show()
    # 绘制热力图    
    for candidate, dataset in result_set.items():
        heatmap_data = []
        other_candidates = [other for other in dataset.keys()]
        for other in other_candidates:
            values_candidate = sum(dataset[other][0]) / 8  # candidate的平均胜率
            values_other = sum(dataset[other][2]) / 8  # other_candidate的平均胜率
        
            # 计算与 candidate 的获胜概率比率
            win_ratio = values_other / values_candidate if values_candidate != 0 else 0
            heatmap_data.append([win_ratio])

        # 将当前 candidate 的值设置为 1
        heatmap_df = pd.DataFrame(heatmap_data, index=other_candidates, columns=None)
    
        # 创建热力图
        plt.figure(figsize=(6, 8))
        sns.heatmap(heatmap_df, annot=True, cmap="YlGnBu", fmt=".2f", 
                cbar_kws={'label': f"相对胜率比 ('{candidate}' 默认为 1)"})
        plt.title(f"'{candidate}'与其它方案的相对胜率比热力图")
        plt.ylabel('待选方案')
        plt.savefig(f'C:\\Users\\hejiyun\\Desktop\\不要删的文件\\作业\\python\\fig_of_flip_coins\\{candidate}与其它方案热力图.png')
