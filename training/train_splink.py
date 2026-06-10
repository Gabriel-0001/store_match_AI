import pandas as pd

from splink import (
    Linker,
    DuckDBAPI,
    SettingsCreator,
    block_on
)

import splink.comparison_library as cl

# --------------------------------------------------
# Load data
# --------------------------------------------------

df_a = pd.read_csv(
    "data/raw/osm_mcdonalds.csv"
)

df_b = pd.read_csv(
    "data/raw/osm_mcdonalds_dirty.csv"
)

df_a["source"] = "osm"
df_b["source"] = "dirty"

# Linkage between two datasets
datasets = [df_a, df_b]

# --------------------------------------------------
# Settings
# --------------------------------------------------

settings = SettingsCreator(
    link_type="link_only",
     unique_id_column_name="id",
    blocking_rules_to_generate_predictions=[
        block_on("brand")
    ],
    comparisons=[
        cl.ExactMatch("brand"),

        cl.JaroWinklerAtThresholds(
            "name",
            [0.95, 0.90, 0.85]
        )
    ],
    retain_matching_columns=True
)

# --------------------------------------------------
# Create linker
# --------------------------------------------------

linker = Linker(
    datasets,
    settings,
    DuckDBAPI()
)

# --------------------------------------------------
# Estimate parameters
# --------------------------------------------------

linker.training.estimate_u_using_random_sampling(
    max_pairs=1_000_000
)

# --------------------------------------------------
# Predict matches
# --------------------------------------------------

predictions = linker.inference.predict()

# --------------------------------------------------
# Export results
# --------------------------------------------------

predictions_df = predictions.as_pandas_dataframe()

predictions_df.to_csv(
    "data/predictions.csv",
    index=False
)

print(predictions_df.head())

print(
    f"Generated {len(predictions_df):,} candidate matches."
)