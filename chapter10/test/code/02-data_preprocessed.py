# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
data = pd.read_excel('../data/original_data.xls')
print('��ʼ״̬��������״Ϊ��', data.shape)
# ɾ����ˮ����š�����ˮ��������ģʽ����
data.drop(labels = ["��ˮ�����","����ˮ��","����ģʽ"],axis = 1,inplace = True) 
print('ɾ�������������������״Ϊ��', data.shape)
data.to_csv('../tmp/water_heart.csv',index = False)



import pandas as pd
import numpy as np
# ��ȡ����
data = pd.read_csv('../tmp/water_heart.csv')
# ������ˮ�¼�
threshold = pd.Timedelta('4 min')  # ��ֵΪ4����
data['����ʱ��'] = pd.to_datetime(data['����ʱ��'], format = '%Y%m%d%H%M%S')  # ת��ʱ���ʽ
data = data[data['ˮ����'] > 0]  # ֻҪ��������0�ļ�¼
sjKs = data['����ʱ��'].diff() > threshold  # ����ʱ����ǰ��֣��Ƚ��Ƿ������ֵ
sjKs.iloc[0] = True  # ���һ��ʱ��Ϊ��һ����ˮ�¼��Ŀ�ʼ�¼�
sjJs = sjKs.iloc[1:]  # ����ֵĽ��
sjJs = pd.concat([sjJs,pd.Series(True)])  # �����һ��ʱ����Ϊ���һ����ˮ�¼��Ľ���ʱ��
# �������ݿ򣬲�������ˮ�¼�����
sj = pd.DataFrame(np.arange(1,sum(sjKs)+1),columns = ["�¼����"])
sj["�¼���ʼ���"] = data.index[sjKs == 1]+1  # ������ˮ�¼�����ʼ���
sj["�¼���ֹ���"] = data.index[sjJs == 1]+1  # ������ˮ�¼�����ֹ���
print('����ֵΪ4���ӵ�ʱ���¼���ĿΪ��',sj.shape[0])
sj.to_csv('../tmp/sj.csv',index = False)



# ȷ��������ˮ�¼�ʱ����ֵ
n = 4  # ʹ���Ժ��ĸ����ƽ��б��
threshold = pd.Timedelta(minutes = 5)  # ר����ֵ
data['����ʱ��'] = pd.to_datetime(data['����ʱ��'], format = '%Y%m%d%H%M%S')
data = data[data['ˮ����'] > 0]  # ֻҪ��������0�ļ�¼
# �Զ��庯�������뻮��ʱ���ʱ����ֵ���õ����ֵ��¼���
def event_num(ts):
    d = data['����ʱ��'].diff() > ts  # ����ʱ������֣��Ƚ��Ƿ������ֵ
    return d.sum() + 1  # ����ֱ�ӷ����¼���
dt = [pd.Timedelta(minutes = i) for i in np.arange(1, 9, 0.25)]
h = pd.DataFrame(dt, columns = ['��ֵ'])  # ת�����ݿ򣬶�����ֵ��
h['�¼���'] = h['��ֵ'].apply(event_num)  # ����ÿ����ֵ��Ӧ���¼���
h['б��'] = h['�¼���'].diff()/0.25  # ����ÿ�������ڵ��Ӧ��б��
h['б��ָ��']= h['б��'].abs().rolling(4).mean()  # ��ǰȡn��б�ʾ���ֵƽ����Ϊб��ָ��
ts = h['��ֵ'][h['б��ָ��'].idxmin() - n]
# ��idxmin������Сֵ��Index������rolling_mean()�������ǰn��б�ʵľ���ֵƽ��
# ���Խ��Ҫ����ƽ�ƣ�-n��
if ts > threshold:
    ts = pd.Timedelta(minutes = 4)
print('������ĵ�����ˮʱ������ֵΪ��',ts)



import pandas as pd 
import numpy as np

data = pd.read_excel('../data/water_hearter.xlsx',encoding = 'gbk')  # ��ȡ��ˮ��ʹ�����ݼ�¼
sj = pd.read_csv('../tmp/sj.csv',encoding = 'utf-8')  # ��ȡ��ˮ�¼���¼

# ת��ʱ���ʽ
data["����ʱ��"] = pd.to_datetime(data["����ʱ��"],format = "%Y%m%d%H%M%S")

# ��������������ˮʱ��
timeDel = pd.Timedelta("1 sec")
sj["�¼���ʼʱ��"] = data.iloc[sj["�¼���ʼ���"]-1,0].values- timeDel
sj["�¼�����ʱ��"] = data.iloc[sj["�¼���ֹ���"]-1,0].values + timeDel
sj['ϴԡʱ���'] = [i.hour for i in sj["�¼���ʼʱ��"]]
sj["����ˮʱ��"] = np.int64(sj["�¼�����ʱ��"] - sj["�¼���ʼʱ��"])/1000000000 

# ������ˮͣ���¼�
# ����������ͣ�ٿ�ʼʱ�䡱����ͣ�ٽ���ʱ�䡱
# ͣ�ٿ�ʼʱ��ָ����ˮ������ˮ����ͣ�ٽ���ʱ��ָ����ˮ������ˮ��
for i in range(len(data)-1):
    if (data.loc[i,"ˮ����"] != 0) & (data.loc[i + 1,"ˮ����"] == 0) :
        data.loc[i + 1,"ͣ�ٿ�ʼʱ��"] = data.loc[i +1, "����ʱ��"] - timeDel
    if (data.loc[i,"ˮ����"] == 0) & (data.loc[i + 1,"ˮ����"] != 0) :
        data.loc[i,"ͣ�ٽ���ʱ��"] = data.loc[i , "����ʱ��"] + timeDel
        
# ��ȡͣ�ٿ�ʼʱ�������ʱ������Ӧ�кţ��������ݿ�Stop��
indStopStart = data.index[data["ͣ�ٿ�ʼʱ��"].notnull()]+1
indStopEnd = data.index[data["ͣ�ٽ���ʱ��"].notnull()]+1
Stop = pd.DataFrame(data = {"ͣ�ٿ�ʼ���":indStopStart[:-1],
                            "ͣ�ٽ������":indStopEnd[1:]}) 
# ����ͣ��ʱ�������������ݿ�stop�У�ͣ��ʱ��=ͣ�ٽ���ʱ��-ͣ�ٽ���ʱ��
Stop["ͣ��ʱ��"] = np.int64(data.loc[indStopEnd[1:]-1,"ͣ�ٽ���ʱ��"].values-
                     data.loc[indStopStart[:-1]-1,"ͣ�ٿ�ʼʱ��"].values)/1000000000
# ��ÿ��ͣ�����¼�ƥ��,ͣ�ٵĿ�ʼʱ��Ҫ�����¼��Ŀ�ʼʱ�䣬
# ��ͣ�ٵĽ���ʱ��ҪС���¼��Ľ���ʱ��
for i in range(len(sj)):
    Stop.loc[(Stop["ͣ�ٿ�ʼ���"] > sj.loc[i,"�¼���ʼ���"]) & 
           (Stop["ͣ�ٽ������"] < sj.loc[i,"�¼���ֹ���"]),"ͣ�ٹ����¼�"] = i+1
             
# ɾ��ͣ�ٴ���Ϊ0���¼�
Stop = Stop[Stop["ͣ�ٹ����¼�"].notnull()]

# �������� ��ˮ�¼�ͣ����ʱ����ͣ�ٴ�����ͣ��ƽ��ʱ����
# ��ˮʱ������ˮ/��ʱ��
stopAgg =  Stop.groupby("ͣ�ٹ����¼�").agg({"ͣ��ʱ��":sum,"ͣ�ٿ�ʼ���":len})
sj.loc[stopAgg.index - 1,"��ͣ��ʱ��"] = stopAgg.loc[:,"ͣ��ʱ��"].values
sj.loc[stopAgg.index-1,"ͣ�ٴ���"] = stopAgg.loc[:,"ͣ�ٿ�ʼ���"].values
sj.fillna(0,inplace=True)  # ��ȱʧֵ��0�岹
stopNo0 = sj["ͣ�ٴ���"] != 0  # �ж���ˮ�¼��Ƿ����ͣ��
sj.loc[stopNo0,"ƽ��ͣ��ʱ��"] = sj.loc[stopNo0,"��ͣ��ʱ��"]/sj.loc[stopNo0,"ͣ�ٴ���"] 
sj.fillna(0,inplace=True)  # ��ȱʧֵ��0�岹
sj["��ˮʱ��"] = sj["����ˮʱ��"] - sj["��ͣ��ʱ��"]  # ����������ˮʱ��
sj["��ˮ/��ʱ��"] = sj["��ˮʱ��"] / sj["����ˮʱ��"]  # �������� ��ˮ/��ʱ��
print('��ˮ�¼���ˮʱ����Ƶ������������ɺ����ݵ�����Ϊ��\n',sj.columns)
print('��ˮ�¼���ˮʱ����Ƶ������������ɺ����ݵ�ǰ5��5������Ϊ��\n',
      sj.iloc[:5,:5])



data["ˮ����"] = data["ˮ����"] / 60 # ԭ��λL/min����ת��ΪL/sec
sj["����ˮ��"] = 0 # ������ˮ����һ����ʼֵ0
for i in range(len(sj)):
    Start = sj.loc[i,"�¼���ʼ���"]-1
    End = sj.loc[i,"�¼���ֹ���"]-1
    if Start != End:
        for j in range(Start,End):
            if data.loc[j,"ˮ����"] != 0:
                sj.loc[i,"����ˮ��"] = (data.loc[j + 1,"����ʱ��"] - 
                                    data.loc[j,"����ʱ��"]).seconds* \
                                    data.loc[j,"ˮ����"] + sj.loc[i,"����ˮ��"]
        sj.loc[i,"����ˮ��"] = sj.loc[i,"����ˮ��"] + data.loc[End,"ˮ����"] * 2
    else:
        sj.loc[i,"����ˮ��"] = data.loc[Start,"ˮ����"] * 2
        
sj["ƽ��ˮ����"] = sj["����ˮ��"] / sj["��ˮʱ��"] # �������� ƽ��ˮ����
# ����������ˮ��������
# ˮ��������=��(((����ˮ����ֵ-ƽ��ˮ����)^2)*����ʱ��)/��ˮʱ��
sj["ˮ��������"] = 0 # ��ˮ����������һ����ʼֵ0
for i in range(len(sj)):
    Start = sj.loc[i,"�¼���ʼ���"] - 1
    End = sj.loc[i,"�¼���ֹ���"] - 1
    for j in range(Start,End + 1):
        if data.loc[j,"ˮ����"] != 0:
            slbd = (data.loc[j,"ˮ����"] - sj.loc[i,"ƽ��ˮ����"])**2
            slsj = (data.loc[j + 1,"����ʱ��"] - data.loc[j,"����ʱ��"]).seconds
            sj.loc[i,"ˮ��������"] = slbd * slsj + sj.loc[i,"ˮ��������"]
    sj.loc[i,"ˮ��������"] = sj.loc[i,"ˮ��������"] / sj.loc[i,"��ˮʱ��"]   

# ����������ͣ��ʱ������
# ͣ��ʱ������=��(((����ͣ��ʱ��-ƽ��ͣ��ʱ��)^2)*����ʱ��)/��ͣ��ʱ��
sj["ͣ��ʱ������"] = 0 # ��ͣ��ʱ��������һ����ʼֵ0
for i in range(len(sj)):
    if sj.loc[i,"ͣ�ٴ���"] > 1: # ��ͣ�ٴ���Ϊ0��1ʱ��ͣ��ʱ������ֵΪ0�����ų�
        for j in Stop.loc[Stop["ͣ�ٹ����¼�"] == (i+1),"ͣ��ʱ��"].values:
            sj.loc[i,"ͣ��ʱ������"] = ((j - sj.loc[i,"ƽ��ͣ��ʱ��"])**2) * j + \
                                     sj.loc[i,"ͣ��ʱ������"]
        sj.loc[i,"ͣ��ʱ������"] = sj.loc[i,"ͣ��ʱ������"] / sj.loc[i,"��ͣ��ʱ��"]

print('��ˮ���Ͳ�������������ɺ����ݵ�����Ϊ��\n',sj.columns)
print('��ˮ���Ͳ�������������ɺ����ݵ�ǰ5��5������Ϊ��\n',sj.iloc[:5,:5])



sj_bool = (sj['��ˮʱ��'] >100) & (sj['����ˮʱ��'] > 120) & (sj['����ˮ��'] > 5)
sj_final = sj.loc[sj_bool,:]
sj_final.to_excel('../tmp/sj_final.xlsx',index = False)
print('ɸѡ����ѡϴԡ�¼�ǰ��������״Ϊ��',sj.shape)
print('ɸѡ����ѡϴԡ�¼����������״Ϊ��',sj_final.shape)
