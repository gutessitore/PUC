from utils.objects.abstract_classifier import AbstractClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier


class DecisionTree(AbstractClassifier):

    def __init__(self, features, target, pos_label=1, *args, **kwargs):
        model = DecisionTreeClassifier(*args, **kwargs)
        super().__init__(model, features, target, pos_label)

    def run_pipeline(self):
        self.split_data()
        self.fit()
        self.predicted_target = self.predict_test

    def encode_features(self, encoder: str, *args, **kwargs):
        encoders = {
            'label': LabelEncoder(),
            'one_hot': OneHotEncoder(*args, **kwargs),
            'ordinal': OrdinalEncoder(*args, **kwargs)
        }
        print(f'Encoding features with {encoder} encoder')
        encoder_instace = encoders[encoder]
        for column in self.features.columns:
            self.features[column] = encoder_instace.fit_transform(self.features[column])





