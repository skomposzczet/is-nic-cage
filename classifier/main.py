from src.classifier import Classifier

if __name__ == '__main__':
    classifier = Classifier()
    classifier.train()
    classifier.save()
