#!/usr/bin/env python3
"""
Bangkok Halal Restaurants Map - SEO & Directory Builder
Generates crawlable places.html and structured data
"""

import json
import os
from datetime import datetime


def build_places_html(gj):
    """Generate static places.html with Schema.org markup"""
    
    count = len(gj["features"])
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bangkok Halal Restaurants Directory</title>
    <meta name="description" content="Searchable directory of ''' + str(count) + ''' verified halal restaurants in Bangkok with certification status, prayer facilities, cuisines, and community reviews.">
    <meta property="og:title" content="Bangkok Halal Restaurants Directory">
    <meta property="og:description" content="Find halal-certified restaurants, prices, prayer rooms, and cuisines in Bangkok.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://example.com/places.html">
    
    <link rel="canonical" href="https://example.com/places.html">
    
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "name": "Bangkok Halal Restaurants Directory",
        "description": "Open directory of ''' + str(count) + ''' verified halal restaurants in Bangkok",
        "url": "https://example.com/places.html",
        "datePublished": "''' + datetime.now().isoformat() + '''",
        "license": "https://opendatacommons.org/licenses/odbl/",
        "isBasedOn": {
            "@type": "Dataset",
            "name": "Bangkok Halal Restaurants GeoJSON",
            "url": "https://example.com/data/halal_restaurants_bangkok.geojson",
            "distribution": {
                "@type": "DataDownload",
                "encodingFormat": "application/json",
                "url": "https://example.com/data/halal_restaurants_bangkok.geojson"
            }
        },
        "creator": {
            "@type": "Organization",
            "name": "Bangkok Halal Restaurants Contributors",
            "url": "https://github.com/yourname/halal-restaurants-bangkok"
        },
        "spatialCoverage": {
            "@type": "Place",
            "name": "Bangkok, Thailand",
            "geo": {
                "@type": "GeoShape",
                "box": "13.6 100.3 13.9 100.7"
            }
        }
    }
    </script>
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        header {
            background: #2c5f2d;
            color: white;
            padding: 2rem 1rem;
            text-align: center;
        }
        header h1 { font-size: 2rem; margin-bottom: 0.5rem; }
        header p { font-size: 1rem; opacity: 0.95; }
        .container { max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }
        .intro { background: white; padding: 1.5rem; border-radius: 4px; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .intro h2 { color: #2c5f2d; margin-bottom: 1rem; }
        .restaurants { display: grid; gap: 1rem; }
        .restaurant {
            background: white;
            padding: 1rem;
            border-left: 4px solid #2c5f2d;
            border-radius: 2px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .restaurant h3 { color: #2c5f2d; margin-bottom: 0.5rem; }
        .restaurant-meta { font-size: 0.9rem; color: #666; margin: 0.5rem 0; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 3px; font-size: 0.8rem; margin-right: 0.5rem; margin-bottom: 0.5rem; }
        .badge-zabiha { background: #c8e6c9; color: #1b5e20; }
        .badge-authority { background: #b3e5fc; color: #01579b; }
        .badge-self { background: #fff9c4; color: #f57f17; }
        .badge-unverified { background: #f0f0f0; color: #666; }
        .cuisines { color: #555; }
        .address { color: #666; font-size: 0.9rem; }
        .links { margin-top: 2rem; text-align: center; }
        .links a { display: inline-block; margin: 0.5rem; padding: 0.75rem 1.5rem; background: #2c5f2d; color: white; text-decoration: none; border-radius: 4px; }
        .links a:hover { background: #1b4620; }
        footer { background: #f0f0f0; padding: 2rem 1rem; text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem; }
        footer a { color: #2c5f2d; }
    </style>
</head>
<body>
    <header>
        <h1>🍽️ Bangkok Halal Restaurants Directory</h1>
        <p>''' + str(count) + ''' verified halal-certified restaurants with cuisine, price, and prayer facilities</p>
    </header>

    <div class="container">
        <div class="intro">
            <h2>Searchable Directory</h2>
            <p>Browse all ''' + str(count) + ''' halal restaurants in Bangkok, or <a href="/">use the interactive map</a> to filter by certification, cuisine, price range, and prayer facilities.</p>
        </div>
        
        <div class="restaurants" itemscope itemtype="https://schema.org/ItemList">
            <meta itemprop="itemListOrder" content="Unordered">
'''
    
    for i, feature in enumerate(gj["features"], 1):
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        cert_class = props["halal_cert"].lower().replace(" ", "-")
        
        phone_line = f'<div class="address"><strong>Phone:</strong> <a href="tel:{props["phone"]}">{props["phone"]}</a></div>' if props['phone'] else ''
        hours_line = f'<div class="address"><strong>Hours:</strong> {props["hours"]}</div>' if props['hours'] else ''
        notes_line = f'<div class="address"><strong>Notes:</strong> {props["notes"]}</div>' if props['notes'] else ''
        verified_line = f'<div class="address"><small>Verified: {props["verified_date"]}</small></div>' if props['verified_date'] else ''
        prayer_badge = '<span class="badge" style="background: #ffccbc; color: #bf360c;">🤲 Prayer Room</span>' if props['has_prayer_room'] else ''
        
        html += f'''
            <div class="restaurant" itemscope itemtype="https://schema.org/LocalBusiness">
                <meta itemprop="name" content="{props['name']}">
                <meta itemprop="geo" content="{coords[1]}, {coords[0]}">
                <meta itemprop="address" content="{props['address']}">
                <meta itemprop="telephone" content="{props['phone']}">
                <meta itemprop="openingHoursSpecification" content="{props['hours']}">
                
                <h3 itemprop="name">{props['name']}</h3>
                
                <div class="restaurant-meta">
                    <span class="badge badge-{cert_class}" itemprop="priceRange">{props['halal_cert']}</span>
                    <span class="badge" style="background: #f3e5f5; color: #4a148c;">{props['price_range']}</span>
                    {prayer_badge}
                </div>
                
                <div class="cuisines"><strong>Cuisines:</strong> {', '.join(props['cuisines'])}</div>
                <div class="address"><strong>Address:</strong> {props['address']}</div>
                {phone_line}
                {hours_line}
                {notes_line}
                {verified_line}
            </div>
'''
    
    html += '''
        </div>
    </div>
    
    <div class="links">
        <a href="/">🗺️ Interactive Map</a>
        <a href="/data/halal_restaurants_bangkok.geojson" download>📥 Download GeoJSON</a>
        <a href="https://github.com/yourname/halal-restaurants-bangkok" target="_blank">🔗 GitHub Repository</a>
    </div>
    
    <footer>
        <p>Licensed under <a href="https://opendatacommons.org/licenses/odbl/" target="_blank">ODbL 1.0</a> | 
        <a href="https://github.com/yourname/halal-restaurants-bangkok" target="_blank">Contribute</a> | 
        Last updated: ''' + datetime.now().strftime("%Y-%m-%d") + '''</p>
    </footer>
</body>
</html>
'''
    
    return html


def main():
    # Read generated data.js
    try:
        with open("docs/js/data.js", "r", encoding="utf-8") as f:
            js_content = f.read()
            # Extract JSON from: const RESTAURANTS = {...};
            json_str = js_content.replace("const RESTAURANTS = ", "").replace(";", "")
            gj = json.loads(json_str)
    except FileNotFoundError:
        print("✗ docs/js/data.js not found. Run build.py first.")
        return
    
    # Generate places.html
    html = build_places_html(gj)
    with open("docs/places.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✓ Generated docs/places.html with {len(gj['features'])} restaurants")
    print("✓ Schema.org structured data embedded for crawlers")


if __name__ == "__main__":
    main()
