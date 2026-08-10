import json
import yaml
from pathlib import Path
from catalog_pipeline.ingest import esri

BASE = Path(__file__).resolve().parent
SOURCES = BASE / "sources.yaml"
CATALOG = BASE / "catalog.json"


def build_catalog():
    config = yaml.safe_load(SOURCES.read_text(encoding="utf-8"))
    ramps = []
    for source in config["sources"]:
        if source["type"] == "esri":
            print(f"Ingesting {source['name']}...")
            ramps.extend(esri.fetch_ramps(source["url"]))

    data = [ramp.model_dump() for ramp in ramps]
    CATALOG.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Built catalog with {len(ramps)} ramps -> {CATALOG}")
    return ramps


if __name__ == "__main__":
    build_catalog()