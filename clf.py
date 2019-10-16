from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def get_clf(X_tr,X_ts,y_tr,y_ts):
    clf = DecisionTreeClassifier()
    clf.fit(X_tr.flatten().reshape(len(X_tr), -1), y_tr)
    yhat = clf.predict(X_ts.flatten().reshape(len(X_ts), -1))
    return yhat, accuracy_score(y_ts,yhat)