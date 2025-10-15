import argparse
import ast
import mlflow
import mlflow.sklearn
import mlflow.xgboost
import joblib, re, string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd

# ---- preprocessing functions ----
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_moderate(text):
    text = text.lower().strip()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def preprocess_aggressive(text):
    text = text.lower().strip()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[0-9]+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text)
    return text

def preprocess_with_stopwords(text):
    text = preprocess_moderate(text)
    words = text.split()
    return ' '.join([w for w in words if w not in stop_words])

def preprocess_with_stemming(text):
    text = preprocess_moderate(text)
    words = text.split()
    return ' '.join([stemmer.stem(w) for w in words])

def preprocess_with_lemmatization(text):
    text = preprocess_moderate(text)
    words = text.split()
    return ' '.join([lemmatizer.lemmatize(w) for w in words])

preprocess_map = {
    "aggressive": preprocess_aggressive,
    "stopwords": preprocess_with_stopwords,
    "stemming": preprocess_with_stemming,
    "lemmatization": preprocess_with_lemmatization
}

#########################################################################
# ---- main script ----
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preprocessor")
    parser.add_argument("--model_type")
    parser.add_argument("--ngram")
    parser.add_argument("--max_features", type=int)
    parser.add_argument("--logreg_C", type=float)
    parser.add_argument("--xgb_eta", type=float)
    parser.add_argument("--xgb_n_estimators", type=int)
    parser.add_argument("--xgb_max_depth", type=int)
    parser.add_argument("--xgb_colsample_bytree", type=float)
    args = parser.parse_args()

    # dummy dataset placeholder (replace with your dataset)
    df = pd.read_csv("combined_dataset.csv")  # assume 'text' and 'label' columns
    preprocess_fn = preprocess_map[args.preprocessor]
    df["text"] = df["text"].apply(preprocess_fn)

    # ngram_range = ast.literal_eval(args.ngram)
    # ngram_range = tuple(map(float, args.ngram.split(',')))
    # print("Using ngram range:", ngram_range)
    # print("ngram type:", type(ngram_range))
    # NOT WORKING MAN, JUST USING DEFAULTS FOR NOW
    vect = TfidfVectorizer(ngram_range=(1, 2), max_features=args.max_features) # type: ignore
    X = vect.fit_transform(df["text"])
    y = df["label"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        mlflow.log_params(vars(args))

        if args.model_type == "logreg":
            model = LogisticRegression(C=args.logreg_C, max_iter=1000)
            model.fit(X_train, y_train)
            preds = model.predict_proba(X_val)[:, 1]
            auc = roc_auc_score(y_val, preds)
            mlflow.log_metric("roc_auc", float(auc))
            mlflow.pyfunc.log_model("model", python_model=model)

        elif args.model_type == "xgboost":
            model = XGBClassifier(eta=args.xgb_eta, n_estimators=args.xgb_n_estimators, eval_metric="auc")
            model.fit(X_train, y_train)
            preds = model.predict_proba(X_val)[:, 1]
            auc = roc_auc_score(y_val, preds)
            mlflow.log_metric("roc_auc", float(auc))
            mlflow.pyfunc.log_model("model", python_model=model)

        # save tfidf vectorizer
        joblib.dump(vect, "tfidf.pkl")
        mlflow.log_artifact("tfidf.pkl", artifact_path="vectorizer")
