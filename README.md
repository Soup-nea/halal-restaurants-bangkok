# Bangkok Halal Restaurants Map 🍽️

A community-driven, open-data map of verified halal restaurants in Bangkok. Mobile-friendly PWA with offline support, searchable by certification status, cuisine type, price range, and prayer facilities.

**Live Demo:** https://yourname.github.io/halal-restaurants-bangkok  
**Data License:** [ODbL 1.0](https://opendatacommons.org/licenses/odbl/)  
**Dataset:** https://yourname.github.io/halal-restaurants-bangkok/data/halal_restaurants_bangkok.geojson  

---

## Features

✅ **Interactive Leaflet Map** — Search, filter, and view halal restaurants in real-time  
✅ **Mobile-Friendly PWA** — Works offline, installable on home screen  
✅ **Certification-First Filtering** — Zabiha, Halal Authority, Self-certified, Unverified  
✅ **Multi-Criteria Search** — Filter by cuisine, price, prayer facilities  
✅ **Crawlable Directory** — SEO-optimized `/places.html` for search engines  
✅ **Open GeoJSON Dataset** — Downloadable for use in other projects  
✅ **Community-Driven** — Submit corrections via Google Form  
✅ **Zero Backend Costs** — Hosted on GitHub Pages, built with GitHub Actions  

---

## Quick Start: Add a Restaurant

### Option 1: Edit the CSV directly (for contributors)

1. **Fork this repo** and clone locally:
   ```bash
   git clone https://github.com/yourname/halal-restaurants-bangkok.git
   cd halal-restaurants-bangkok
   ```

2. **Edit `data/restaurants.csv`** and add a new row:
   ```csv
   HLR_BKK_011,Restaurant Name,13.7563,100.5018,"Thai; Middle Eastern",Zabiha,$$,Yes,"123 Sukhumvit Rd","0812345678","11:00-22:00","Notes here","Your Name","2024-01-20"
   ```

3. **Run the build pipeline**:
   ```bash
   python build.py
   python build_seo.py
   ```

4. **Commit and push**:
   ```bash
   git add data/restaurants.csv docs/
   git commit -m "Add: Restaurant Name"
   git push
   ```

5. **Create a Pull Request** — we'll review and merge!

### Option 2: Submit via Google Form (no coding required)

[Submit a restaurant](https://forms.gle/yourformlink) — we'll verify and add it to the map.

---

## Data Schema

`data/restaurants.csv` uses this structure:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | String | `HLR_BKK_001` | Stable unique ID (don't change) |
| `name` | String | `Al Reef Bakery` | Restaurant name |
| `lat` | Float | `13.7563` | Latitude (Google Maps) |
| `lon` | Float | `100.5018` | Longitude (Google Maps) |
| `cuisine_type` | String | `Thai; Middle Eastern` | Semicolon-separated list |
| `halal_cert` | Enum | `Zabiha` | One of: Zabiha, Halal Authority, Self-certified, Unverified |
| `price_range` | String | `$$` | `$`, `$$`, or `$$$` |
| `has_prayer_room` | Boolean | `Yes` | Yes or No |
| `address` | String | `123 Sukhumvit Rd` | Full street address |
| `phone` | String | `0812345678` | Thai format (0XX-XXX-XXXX) |
| `hours` | String | `11:00-22:00` | Operating hours (24h format) |
| `notes` | String | `Popular for bread` | Optional notes |
| `source` | String | `Community submission` | How you found it |
| `verified_date` | String | `2024-01-15` | Last verification date (YYYY-MM-DD) |

### Finding Coordinates

1. Go to [Google Maps](https://maps.google.com)
2. Right-click on the restaurant location → **coordinates appear at bottom**
3. Copy as `lat,lon` (e.g., `13.7563, 100.5018`)

---

## Tech Stack

- **Frontend:** Leaflet.js (map), vanilla JavaScript
- **Data Pipeline:** Python 3 (CSV → GeoJSON, OSM, SEO)
- **Hosting:** GitHub Pages (free)
- **CI/CD:** GitHub Actions (auto-build on CSV changes)
- **PWA:** Service Worker + Web App Manifest
- **License:** Open Data Commons (ODbL 1.0)

---

## File Structure

```
halal-restaurants-bangkok/
├── README.md                           # This file
├── LICENSE                             # ODbL 1.0 license
├── data/
│   └── restaurants.csv                 # 🔑 Single source of truth
├── build.py                            # CSV → GeoJSON, OSM, sitemap
├── build_seo.py                        # CSV → crawlable places.html
├── .github/
│   └── workflows/
│       └── build.yml                   # Auto-deploy on push
└── docs/                               # 📦 Published GitHub Pages site
    ├── index.html                      # Interactive map + search
    ├── places.html                     # SEO directory (auto-generated)
    ├── manifest.json                   # PWA manifest
    ├── sw.js                           # Service Worker (offline)
    ├── robots.txt                      # SEO crawlability (auto-generated)
    ├── sitemap.xml                     # SEO sitemap (auto-generated)
    ├── js/
    │   ├── app.js                      # Main app logic
    │   └── data.js                     # GeoJSON (auto-generated)
    └── data/
        ├── halal_restaurants_bangkok.geojson    # Open dataset
        └── bangkok_halal_restaurants_for_josm.osm  # OSM export
```

---

## Setup for Development

### Prerequisites
- Python 3.7+
- Git
- GitHub account

### Local Installation

```bash
# Clone repo
git clone https://github.com/yourname/halal-restaurants-bangkok.git
cd halal-restaurants-bangkok

# Edit data/restaurants.csv
nano data/restaurants.csv

# Build pipeline
python build.py      # CSV → GeoJSON, OSM
python build_seo.py  # CSV → places.html

# Serve locally (Python 3.7+)
python -m http.server 8000
# Open: http://localhost:8000/docs/

# Or with Python 2:
python -m SimpleHTTPServer 8000 &
cd docs && python -m SimpleHTTPServer 8001
```

---

## Deployment to GitHub Pages

### First-Time Setup

1. **Create a GitHub repo**: `halal-restaurants-bangkok`
2. **Enable GitHub Pages**:
   - Settings → Pages → Source: `GitHub Actions` or `Branch: main /docs`
3. **Add CNAME** (optional, for custom domain):
   ```bash
   echo "halal.bangkok" > docs/CNAME
   git add docs/CNAME && git commit -m "Add custom domain"
   ```
4. **Push to main branch**:
   ```bash
   git push origin main
   ```
5. **GitHub Actions auto-runs** `build.yml` → rebuilds and deploys ✨

### Every Update
Just edit `data/restaurants.csv`, commit, and push. GitHub Actions handles the rest!

---

## Open Data: Download & Reuse

### Formats Available

1. **GeoJSON** (Leaflet, Mapbox, ArcGIS):
   ```
   https://yourname.github.io/halal-restaurants-bangkok/data/halal_restaurants_bangkok.geojson
   ```

2. **OSM File** (JOSM, iD editor):
   ```
   https://yourname.github.io/halal-restaurants-bangkok/data/bangkok_halal_restaurants_for_josm.osm
   ```

3. **CSV** (Excel, Google Sheets):
   Download from `data/restaurants.csv` in GitHub

### Embed in Your Project

```html
<!-- Embed GeoJSON in Leaflet -->
<script src="https://yourname.github.io/halal-restaurants-bangkok/data/halal_restaurants_bangkok.geojson"></script>
<script>
  fetch('https://yourname.github.io/halal-restaurants-bangkok/data/halal_restaurants_bangkok.geojson')
    .then(r => r.json())
    .then(data => L.geoJSON(data).addTo(map));
</script>
```

### License & Attribution

You're free to:
- ✅ Copy, modify, and reuse this dataset
- ✅ Build derivative maps (Google My Maps, OSM, etc.)
- ✅ Commercial use

You must:
- 📌 **Attribute** "Bangkok Halal Restaurants Contributors"
- 📌 **Share-alike** — any improvements are public ([ODbL 1.0](https://opendatacommons.org/licenses/odbl/))

---

## SEO & Discoverability

### Google Search Console
1. Verify your site: https://search.google.com/search-console
2. Submit sitemap: `/sitemap.xml` (auto-generated)
3. Monitor indexing: should see 300+ URLs indexed

### Structured Data (Schema.org)
- `/places.html` includes `DataCatalog` + `LocalBusiness` JSON-LD
- Tested with [Google's Rich Results Test](https://search.google.com/test/rich-results)

### SEO Strategy
| Channel | Action | Impact |
|---------|--------|--------|
| **Google Search** | Submit sitemap + structured data | #1-3 for "halal restaurants Bangkok" |
| **Google My Business** | Batch-upload restaurants | Google Maps listings |
| **OpenStreetMap** | Create discussion thread (don't bulk-import yet) | Community import path |
| **Kaggle Datasets** | Publish GeoJSON | Free data discovery |
| **Twitter/Bluesky** | Link from halal communities | Traffic + awareness |

---

## Community Feedback Loop

### Report an Issue / Send Feedback

**Option 1: GitHub Issues**
[Create an issue](https://github.com/yourname/halal-restaurants-bangkok/issues)

**Option 2: Google Form**
[Submit feedback](https://forms.gle/yourformlink)

**Option 3: Email**
contact@example.com

### Corrections Workflow

1. **Report:** "Restaurant X hours are wrong" or "Add new restaurant Y"
2. **Verify:** We confirm with photos, review, or community vote
3. **Update:** CSV is edited → `build.py` runs → site updates automatically
4. **Confirm:** You get an email: "Done! Updated on [date]"

---

## Roadmap

### Phase 1 (Now)
- [x] Data schema finalized
- [x] Leaflet map + search
- [x] PWA + offline
- [x] GeoJSON export
- [x] GitHub Pages hosting
- [ ] 50+ verified restaurants

### Phase 2 (Q2 2024)
- [ ] 200+ restaurants
- [ ] Community feedback form integration
- [ ] Google My Business batch upload
- [ ] Mobile app (Expo/React Native)

### Phase 3 (Q4 2024)
- [ ] OSM bulk import discussion
- [ ] Halal authority partnership
- [ ] Multi-city expansion (Chiang Mai, Phuket)

---

## FAQ

**Q: Can I use this data for my app/website?**  
A: Yes! It's open under ODbL 1.0. Just attribute us and share improvements back.

**Q: How often is the data updated?**  
A: Whenever someone edits `data/restaurants.csv` and we verify. Usually within 1-2 weeks.

**Q: Does the map work offline?**  
A: Yes! The PWA caches the map and restaurant data. Tiles are cached after first view.

**Q: Can I submit new restaurants?**  
A: Yes, via Google Form or by editing `data/restaurants.csv` directly (if you're comfortable with GitHub).

**Q: How do I report a closed restaurant?**  
A: Edit the CSV (remove the row) → push → we'll merge. Or fill out the feedback form.

**Q: Why ODbL and not CC0?**  
A: ODbL requires attribution + share-alike, preventing commercial lockdown of our data.

---

## Contributors

[Add your name here after your first PR!]

---

## Support This Project

- ⭐ Star the repo
- 🔗 Link from your website
- 📝 Submit corrections
- 🤝 Contribute restaurants
- 💬 Share in halal communities

---

## License

**Data License:** Open Data Commons ODDbL 1.0  
**Code License:** MIT  

See [LICENSE](./LICENSE) for details.

---

## Contact

- 📧 Email: contact@example.com
- 🐙 GitHub: [@yourname](https://github.com/yourname)
- 📍 Maps: [Bangkok Halal Restaurants](https://yourname.github.io/halal-restaurants-bangkok)

---

**Last Updated:** 2024-01-20  
**Data Points:** 10+ restaurants (beta)  
**Next Update:** 2024-02-15
