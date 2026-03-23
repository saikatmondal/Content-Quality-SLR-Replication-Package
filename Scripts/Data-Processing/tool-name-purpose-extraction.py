import pandas as pd
import re

IN_CSV  = r"E:/PhD Milestones/Comprehensive/ReplicationPackage/FilesForWritingHelp/RQ6/RQ6-V2-Tools-Techniques.csv"
OUT_CSV = r"E:/PhD Milestones/Comprehensive/ReplicationPackage/FilesForWritingHelp/RQ6/RQ6-V2-Tools-Techniques-with-tool-purpose-v1___.csv"

df = pd.read_csv(IN_CSV, encoding="ISO-8859-1")

# More tolerant patterns (handles spaces around '/' and minor variations)
tool_pat = re.compile(r"Tool\s*/\s*Technique\s*\[(.*?)\]", re.IGNORECASE)
purpose_pat = re.compile(r"Purpose\s*\[(.*?)\]", re.IGNORECASE)

def extract_tool_purpose(text):
    if not isinstance(text, str) or not text.strip():
        return "", ""
    m_tool = tool_pat.search(text)
    m_purpose = purpose_pat.search(text)
    tool = m_tool.group(1).strip() if m_tool else ""
    purpose = m_purpose.group(1).strip() if m_purpose else ""
    return tool, purpose

# --- Find the correct source column automatically ---
text_cols = [c for c in df.columns if df[c].dtype == "object"]

def score_col(col):
    s = df[col].dropna().astype(str)
    # count how many cells match either label
    return s.str.contains(r"Tool\s*/\s*Technique\s*\[|Purpose\s*\[", case=False, regex=True).sum()

if not text_cols:
    raise ValueError("No text columns found.")

src_col = max(text_cols, key=score_col)
best_score = score_col(src_col)

if best_score == 0:
    raise ValueError(
        "Couldn't find 'Tool/Technique [' or 'Purpose [' in any text column. "
        "Check the column text or label spelling in the CSV."
    )

# --- Extract ---
tools, purposes = zip(*(extract_tool_purpose(v) for v in df[src_col].astype(str)))

df["Tool"] = list(tools)
df["Purpose"] = list(purposes)

df.to_csv(OUT_CSV, index=False, encoding="ISO-8859-1")
print(f"Saved: {OUT_CSV}")
print(f"Extraction source column: {src_col} (matched rows: {best_score})")
