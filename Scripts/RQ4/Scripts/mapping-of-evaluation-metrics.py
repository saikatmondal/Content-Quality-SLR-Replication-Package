import pandas as pd
import re
import unicodedata

IN_CSV  = r".../RQ4/Outputs/study-wise-evaluation-metrics.csv"
OUT_CSV = r".../RQ4/Outputs/study-vs-metrics-binary-mapping.csv"

# -----------------------------
# 1) Metric list (column headers)
# -----------------------------
METRICS = [
    "recall",
    "precision",
    "f1 score",
    "accuracy",
    "auc/roc/auc-roc",
    "rouge",
    "bleu",
    "cohen's kappa",
    "odds ratio",
    "mean reciprocal rank",
    "standard deviation",
    "chi-squared test",
    "r-square",
    "mean",
    "likert scale",
    "pearson correlation",
    "ndcg",
    "cliff's delta",
    "mann-whitney-wilcoxon test",
    "infogain",
    "t-test",
    "krippendorff's alpha",
    "human evaluation",
    "hosmer-lemeshow test",
    "log likelihood",
    "qualitative analysis",
    "manual validation",
    "meteor",
    "p-value",
    "relevance score",
    "rmse",
    "usefulness score",
    "gleu",
    "mann-whitney u-test results",
    "correctness",
    "conciseness",
    "coefficient estimate",
    "exact match (em)",
    "diversity score",
    "completeness",
    "answer score",
    "cosine similarity",
    "fisher's z-transformation",
    "relative differences (rd)",
    "rank feature (z-score)",
    "random forest coefficient",
    "psp (propensity scored precision)",
    "cohen's classification (rho)",
    "compilability",
    "binning (time categorization)",
    "pseudo-r-squared",
    "comprehensibility",
    "omnibus tests of model coefficients",
    "chi-squared statistic",
    "beta coefficients",
    "beta value Â– b",
    "standard error mean",
    "user study",
    "anova",
    "understandability",
    "top@k (k=1,3,5,10,15)",
    "statistical analysis (mean, standard deviation)",
    "statistical analysis",
    "standard error - s.e",
    "consensus-based image description evaluation (cider)",
    "bertscore",
    "spearman's rank correlation",
    "skewness",
    "significance Â– p",
    "significance - ?",
    "scott-knott (feature ranking)",
    "omnibus test ?2",
    "constant",
    "normalized cumulative gain discount (ndcc@k, k=1-10)",
    "cramer's v",
    "mae",
    "macro-recall",
    "macro-precision",
    "macro-f1",
    "logistic regression(beta value - ?",
    "cox and snell r^2",
    "kurtosis",
    "neural network coefficient",
    "cross-entropy loss",
    "kaplan-meier estimator",
    "discounted cumulative gain -dcg@k (k=2-5)",
    "f-statistic",
    "gelkerke r^2",
    "fleiss's kappa (agreement)",
    "agreement level",
    "cox and snell r square",
    "manual evaluation",
    "cox and snell incremental r^2",
    "matching score",
    "matching_top10",
    "matthews correlation coefficient",
    "mean average precision (map)",
    "correlation",
    "micro-receiver operating characteristic (roc) curve",
    "mse",
    "multi-class log loss (mll)",
    "na",
    "nagelkerke incremental r^2",
    "nagelkerke r square",
    "nasa tlx for workload",
    "fitness function",
    "wald statistics - wald",
]

# -----------------------------
# 2) Normalization helper
#    (case-insensitive + fixes weird encodings like Â–)
# -----------------------------
def norm_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFKC", s)
    # common mojibake cleanups
    s = s.replace("Â–", "-").replace("–", "-").replace("—", "-")
    s = s.replace("Â", "")
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)  # collapse whitespace
    return s

# Pre-normalize the canonical metric list
metric_norm_map = {m: norm_text(m) for m in METRICS}
metric_norm_set = set(metric_norm_map.values())

# -----------------------------
# 3) Load input
# -----------------------------
df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

# Ensure required columns exist
if "Study#" not in df.columns or "EvaluationMetrics" not in df.columns:
    raise ValueError("Input CSV must contain columns: 'Study#' and 'EvaluationMetrics'")

# -----------------------------
# 4) Build binary mapping
# -----------------------------
out_rows = []

for _, row in df.iterrows():
    study = row.get("Study#", "")
    em = row.get("EvaluationMetrics", "")

    if not isinstance(study, str) or not study.strip():
        continue

    # Split the EvaluationMetrics cell by ';'
    found_metrics = set()
    if isinstance(em, str) and em.strip():
        tokens = [t.strip() for t in em.split(";") if t.strip()]
        found_metrics = {norm_text(t) for t in tokens if norm_text(t)}

    # Create row with Study# and 0/1 for each metric header
    out_row = {"Study#": study.strip()}
    for metric_header in METRICS:
        key = metric_norm_map[metric_header]
        out_row[metric_header] = 1 if key in found_metrics else 0

    out_rows.append(out_row)

out_df = pd.DataFrame(out_rows, columns=["Study#"] + METRICS)

# Optional: ensure studies S1..S127 exist (add missing as all-0)
# Comment out if you ONLY want studies present in the file.
existing = set(out_df["Study#"].astype(str))
missing_rows = []
for i in range(1, 128):
    s = f"S{i}"
    if s not in existing:
        r = {"Study#": s}
        for metric_header in METRICS:
            r[metric_header] = 0
        missing_rows.append(r)
if missing_rows:
    out_df = pd.concat([out_df, pd.DataFrame(missing_rows)], ignore_index=True)

# Sort by numeric study id (S1, S2, ... S127)
def study_sort_key(s):
    m = re.match(r"(?i)^s(\d+)$", str(s).strip())
    return int(m.group(1)) if m else 10**9

out_df = out_df.sort_values(by="Study#", key=lambda col: col.map(study_sort_key))

# -----------------------------
# 5) Save
# -----------------------------
# out_df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")
out_df.to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"Saved binary study-metric mapping to:\n{OUT_CSV}")
