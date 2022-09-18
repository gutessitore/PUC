from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from abc import ABC, abstractmethod


class AbstractClassifier(ABC):

    @abstractmethod
    def __init__(self, model, features, target, pos_label=1):
        self.model = model
        self.features = features
        self.target = target
        self.pos_label = pos_label

        self.features_train = None
        self.features_test = None
        self.target_train = None
        self.target_test = None

        self.predicted_target = None

    @abstractmethod
    def run_pipeline(self):
        pass

    @abstractmethod
    def encode_features(self, encoder: str):
        pass

    def evaluate_classifier(self) -> None:
        accuracy = self.score
        precision = self.precision
        recall = self.recall
        f1 = self.f1

        conf_matrix = self.confusion_matrix
        ConfusionMatrixDisplay(conf_matrix, display_labels=self.classes).plot(cmap='Blues')
        print(f'Accuracy: {accuracy:.4}\nPrecision: {precision:.4}\nRecall: {recall:.4}\nF1: {f1:.4}')

    def split_data(self, test_size: float = 0.2, random_state: int = 0) -> None:
        self.features_train, self.features_test, self.target_train, self.target_test = train_test_split(
            self.features, self.target, test_size=test_size, random_state=random_state)

    def fit(self):
        self.model.fit(self.features_train, self.target_train)

    @property
    def predict_test(self):
        return self.model.predict(self.features_test)

    def predict_proba(self, features):
        return self.model.predict_proba(features)

    @property
    def score(self):
        return accuracy_score(self.target_test, self.predicted_target)

    @property
    def precision(self):
        return precision_score(self.target_test, self.predicted_target, pos_label=self.pos_label)

    @property
    def recall(self):
        return recall_score(self.target_test, self.predicted_target, pos_label=self.pos_label)

    @property
    def f1(self):
        return f1_score(self.target_test, self.predicted_target, pos_label=self.pos_label)

    @property
    def confusion_matrix(self):
        return confusion_matrix(self.target_test, self.predicted_target)

    @property
    def classes(self):
        return self.model.classes_
