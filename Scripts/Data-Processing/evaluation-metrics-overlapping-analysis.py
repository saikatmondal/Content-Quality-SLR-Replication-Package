import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Paths
# -----------------------------
IN_CSV  = r".../RQ4/Outputs/study-vs-metrics-binary-mapping.csv"
OUT_CO  = r".../RQ4/Outputs/evaluation-metric-cooccurrence-count.csv"
OUT_JAC = r".../RQ4/Outputs/evaluation-metric-jaccard-similarity.csv"

FIG_CO  = r".../RQ4/Outputs/heatmap-cooccurrence.png"
FIG_JAC = r".../RQ4/Outputs/heatmap-jaccard.png"

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(IN_CSV, encoding="utf-8")

metrics_df = df.drop(columns=["Study#"])
metrics_df = metrics_df.apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)

metric_names = metrics_df.columns.tolist()
M = metrics_df.values  # (studies × metrics)

# -----------------------------
# 1) Co-occurrence matrix
# -----------------------------
cooccurrence = M.T @ M
co_df = pd.DataFrame(cooccurrence, index=metric_names, columns=metric_names)
co_df.to_csv(OUT_CO, encoding="utf-8")

# -----------------------------
# 2) Jaccard matrix
# -----------------------------
n = len(metric_names)
jaccard = np.zeros((n, n), dtype=float)

for i in range(n):
    for j in range(n):
        inter = cooccurrence[i, j]
        union = cooccurrence[i, i] + cooccurrence[j, j] - inter
        jaccard[i, j] = inter / union if union > 0 else 0.0

jac_df = pd.DataFrame(jaccard, index=metric_names, columns=metric_names)
jac_df.to_csv(OUT_JAC, encoding="utf-8")

# -----------------------------
# Heatmap drawing function
# -----------------------------
def draw_heatmap(mat, labels, title, out_png, fmt):
    plt.figure(figsize=(14, 12))

    im = plt.imshow(mat, cmap="YlOrRd", interpolation="nearest", alpha=0.70)
    plt.colorbar(im, fraction=0.046, pad=0.04)

    plt.xticks(range(len(labels)), labels, rotation=90, fontsize=8)
    plt.yticks(range(len(labels)), labels, fontsize=8)

    # Annotate numbers inside cells
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = mat[i, j]
            if fmt == "int":
                text = f"{int(val)}"
            else:
                text = f"{val:.2f}"

            plt.text(
                j, i, text,
                ha="center", va="center",
                fontsize=6,
                color="black"
            )

    plt.title(title, fontsize=14)
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

# -----------------------------
# Draw heatmaps
# -----------------------------
draw_heatmap(
    cooccurrence,
    metric_names,
    "Evaluation Metric Co-occurrence (Count)",
    FIG_CO,
    fmt="int"
)

draw_heatmap(
    jaccard,
    metric_names,
    "Evaluation Metric Co-occurrence (Jaccard Similarity)",
    FIG_JAC,
    fmt="float"
)

print("Saved outputs:")
print(f"- CSV (count):    {OUT_CO}")
print(f"- CSV (jaccard):  {OUT_JAC}")
print(f"- Heatmap count:  {FIG_CO}")
print(f"- Heatmap jacc.:  {FIG_JAC}")