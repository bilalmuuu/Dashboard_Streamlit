import geopandas as gpd

print("Loading geojson...")

gdf = gpd.read_file(
    "data/Kabupaten_Indonesia.json"
)

print("Rows:", len(gdf))

print("Creating kabupaten boundary...")

kab_gdf = (
    gdf
    .dissolve(
        by="WADMKK",
        as_index=False
    )
)

print("Rows after dissolve:", len(kab_gdf))

kab_gdf.to_file(
    "data/kabupaten_clean.geojson",
    driver="GeoJSON"
)

print("Finished.")