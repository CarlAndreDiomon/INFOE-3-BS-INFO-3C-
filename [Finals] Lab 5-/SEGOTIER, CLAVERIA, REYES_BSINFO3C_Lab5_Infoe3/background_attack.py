import pandas as pd


def check_k_anonymity(df, qi_cols, k):
    groups = df.groupby(qi_cols, dropna=False).size().reset_index(name="count")
    groups[f"k={k}_satisfied"] = groups["count"] >= k
    print(groups.to_string(index=False))
    return bool(groups["count"].min() >= k)


def build_datasets():
    herorank = pd.DataFrame(
        {
            "record": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"],
            "power_low": [8000, 8000, 5000, 5000, 9500, 9500, 3000, 3000],
            "power_high": [9000, 9000, 6000, 6000, 10500, 10500, 4000, 4000],
            "region": [
                "Eastern Kingdom",
                "Eastern Kingdom",
                "Northern Wastes",
                "Northern Wastes",
                "Capital City",
                "Capital City",
                "Southern Isles",
                "Southern Isles",
            ],
            "weapon": [
                "Sword",
                "Sword",
                "Magic Staff",
                "Magic Staff",
                "Bare Hands",
                "Spear",
                "Bow",
                "Bow",
            ],
            "weakness": [
                "Fire",
                "Ice",
                "Dark Magic",
                "Holy Light",
                "None",
                "Poison",
                "Close Combat",
                "Thunder",
            ],
        }
    )
    wiki = pd.DataFrame(
        {
            "name": [
                "Kyo Ashura",
                "Nami Frost",
                "Zephyr Moon",
                "Seraphiel",
                "Riku Darkwind",
            ],
            "power": [8450, 8720, 5300, 9800, 3200],
            "hometown": [
                "Ryugawa City (East)",
                "Ryugawa City (East)",
                "Frostholm (North)",
                "Solaris (Capital)",
                "Shimaoka (South)",
            ],
            "weapon_raw": [
                "Katana (Sword)",
                "Ice Blade (Sword)",
                "Rune Staff (Magic)",
                "None (Bare Hands)",
                "Longbow (Bow)",
            ],
        }
    )
    return herorank, wiki


def normalize_weapon(raw_weapon):
    weapon = raw_weapon.split("(")[-1].rstrip(")")
    if weapon == "Magic":
        return "Magic Staff"
    return weapon


def normalize_region(hometown):
    return {
        "Ryugawa City (East)": "Eastern Kingdom",
        "Frostholm (North)": "Northern Wastes",
        "Solaris (Capital)": "Capital City",
        "Shimaoka (South)": "Southern Isles",
    }[hometown]


def linkage_attack(herorank_df, wiki_df):
    results = []
    for _, char in wiki_df.iterrows():
        norm_weapon = normalize_weapon(char["weapon_raw"])
        norm_region = normalize_region(char["hometown"])
        matches = herorank_df[
            (herorank_df["power_low"] <= char["power"])
            & (char["power"] <= herorank_df["power_high"])
            & (herorank_df["region"] == norm_region)
            & (herorank_df["weapon"] == norm_weapon)
        ]

        for _, row in matches.iterrows():
            results.append(
                {
                    "character": char["name"],
                    "matched_record": row["record"],
                    "weakness": row["weakness"],
                }
            )
    return results


def re_anonymize_k4(herorank_df):
    df = herorank_df.copy()
    df["power_range"] = df["record"].map(
        {
            "R1": "High Power",
            "R2": "High Power",
            "R5": "High Power",
            "R6": "High Power",
            "R3": "Low/Mid Power",
            "R4": "Low/Mid Power",
            "R7": "Low/Mid Power",
            "R8": "Low/Mid Power",
        }
    )
    df["region"] = df["record"].map(
        {
            "R1": "Core Realms",
            "R2": "Core Realms",
            "R5": "Core Realms",
            "R6": "Core Realms",
            "R3": "Outer Realms",
            "R4": "Outer Realms",
            "R7": "Outer Realms",
            "R8": "Outer Realms",
        }
    )
    df["weapon"] = "*"
    df["power_low"] = df["power_range"].map({"High Power": 8000, "Low/Mid Power": 3000})
    df["power_high"] = df["power_range"].map(
        {"High Power": 10500, "Low/Mid Power": 6000}
    )
    return df


def main():
    herorank, wiki = build_datasets()
    print("HeroRank:")
    print(herorank.to_string(index=False))
    print("\nAnime Wiki:")
    print(wiki.to_string(index=False))

    attack_results = pd.DataFrame(linkage_attack(herorank, wiki))
    print("\nLinkage attack results on released k=2 data:")
    print(attack_results.to_string(index=False))
    exact = attack_results.groupby("character").size().eq(1).sum()
    print(f"Characters fully re-identified: {exact} out of {len(wiki)}")

    herorank_k4 = re_anonymize_k4(herorank)
    print("\nRe-anonymized HeroRank dataset:")
    print(herorank_k4.to_string(index=False))
    print("\nk=4 verification:")
    check_k_anonymity(herorank_k4, ["power_range", "region", "weapon"], k=4)

    after_results = pd.DataFrame(linkage_attack(herorank_k4, wiki))
    print("\nLinkage attack results after k=4 re-anonymization:")
    if after_results.empty:
        print("No character matched the generalized k=4 QI values exactly.")
    else:
        print(after_results.to_string(index=False))



if __name__ == "__main__":
    main()
