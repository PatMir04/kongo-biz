# KongoBiz - Business Directory & Review Platform for DR Congo

A Yelp-like local business directory and review platform built specifically for the Democratic Republic of Congo. Built with Django and designed for mobile-first, low-bandwidth environments.

## Project Status

| Feature | Status |
|---------|--------|
| Project Setup & README | Done |
| Django Project Structure | Done |
| Business Listings App (models, views, search) | Done |
| User Accounts App (register, login, profiles) | Done |
| Reviews & Ratings App | Done |
| Homepage & Base Templates | Done |
| Static Files (CSS/JS) | Done |
| Map Integration (OpenStreetMap/Leaflet) | Pending |
| Photo Upload System | Pending |
| Business Owner Dashboard | Pending |
| Mobile Money Integration | Pending |
| API Endpoints (DRF) | Pending |
| Deployment Config | Pending |
| PWA Offline Support | Pending |

## Tech Stack

- **Backend:** Django 5.x, Python 3.11+
- **Database:** SQLite (dev) / PostgreSQL + PostGIS (prod)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Maps:** Leaflet.js + OpenStreetMap
- **Search:** Django full-text search / PostgreSQL trigram
- **Auth:** Django built-in auth + social auth
- **Deployment:** Gunicorn, Nginx, Docker

## Project Structure

```
kongo-biz/
|-- manage.py
|-- requirements.txt
|-- kongobiz/              # Django project config
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|-- businesses/            # Business listings app
|   |-- models.py
|   |-- views.py
|   |-- urls.py
|   |-- forms.py
|   |-- admin.py
|-- accounts/              # User auth & profiles
|   |-- models.py
|   |-- views.py
|   |-- urls.py
|   |-- forms.py
|-- reviews/               # Reviews & ratings
|   |-- models.py
|   |-- views.py
|   |-- urls.py
|   |-- forms.py
|-- templates/             # HTML templates
|   |-- base.html
|   |-- home.html
|   |-- businesses/
|   |-- accounts/
|   |-- reviews/
|-- static/                # CSS, JS, images
|   |-- css/
|   |-- js/
|   |-- images/
```

## DRC-Specific Features

- **French language** as primary UI language
- **Lingala, Swahili, Tshiluba, Kikongo** support planned
- **Mobile-first** responsive design
- **Low-bandwidth** optimized (compressed images, minimal JS)
- **Cities:** Kinshasa, Lubumbashi, Goma, Bukavu, Mbuji-Mayi, Kisangani, Kananga, Kolwezi
- **Categories:** Restaurants, Hotels, Pharmacies, Hospitals, Schools, Markets, Transport, Banks, Salons, Auto Repair
- **Mobile Money:** M-Pesa, Airtel Money, Orange Money integration (planned)
- **PWA:** Progressive Web App for offline access (planned)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/PatMir04/kongo-biz.git
cd kongo-biz

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata sample_data.json

# Run the server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the app.

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

MIT
