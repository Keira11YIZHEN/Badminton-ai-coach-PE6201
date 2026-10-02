"""Reproduce the Class 1 baseline and local classifier evaluation."""
from collections import Counter
import json, time
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report
from app.classifier import load_data, train_classifier

ROOT=Path(__file__).resolve().parents[1]
rows=load_data()
model,(X_train,X_test,y_train,y_test)=train_classifier(rows)
majority=Counter(y_test).most_common(1)[0][0]
baseline=[majority]*len(y_test)
t0=time.perf_counter(); pred=model.predict(X_test); elapsed=time.perf_counter()-t0
result={
 'n_total':len(rows),'n_train':len(X_train),'n_test':len(X_test),
 'test_support':dict(Counter(y_test)),
 'majority_label':majority,'majority_accuracy':accuracy_score(y_test,baseline),
 'tfidf_accuracy':accuracy_score(y_test,pred),
 'tfidf_latency_ms_per_item':elapsed/len(X_test)*1000,
 'classification_report':classification_report(y_test,pred,zero_division=0,output_dict=True),
}
print(json.dumps(result,indent=2))
(ROOT/'results'/'classifier_local_reproduction.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
