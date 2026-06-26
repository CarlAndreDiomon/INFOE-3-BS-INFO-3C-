import pandas as pd


def build_animevault_df():
    data = {
        "user_id": [f"U{i:03d}" for i in range(1, 13)],
        "age": [17, 18, 17, 19, 22, 22, 25, 24, 23, 19, 18, 25],
        "region": [
            "NCR",
            "NCR",
            "Cebu",
            "NCR",
            "Davao",
            "Davao",
            "NCR",
            "Cebu",
            "Cebu",
            "NCR",
            "Davao",
            "Davao",
        ],
        "genre": [
            "Shonen",
            "Shonen",
            "Isekai",
            "Romance",
            "Shonen",
            "Isekai",
            "Horror",
            "Romance",
            "Horror",
            "Isekai",
            "Shonen",
            "Romance",
        ],
        "sub_plan": [
            "Basic",
            "Premium",
            "Basic",
            "Premium",
            "Standard",
            "Basic",
            "Premium",
            "Standard",
            "Basic",
            "Standard",
            "Basic",
            "Premium",
        ],
    }
    return pd.DataFrame(data)


def generalize_age(age, level=1):
    if level == 1:
        low = (int(age) // 5) * 5
        return f"[{low}-{low + 4}]"
    if level == 2:
        low = (int(age) // 10) * 10
        return f"[{low}-{low + 9}]"
    return "Any"


def generalize_region(region, level=1):
    if level == 1:
        return {"NCR": "Luzon", "Cebu": "Visayas", "Davao": "Mindanao"}[region]
    return "Philippines"


def generalize_genre(genre, level=1):
    if level == 1:
        return {
            "Shonen": "Action/Adventure",
            "Isekai": "Action/Adventure",
            "Romance": "Drama/Thriller",
            "Horror": "Drama/Thriller",
        }[genre]
    return "Anime"


def check_k_anonymity(df, qi_cols, k):
    groups = df.groupby(qi_cols, dropna=False).size().reset_index(name="count")
    groups[f"k={k}_satisfied"] = groups["count"] >= k
    print(groups.to_string(index=False))
    return bool(groups["count"].min() >= k)


def anonymize_until_k(df, k=3):
    attempts = [
        (1, 1, 1),
        (2, 1, 1),
        (2, 2, 1),
        (2, 2, 2),
        (3, 2, 2),
    ]
    qi = ["age", "region", "genre"]

    for age_level, region_level, genre_level in attempts:
        candidate = df.copy()
        candidate["age"] = candidate["age"].apply(lambda x: generalize_age(x, age_level))
        candidate["region"] = candidate["region"].apply(
            lambda x: generalize_region(x, region_level)
        )
        candidate["genre"] = candidate["genre"].apply(
            lambda x: generalize_genre(x, genre_level)
        )

        print(
            f"\nTrying levels: age={age_level}, region={region_level}, genre={genre_level}"
        )
        if check_k_anonymity(candidate, qi, k):
            return candidate, (age_level, region_level, genre_level)

    raise ValueError("No tested generalization satisfied k-anonymity.")


def main():
    df = build_animevault_df()
    print("Original AnimeVault data:")
    print(df.to_string(index=False))
    print("\nData types:")
    print(df.dtypes)

    df_anon, levels = anonymize_until_k(df, k=3)
    qi = ["age", "region", "genre"]
    age_level, region_level, genre_level = levels

    print("\nFinal anonymized dataset:")
    print(df_anon.to_string(index=False))
    print("\nFinal equivalence classes:")
    check_k_anonymity(df_anon, qi, k=3)
    print(f"\nk=3 satisfied: {check_k_anonymity(df_anon, qi, k=3)}")

    u007_age = generalize_age(25, level=age_level)
    u007_region = generalize_region("NCR", level=region_level)
    u007_genre = generalize_genre("Horror", level=genre_level)
    ec_u007 = df_anon[
        (df_anon["age"] == u007_age)
        & (df_anon["region"] == u007_region)
        & (df_anon["genre"] == u007_genre)
    ]
    print("\nEquivalence class containing U007:")
    print(ec_u007.to_string(index=False))


if __name__ == "__main__":
    main()
