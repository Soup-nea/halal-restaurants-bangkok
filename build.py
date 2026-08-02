#!/usr/bin/env python3
"""
Bangkok Halal Restaurants Map - Build Pipeline
Converts source CSV → GeoJSON, static directory, OSM export, and sitemap
"""

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_restaurants(csv_path="data/restaurants.csv"):
    """Load and validate restaurants CSV"""
    if not os.path.exists(csv_path):
        print(f"✗ CSV not found: {csv_path}")
        return []
    
    recs = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            # Basic validation
            try:
                float(row["lat"])
                float(row["lon"])
            except (ValueError, KeyError):
                print(f"⚠ Row {i}: Invalid coordinates, skipping")
                continue
            
            recs.append(row)
    
    print(f"✓ Loaded {len(recs)} restaurants from {csv_path}")
    return recs


def to_geojson(recs):
    """Convert restaurants to GeoJSON FeatureCollection"""
    features = []
    
    for rec in recs:
        cuisines = [c.strip() for c in rec.get("cuisine_type", "").split(";") if c.strip()]
        
        feature = {
            "type": "Feature",
            "id": rec["id"],
            "geometry": {
                "type": "Point",
                "coordinates": [float(rec["lon"]), float(rec["lat"])]
            },
            "properties": {
                "name": rec.get("name", ""),
                "cuisines": cuisines,
                "halal_cert": rec.get("halal_cert", "Unverified"),
                "price_range": rec.get("price_range", ""),
                "has_prayer_room": rec.get("has_prayer_room", "").lower() == "yes",
                "address": rec.get("address", ""),
                "phone": rec.get("phone", ""),
                "hours": rec.get("hours", ""),
                "notes": rec.get("notes", ""),
                "verified_date": rec.get("verified_date", ""),
                "source": rec.get("source", "")
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "generated": datetime.now().isoformat(),
            "count": len(features),
            "license": "ODbL 1.0",
            "attribution": "Bangkok Halal Restaurants Contributors"
        }
    }


def to_osm(recs):
    """Convert to OSM XML format (for JOSM, not yet for bulk import)"""
    osm_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<osm version="0.6">\n'
    
    for i, rec in enumerate(recs, 1):
        lat = rec.get("lat", "0")
        lon = rec.get("lon", "0")
        name = rec.get("name", "").replace('"', "&quot;")
        cuisines = rec.get("cuisine_type", "").replace('"', "&quot;")
        halal = rec.get("halal_cert", "").replace('"', "&quot;")
        prayer = "yes" if rec.get("has_prayer_room", "").lower() == "yes" else "no"
        
        osm_xml += f'''  <node id="-{i}" lat="{lat}" lon="{lon}">
    <tag k="name" v="{name}"/>
    <tag k="cuisine" v="{cuisines}"/>
    <tag k="halal" v="{halal}"/>
    <tag k="amenity" v="restaurant"/>
    <tag k="prayer_room" v="{prayer}"/>
    <tag k="source" v="Bangkok Halal Restaurants Map"/>
  </node>
'''
    
    osm_xml += '</osm>'
    return osm_xml


def generate_sitemap(recs, base_url="https://yourname.github.io/halal-restaurants-bangkok"):
    """Generate XML sitemap for SEO"""
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{base_url}/</loc><priority>1.0</priority></url>\n'
    sitemap += f'  <url><loc>{base_url}/places.html</loc><priority>0.9</priority></url>\n'
    sitemap += f'  <url><loc>{base_url}/data/halal_restaurants_bangkok.geojson</loc><priority>0.8</priority></url>\n'
    
    for rec in recs:
        # One URL per restaurant (for link equity)
        url = f"{base_url}/#restaurant/{rec['id']}"
        sitemap += f'  <url><loc>{url}</loc><priority>0.7</priority></url>\n'
    
    sitemap += '</urlset>'
    return sitemap


def generate_robots_txt():
    """Generate robots.txt for crawlers"""
    return """User-agent: *
Allow: /
Disallow: /admin/

Sitemap: https://example.com/sitemap.xml
"""


def main():
    # Ensure output directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("js", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    
    # Load data
    recs = load_restaurants()
    if not recs:
        print("✗ No restaurants to process")
        sys.exit(1)
    
    # Generate GeoJSON
    gj = to_geojson(recs)
    
    # Write data.js for Leaflet map (client-side)
    with open("docs/js/data.js", "w", encoding="utf-8") as f:
        f.write("const RESTAURANTS = ")
        json.dump(gj, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";")
    print("✓ Generated docs/js/data.js")
    
    # Write public GeoJSON dataset
    with open("docs/data/halal_restaurants_bangkok.geojson", "w", encoding="utf-8") as f:
        json.dump(gj, f, ensure_ascii=False, indent=2)
    print("✓ Generated docs/data/halal_restaurants_bangkok.geojson")
    
    # Write OSM file
    with open("docs/data/bangkok_halal_restaurants_for_josm.osm", "w", encoding="utf-8") as f:
        f.write(to_osm(recs))
    print("✓ Generated docs/data/bangkok_halal_restaurants_for_josm.osm")
    
    # Write sitemap
    with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(generate_sitemap(recs))
    print("✓ Generated docs/sitemap.xml")
    
    # Write robots.txt
    with open("docs/robots.txt", "w", encoding="utf-8") as f:
        f.write(generate_robots_txt())
    print("✓ Generated docs/robots.txt")
    
    print(f"\n✓ Build complete: {len(recs)} restaurants ready for deployment")


if __name__ == "__main__":
    main()
