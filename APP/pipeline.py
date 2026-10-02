'''End-to-end orchestration for the Badminton AI Coach.'''
from .classifier import train_classifier, predict_with_confidence
from .retrieval import Retriever
from .advisor import advise

class BadmintonCoach:
    def __init__(self, top_k=3, api_key=None):
        self.classifier,_=train_classifier()
        self.retriever=Retriever()
        self.top_k=top_k
        self.api_key=api_key

    def run(self, question):
        category,confidence,probabilities=predict_with_confidence(self.classifier,question)
        hits=self.retriever.retrieve(question,category=category,top_k=self.top_k)
        answer,usage=advise(question,category,hits,api_key=self.api_key)
        return {
            'question':question,
            'category':category,
            'classifier_confidence':confidence,
            'class_probabilities':probabilities,
            'retrieval_backend':self.retriever.using,
            'retrieved':hits,
            'advice':answer,
            'usage':usage,
        }
