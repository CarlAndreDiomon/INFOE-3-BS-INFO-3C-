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
        distinct_values = sorted(group[sensitive_col].unique())
        row = dict(zip(qi_cols, qi_values))
        row.update(
            {
                "records": len(group),
                "distinct_count": len(distinct_values),
                "distinct_values": distinct_values,
                f"l={l}_satisfied": len(distinct_values) >= l,
            }
        )
        rows.append(row)
    summary = pd.DataFrame(rows)
    print(summary.to_string(index=False))
    return bool(summary[f"l={l}_satisfied"].all())


def build_otakuhealth_df():
    return pd.DataFrame(
        {
            "patient_id": [f"P{i:02d}" for i in range(1, 13)],
            "age_group": [
                "Teen (13-19)",
                "Teen (13-19)",
                "Teen (13-19)",
                "Adult (20-35)",
                "Adult (20-35)",
                "Adult (20-35)",
                "Senior (36+)",
                "Senior (36+)",
                "Senior (36+)",
                "Adult (20-35)",
                "Adult (20-35)",
                "Adult (20-35)",
            ],
            "district": [
                "Shibuya",
                "Shibuya",
                "Shibuya",
                "Harajuku",
                "Harajuku",
                "Harajuku",
                "Akihabara",
                "Akihabara",
                "Akihabara",
                "Shibuya",
                "Shibuya",
                "Shibuya",
            ],
            "role": [
                "Attendee",
                "Attendee",
                "Attendee",
                "Cosplayer",
                "Cosplayer",
                "Cosplayer",
                "Vendor",
                "Vendor",
                "Vendor",
                "Volunteer",
                "Volunteer",
                "Volunteer",
            ],
            "diagnosis": [
                "Anxiety",
                "Anxiety",
                "Anxiety",
                "Back Pain",
                "Back Pain",
                "Fatigue",
                "Hypertension",
                "Hypertension",
                "Hypertension",
                "Fatigue",
                "Fatigue",
                "Fatigue",
            ],
        }
    )


def fix_l_diversity(df, qi_cols, sensitive_col, l):
    df_fixed = df.copy()
    # The homogeneous ECs are merged by suppressing all three QIs to broader
    # values. This costs utility, but it preserves every record and gives the
    # formerly vulnerable groups multiple sensitive values.
    df_fixed["age_group"] = "All Ages"
    df_fixed["district"] = "Tokyo Event Area"
    df_fixed["role"] = "Participant"
    return df_fixed


def build_mangaleague_df():
    return pd.DataFrame(
        {
            "fan_id": [f"F{i:02d}" for i in range(1, 16)],
            "age_range": [
                "15-19",
                "15-19",
                "15-19",
                "20-25",
                "20-25",
                "20-25",
                "26-35",
                "26-35",
                "26-35",
                "36+",
                "36+",
                "36+",
                "15-19",
                "15-19",
                "15-19",
            ],
            "region": [
                "Luzon",
                "Luzon",
                "Luzon",
                "Visayas",
                "Visayas",
                "Visayas",
                "Mindanao",
                "Mindanao",
                "Mindanao",
                "Luzon",
                "Luzon",
                "Luzon",
                "Visayas",
                "Visayas",
                "Visayas",
            ],
            "series": [
                "One Piece",
                "One Piece",
                "Naruto",
                "Attack on Titan",
                "Attack on Titan",
                "Attack on Titan",
                "Dragon Ball Z",
                "Dragon Ball Z",
                "Dragon Ball Z",
                "Sailor Moon",
                "Sailor Moon",
                "Sailor Moon",
                "Demon Slayer",
                "Demon Slayer",
                "Demon Slayer",
            ],
            "knowledge": [
                "Novice",
                "Novice",
                "Intermediate",
                "Expert",
                "Expert",
                "Master",
                "Intermediate",
                "Intermediate",
                "Intermediate",
                "Master",
                "Master",
                "Expert",
                "Novice",
                "Novice",
                "Intermediate",
            ],
        }
    )


def generalize_series(series, level=1):
    if level == 1:
        return {
            "One Piece": "Shonen",
            "Naruto": "Shonen",
            "Dragon Ball Z": "Shonen",
            "Attack on Titan": "Modern Anime",
            "Demon Slayer": "Modern Anime",
            "Sailor Moon": "Classic/Magical",
        }[series]
    return "Anime"


def generalize_age_range(age_range, level=1):
    if level == 1:
        return {
            "15-19": "Under 25",
            "20-25": "Under 25",
            "26-35": "26 and above",
            "36+": "26 and above",
        }[age_range]
    return "All Ages"


def generalize_region(region, level=1):
    if level == 1:
        return {"Luzon": "North/Central", "Visayas": "South/Central", "Mindanao": "South/Central"}[
            region
        ]
    return "Philippines"


def mangaleague_summary(df, qi):
    ec_summary = (
        df.groupby(qi)["knowledge"]
        .agg(records="count", distinct=pd.Series.nunique, levels=list)
        .reset_index()
    )
    ec_summary["l3_satisfied"] = ec_summary["distinct"] >= 3
    print(ec_summary.to_string(index=False))
    return ec_summary


def main():
    print("=== Lab 2.1: OtakuHealth ===")
    df = build_otakuhealth_df()
    qi = ["age_group", "district", "role"]
    print(df.to_string(index=False))
    print("\nOriginal l=2 check:")
    check_l_diversity(df, qi, "diagnosis", l=2)

    ec_p07 = df[
        (df["age_group"] == "Senior (36+)")
        & (df["district"] == "Akihabara")
        & (df["role"] == "Vendor")
    ]
    print("\nEC for P07 before fix:")
    print(ec_p07.to_string(index=False))
    print("Distinct diagnoses:", ec_p07["diagnosis"].unique())
    # This is a homogeneity attack: every record in P07's EC has Hypertension.

    df_fixed = fix_l_diversity(df, qi, "diagnosis", l=2)
    print("\nVerification after l-diversity fix:")
    check_l_diversity(df_fixed, qi, "diagnosis", l=2)
    print("\nk=3 still satisfied after fix:")
    check_k_anonymity(df_fixed, qi, k=3)
    print("\nP07's EC after fix:")
    p07_fixed = df_fixed[df_fixed["patient_id"] == "P07"].iloc[0]
    ec_p07_after = df_fixed[
        (df_fixed["age_group"] == p07_fixed["age_group"])
        & (df_fixed["district"] == p07_fixed["district"])
        & (df_fixed["role"] == p07_fixed["role"])
    ]
    print(ec_p07_after.to_string(index=False))
    print("Distinct diagnoses:", ec_p07_after["diagnosis"].unique())

    print("\n=== Lab 2.2: MangaLeague ===")
    fans = build_mangaleague_df()
    fan_qi = ["age_range", "region", "series"]
    print("\nOriginal EC summary:")
    mangaleague_summary(fans, fan_qi)

    df_anon = fans.copy()
    df_anon["series"] = df_anon["series"].apply(lambda x: generalize_series(x, level=2))
    df_anon["age_range"] = df_anon["age_range"].apply(
        lambda x: generalize_age_range(x, level=2)
    )
    df_anon["region"] = df_anon["region"].apply(lambda x: generalize_region(x, level=2))
    print("\nAfter generalization to l=3:")
    check_l_diversity(df_anon, fan_qi, "knowledge", l=3)
    print("\nk=3 check after generalization:")
    check_k_anonymity(df_anon, fan_qi, k=3)

    ec_f08_before = fans[
        (fans["age_range"] == "26-35")
        & (fans["region"] == "Mindanao")
        & (fans["series"] == "Dragon Ball Z")
    ]
    print("\nBefore generalization, EC of F08:")
    print(ec_f08_before["knowledge"].value_counts())

    f08_after = df_anon[df_anon["fan_id"] == "F08"].iloc[0]
    ec_f08_after = df_anon[
        (df_anon["age_range"] == f08_after["age_range"])
        & (df_anon["region"] == f08_after["region"])
        & (df_anon["series"] == f08_after["series"])
    ]
    print("\nAfter generalization, EC of F08:")
    print(ec_f08_after["knowledge"].value_counts())
    print("Distinct levels:", sorted(ec_f08_after["knowledge"].unique()))


if __name__ == "__main__":
    main()
