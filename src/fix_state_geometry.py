from pathlib import Path

import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely.ops import unary_union


# =======================================================
# PATHS
# =======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

input_path = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "india_states_dissolved.geojson"
)

output_path = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "india_states_final.geojson"
)


# =======================================================
# LOAD DISSOLVED STATE DATA
# =======================================================

print("Loading dissolved State/UT GeoJSON...")

gdf = gpd.read_file(input_path)

print("Input features:", len(gdf))


# =======================================================
# FUNCTION TO EXTRACT POLYGON GEOMETRY
# =======================================================

def extract_polygon_geometry(geometry):
    """
    Extract only Polygon and MultiPolygon parts from a geometry.

    GeometryCollections can contain polygons together with
    non-area geometries such as lines or points.

    We keep only the polygonal components because the dashboard
    requires State/UT area boundaries.
    """

    if geometry is None or geometry.is_empty:
        return None

    # Already a Polygon
    if isinstance(geometry, Polygon):
        return geometry

    # Already a MultiPolygon
    if isinstance(geometry, MultiPolygon):
        return geometry

    # GeometryCollection
    if isinstance(geometry, GeometryCollection):

        polygon_parts = []

        for part in geometry.geoms:

            extracted = extract_polygon_geometry(part)

            if extracted is not None:
                polygon_parts.append(extracted)

        if not polygon_parts:
            return None

        return unary_union(polygon_parts)

    return None


# =======================================================
# EXTRACT POLYGON PARTS
# =======================================================

print("Converting geometries to polygonal geometry...")

gdf["geometry"] = (
    gdf["geometry"]
    .apply(extract_polygon_geometry)
)


# =======================================================
# REMOVE EMPTY GEOMETRIES
# =======================================================

gdf = gdf[
    gdf["geometry"].notna()
    & ~gdf["geometry"].is_empty
].copy()


# =======================================================
# MAKE SURE GEOMETRIES ARE VALID
# =======================================================

print("Validating geometries...")

gdf["geometry"] = (
    gdf["geometry"]
    .make_valid()
)


# =======================================================
# CONVERT ANY NEW GEOMETRY COLLECTIONS AGAIN
# =======================================================

gdf["geometry"] = (
    gdf["geometry"]
    .apply(extract_polygon_geometry)
)


# =======================================================
# REMOVE EMPTY RESULTS
# =======================================================

gdf = gdf[
    gdf["geometry"].notna()
    & ~gdf["geometry"].is_empty
].copy()


# =======================================================
# DISSOLVE AGAIN BY STATE
# =======================================================

print("Final dissolve by State/UT...")

gdf = (
    gdf
    .dissolve(
        by="state",
        as_index=False
    )
)


# =======================================================
# FINAL GEOMETRY CLEANUP
# =======================================================

gdf["geometry"] = (
    gdf["geometry"]
    .apply(extract_polygon_geometry)
)


gdf = gdf[
    gdf["geometry"].notna()
    & ~gdf["geometry"].is_empty
].copy()


# =======================================================
# CHECK GEOMETRY TYPES
# =======================================================

print("\nFinal feature count:", len(gdf))

print("\nFinal geometry types:")

print(
    gdf.geometry.geom_type.value_counts()
)


# =======================================================
# CHECK HARYANA
# =======================================================

print("\nHaryana geometry:")

haryana = gdf[
    gdf["state"].astype(str).str.lower() == "haryana"
]

if haryana.empty:
    print("Haryana NOT FOUND")
else:
    print(
        haryana[["state", "geometry"]]
    )


# =======================================================
# SAVE
# =======================================================

gdf.to_file(
    output_path,
    driver="GeoJSON"
)

print()
print("Final State/UT GeoJSON created successfully.")
print("Saved to:")
print(output_path)