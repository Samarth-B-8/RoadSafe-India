import json
from pathlib import Path

import geopandas as gpd


# =======================================================
# PATHS
# =======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_path = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "india_states_combined.geojson"
)

output_path = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "india_states_dissolved.geojson"
)


# =======================================================
# CHECK INPUT
# =======================================================

if not input_path.exists():
    raise FileNotFoundError(
        f"Input GeoJSON not found:\n{input_path}"
    )


# =======================================================
# LOAD GEOJSON
# =======================================================

print("Loading GeoJSON...")

gdf = gpd.read_file(input_path)

print(f"Original feature count: {len(gdf)}")
print(f"Original columns: {list(gdf.columns)}")


# =======================================================
# FIND STATE NAME COLUMN
# =======================================================

possible_name_columns = [
    "st_nm",
    "ST_NM",
    "STNAME",
    "state",
    "STATE",
    "name",
    "NAME",
    "NAME_1"
]

state_column = None

for column in possible_name_columns:

    if column in gdf.columns:

        state_column = column
        break


if state_column is None:

    raise ValueError(
        "Could not find a State/UT name column in the GeoJSON."
    )


print(f"State/UT column found: {state_column}")


# =======================================================
# KEEP ONLY WHAT WE NEED
# =======================================================

gdf = gdf[
    [state_column, "geometry"]
].copy()


gdf = gdf.rename(
    columns={
        state_column: "state"
    }
)


# =======================================================
# CLEAN STATE NAMES
# =======================================================

gdf["state"] = (
    gdf["state"]
    .astype(str)
    .str.strip()
)


gdf = gdf[
    gdf["state"].notna() &
    (gdf["state"] != "") &
    (gdf["state"] != "None")
].copy()


# =======================================================
# FIX GEOMETRIES
# =======================================================

print("Fixing geometries...")

gdf["geometry"] = (
    gdf["geometry"]
    .make_valid()
)


# =======================================================
# DISSOLVE MULTIPLE FEATURES INTO ONE STATE GEOMETRY
# =======================================================

print("Dissolving geometries by State/UT...")

dissolved = (
    gdf
    .dissolve(
        by="state",
        as_index=False
    )
)


# =======================================================
# REMOVE EMPTY GEOMETRIES
# =======================================================

dissolved = dissolved[
    dissolved.geometry.notna() &
    ~dissolved.geometry.is_empty
].copy()


# =======================================================
# SAVE
# =======================================================

print(
    f"Final State/UT feature count: {len(dissolved)}"
)

dissolved.to_file(
    output_path,
    driver="GeoJSON"
)


print()
print("State-level GeoJSON created successfully.")
print(f"Saved to: {output_path}")