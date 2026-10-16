# Vehicle Inventory & Booking API

A RESTful API built with Django and Django REST Framework to manage vehicle inventory and customer bookings.

## Live Deployment

**Base URL:** https://vehicle-inventory-booking-api-ax9h.onrender.com

### Live API Endpoints
- **List/Create Vehicles:** https://vehicle-inventory-booking-api-ax9h.onrender.com/api/vehicles/
- **Vehicle Details:** https://vehicle-inventory-booking-api-ax9h.onrender.com/api/vehicles/1/
- **List/Create Bookings:** https://vehicle-inventory-booking-api-ax9h.onrender.com/api/bookings/
- **Booking Details:** https://vehicle-inventory-booking-api-ax9h.onrender.com/api/bookings/1/

## Features

- Create, retrieve, update, and delete vehicles.
- List vehicles and filter by brand, fuel type, and availability.
- Create and retrieve customer bookings.
- Validate customer phone numbers and booking dates.
- Prevent overlapping bookings for the same vehicle.
- Automatically calculate booking amounts based on the daily vehicle price.
- Mark vehicles unavailable after a booking is created.

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- python-dotenv

## Prerequisites

- Python 3.10 or later, compatible with the installed Django version
- pip
- Git (optional)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd vehicle_system
```

If you already have the project locally, open its root directory instead.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install django djangorestframework python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root, alongside `manage.py`:

```env
SECRET_KEY=replace-with-your-own-secret-key
DEBUG=True
```

Generate a Django secret key using:

```powershell
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Replace the placeholder with the generated key. Never commit `.env` to a public repository.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The local API base URL is `http://127.0.0.1:8000/api/`.

## API Demo Video

Watch the 2–5 minute demonstration of the Vehicle Inventory & Booking API:

[Watch the API Demo](https://drive.google.com/file/d/1WI-2xBDgUZRm_d5bcIJP50WVoGxyLTw2/view?usp=sharing)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/vehicles/` | List vehicles |
| POST | `/api/vehicles/` | Create a vehicle |
| GET | `/api/vehicles/<id>/` | Retrieve a vehicle |
| PUT/PATCH | `/api/vehicles/<id>/` | Update a vehicle |
| DELETE | `/api/vehicles/<id>/` | Delete a vehicle |
| GET | `/api/bookings/` | List bookings |
| POST | `/api/bookings/` | Create a booking |
| GET | `/api/bookings/<id>/` | Retrieve a booking |

### Vehicle Filtering

Examples:

- `/api/vehicles/?brand=Honda`
- `/api/vehicles/?fuel_type=Petrol`
- `/api/vehicles/?is_available=true`

Filters can be combined, for example:

`/api/vehicles/?brand=Honda&fuel_type=Petrol`

## Sample Requests

### Create a vehicle

POST `/api/vehicles/`

```json
{
  "name": "City",
  "brand": "Honda",
  "year": 2024,
  "price_per_day": "1500.00",
  "fuel_type": "Petrol",
  "is_available": true
}
```

Supported fuel types: `Petrol`, `Diesel`, `Electric`, `Hybrid`.

### Create a booking

POST `/api/bookings/`

```json
{
  "vehicle": 1,
  "customer_name": "Anita Thomas",
  "customer_phone": "9876543210",
  "start_date": "2026-10-20",
  "end_date": "2026-10-22"
}
```

Use an existing vehicle ID and valid dates in the future.

The `total_amount` field is calculated by the API and should not be supplied by the client.

## Booking Validation

- Customer phone number must contain exactly 10 digits.
- Start date cannot be in the past.
- End date must be after the start date.
- Overlapping bookings for the same vehicle are rejected.
- Booking amount is calculated from the number of days and the vehicle's daily price.
- A vehicle is marked unavailable after a successful booking.

## Testing

Use the Django REST Framework browsable API, a REST client, or `curl` to test the endpoints.

Check successful vehicle and booking creation, filtering, invalid phone numbers, invalid dates, and overlapping bookings.

## Environment and Security

- Keep `.env` private.
- Use a strong, unique secret key.
- Set `DEBUG=False` in production.
- Configure production hosts and a production-ready database before deployment.
- Do not commit virtual environments or local database files.

## License

Add a license if required by the repository owner.
