import pandas as pd


def check_k_anonymity(df, qi_cols, k):
    groups = df.groupby(qi_cols, dropna=False).size().reset_index(name="count")
    groups[f"k={k}_satisfied"] = groups["count"] >= k
    print(groups.to_string(index=False))
    return bool(groups["count"].min() >= k)


def check_l_diversity(df, qi_cols, sensitive_col, l):
    rows = []
    for qi_values, group in df.groupby(qi_cols, dropna=False):
        if not isinstance(qi_values, tuple):
            qi_values = (qi_values,)
        values = sorted(group[sensitive_col].unique())
        row = dict(zip(qi_cols, qi_values))
        row.update(
            {
                "records": len(group),
                "distinct_count": len(values),
                "distinct_values": values,
                f"l={l}_satisfied": len(values) >= l,
            }
        )
        rows.append(row)
    summary = pd.DataFrame(rows)
    print(summary.to_string(index=False))
    return bool(summary[f"l={l}_satisfied"].all())


def compute_emd_unordered(ec_dist, overall_dist):
    categories = set(ec_dist) | set(overall_dist)
    return 0.5 * sum(abs(ec_dist.get(cat, 0) - overall_dist.get(cat, 0)) for cat in categories)


def check_t_closeness(df, ec_col, sensitive_col, overall_dist, t):
    rows = []
    all_pass = True
    for ec_name, group in df.groupby(ec_col):
        ec_dist = group[sensitive_col].value_counts(normalize=True).to_dict()
        emd = compute_emd_unordered(ec_dist, overall_dist)
        passes = emd <= t
        all_pass = all_pass and passes
        rows.append({"ec": ec_name, "records": len(group), "emd": emd, "t": t, "passes": passes})
    print(pd.DataFrame(rows).to_string(index=False))
    return all_pass


def build_animed_df():
    return pd.DataFrame(
        {
            "patient_id": [f"M{i:02d}" for i in range(1, 17)],
            "age_group": [
                "18-22",
                "18-22",
                "18-22",
                "18-22",
                "23-30",
                "23-30",
                "23-30",
                "23-30",
                "31-40",
                "31-40",
                "31-40",
                "31-40",
                "41+",
                "41+",
                "41+",
                "41+",
            ],
            "cosplay": [
                "Shonen Hero",
                "Shonen Hero",
                "Shonen Hero",
                "Shonen Hero",
                "Magical Girl",
                "Magical Girl",
                "Magical Girl",
                "Magical Girl",
                "Mecha Pilot",
                "Mecha Pilot",
                "Mecha Pilot",
                "Mecha Pilot",
                "Classic Villain",
                "Classic Villain",
                "Classic Villain",
                "Classic Villain",
            ],
            "days": [
                "1 Day",
                "1 Day",
                "1 Day",
                "1 Day",
                "2 Days",
                "2 Days",
                "2 Days",
                "2 Days",
                "3 Days",
                "3 Days",
                "3 Days",
                "3 Days",
                "2 Days",
                "2 Days",
                "2 Days",
                "2 Days",
            ],
            "condition": [
                "Normal",
                "Normal",
                "Anemia",
                "Anemia",
                "Normal",
                "Pre-diabetic",
                "Hypertensive",
                "Normal",
                "Hypertensive",
                "Hypertensive",
                "Hypertensive",
                "Pre-diabetic",
                "Normal",
                "Anemia",
                "Hypertensive",
                "Pre-diabetic",
            ],
        }
    )


def assign_equivalence_classes(df):
    df = df.copy()
    # Iteration 1: four original ECs pass k=4 and l=2, but M09-M12 fails
    # t=0.30 because it is too skewed toward Hypertensive.
    # Iteration 2: pair young/middle groups and old/teen groups. Each final EC
    # has 8 records, at least 3 distinct conditions, and EMD <= 0.30.
    df["age_gen"] = df["age_group"].map(
        {
            "18-22": "Mixed A",
            "23-30": "Mixed B",
            "31-40": "Mixed B",
            "41+": "Mixed A",
        }
    )
    df["cosplay_gen"] = df["cosplay"].map(
        {
            "Shonen Hero": "Hero/Classic",
            "Classic Villain": "Hero/Classic",
            "Magical Girl": "Popular/Mecha",
            "Mecha Pilot": "Popular/Mecha",
        }
    )
    df["days_gen"] = df["days"].map(
        {"1 Day": "Mixed Attendance", "2 Days": "Mixed Attendance", "3 Days": "Mixed Attendance"}
    )
    df["ec"] = df["age_gen"] + " | " + df["cosplay_gen"] + " | " + df["days_gen"]
    return df


def main():
    df = build_animed_df()
    print("AniMed source data:")
    print(df.to_string(index=False))

    overall_dist = df["condition"].value_counts(normalize=True).to_dict()
    print("\nOverall distribution of Blood Condition:")
    for condition, proportion in sorted(overall_dist.items()):
        print(f"  {condition}: {proportion:.4f}")

    df_anon = assign_equivalence_classes(df)
    print("\nAnonymized EC assignments:")
    print(df_anon[["patient_id", "ec", "condition"]].to_string(index=False))

    qi = ["ec"]
    print("\n=== k=4 CHECK ===")
    k_ok = check_k_anonymity(df_anon, qi, k=4)
    print("\n=== l=2 CHECK ===")
    l_ok = check_l_diversity(df_anon, qi, "condition", l=2)
    print("\n=== t=0.30 CHECK ===")
    t_ok = check_t_closeness(df_anon, "ec", "condition", overall_dist, t=0.30)
    print(f"\nAll criteria satisfied: {k_ok and l_ok and t_ok}")


if __name__ == "__main__":
    main()
