import pandas as pd


def compute_emd_unordered(ec_dist, overall_dist):
    categories = set(ec_dist) | set(overall_dist)
    return 0.5 * sum(abs(ec_dist.get(cat, 0) - overall_dist.get(cat, 0)) for cat in categories)


def check_t_closeness(df, ec_col, sensitive_col, overall_dist, t):
    all_pass = True
    rows = []
    for ec_name, group in df.groupby(ec_col):
        ec_dist = group[sensitive_col].value_counts(normalize=True).to_dict()
        emd = compute_emd_unordered(ec_dist, overall_dist)
        passes = emd <= t
        all_pass = all_pass and passes
        rows.append({"ec": ec_name, "records": len(group), "emd": emd, "t": t, "passes": passes})
    print(pd.DataFrame(rows).to_string(index=False))
    return all_pass


def build_nihonstream_df():
    records = []
    ec1_tiers = ["Free", "Free", "Silver", "Free", "Silver"]
    ec2_tiers = ["Platinum", "Platinum", "Platinum", "Gold", "Gold", "Gold", "Silver"]
    ec3_tiers = ["Free", "Free", "Free", "Free", "Silver", "Silver", "Gold", "Platinum"]
    for tier in ec1_tiers:
        records.append({"ec": "EC1", "viewer_tier": tier})
    for tier in ec2_tiers:
        records.append({"ec": "EC2", "viewer_tier": tier})
    for tier in ec3_tiers:
        records.append({"ec": "EC3", "viewer_tier": tier})
    return pd.DataFrame(records)


def fix_t_closeness(df):
    df_fixed = df.copy()
    # EC2 is skewed toward Gold/Platinum. Merging all records into a broader
    # released EC makes the EC distribution equal to the overall distribution,
    # passing t-closeness while reducing utility.
    df_fixed["ec"] = "EC_ALL"
    return df_fixed


def main():
    df = build_nihonstream_df()
    overall_dist = df["viewer_tier"].value_counts(normalize=True).sort_index()
    overall_dict = overall_dist.to_dict()
    print("NihonStream data:")
    print(df.to_string(index=False))
    print("\nOverall distribution:")
    print(overall_dist)

    test_ec = {"Free": 0.6, "Silver": 0.4, "Gold": 0.0, "Platinum": 0.0}
    test_overall = {"Free": 0.40, "Silver": 0.25, "Gold": 0.20, "Platinum": 0.15}
    print("\nEMD test result:")
    print(compute_emd_unordered(test_ec, test_overall))
    # Note: using the stated formula, the workbook's sample distributions give
    # 0.35, not 0.175.

    print("\nt=0.25 check before fix:")
    check_t_closeness(df, "ec", "viewer_tier", overall_dict, t=0.25)

    df_fixed = fix_t_closeness(df)
    print("\nt=0.25 check after fix:")
    check_t_closeness(df_fixed, "ec", "viewer_tier", overall_dict, t=0.25)

    # Q1: If t is very small, such as 0.01, EC distributions must almost exactly
    # match the overall distribution. Privacy is strong, but useful subgroup
    # patterns may disappear because heavy merging or suppression is required.
    # Q2: If t is very large, such as 0.90, highly skewed ECs can pass. That
    # creates privacy risk because a sensitive tier may still be inferred from
    # the EC distribution.


if __name__ == "__main__":
    main()
