import pandas as pd

def build_timeline(reports: list) -> pd.DataFrame:
    rows = []
    for r in reports:
        rows.append({
            "path": r.get("path"),
            "created": pd.to_datetime(r.get("created")),
            "modified": pd.to_datetime(r.get("modified")),
            "size_bytes": r.get("size_bytes"),
            "sha256": r.get("sha256")
        })
    df = pd.DataFrame(rows)
    df = df.sort_values(by=["modified", "created"], ascending=True)
    return df
