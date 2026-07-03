from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from src.entity.artifact_entity import ClassificationMetricArtifact

def calculate_metric(model, x, y) -> ClassificationMetricArtifact:
    yhat = model.predict(x)
    return ClassificationMetricArtifact(
        f1_score=f1_score(y, yhat, average='weighted'),
        recall_score=recall_score(y, yhat, average='weighted'),
        precision_score=precision_score(y, yhat, average='weighted'),
    )

def total_cost(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return 10 * fp + 500 * fn