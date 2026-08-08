#!/usr/bin/env python3
"""Reproduce diagnostic benchmark experiments reported in the IWCS descriptor revision."""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score

CSV='dataset/dataset_omnetpp_cleaned_2.csv'
df=pd.read_csv(CSV)
y=df['Attack_Type']
F8=['Avg_RSSI_dBm','DIO_Count_Window','DIS_Count_Window','Rank_Changes_Window','PDR_percent','Avg_Delay_ms','Throughput_kbps','Energy_Consumed_J']
F6=['Avg_RSSI_dBm','DIO_Count_Window','DIS_Count_Window','Rank_Changes_Window','PDR_percent','Throughput_kbps']
MODELS={
 'Decision Tree':DecisionTreeClassifier(max_depth=5,random_state=42),
 'Random Forest':RandomForestClassifier(n_estimators=200,random_state=42,n_jobs=-1),
 'Logistic Regression':make_pipeline(StandardScaler(),LogisticRegression(max_iter=5000,random_state=42)),
}
rows=[]
for label,features in [('8 features',F8),('6-feature ablation',F6)]:
    Xtr,Xte,ytr,yte=train_test_split(df[features],y,test_size=.2,random_state=42,stratify=y)
    for name,model in MODELS.items():
        model.fit(Xtr,ytr); pred=model.predict(Xte)
        rows.append([label,'80/20',name,'-',accuracy_score(yte,pred),f1_score(yte,pred,average='macro')])
    for name in ['Random Forest','Logistic Regression']:
        for topo in sorted(df.Topology.unique()):
            tr=df.Topology!=topo; te=~tr
            model=MODELS[name]
            model.fit(df.loc[tr,features],y[tr]); pred=model.predict(df.loc[te,features])
            rows.append([label,'LOTO',name,topo,accuracy_score(y[te],pred),f1_score(y[te],pred,average='macro')])
out=pd.DataFrame(rows,columns=['Feature_Set','Protocol','Model','Held_Out','Accuracy','Macro_F1'])
out.to_csv('benchmark_results.csv',index=False)
print(out.to_string(index=False))
