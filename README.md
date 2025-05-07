# 🌍 Emissions Calculation Engine

This project is a Django-based API and processing engine for calculating carbon emissions from 
structured activity data. It ingests CSV files for air travel, electricity usage, 
and purchased goods — validates them, applies emission factors, and stores calculated emissions to the database.

---

## 🚀 Features

- Upload CSVs to calculate emissions based on activity type
- Auto-detects activity type via headers
- Validates incoming data using serializers
- Calculates CO₂e, and stores as `EmissionFactor` records
- Includes API tests and serializer validation
- Includes a simple frontend page for viewing emission data

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/alisever/minimum-task.git
cd minimum-task
```

### 2. Create a Virtual Environment
This project was built with Python 3.13. The instructions below assume you are using a Unix-like system (Linux, macOS). If you're on Windows, you may need to adjust the commands accordingly.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the application

```bash
python manage.py runserver
```

### 6. Seed test data
While the app is running, run the following commands.

```bash
curl -X POST -F "file=@emissions/tests/fixtures/air_travel.csv" http://localhost:8000/emissions/upload-emissions/
curl -X POST -F "file=@emissions/tests/fixtures/electricity.csv" http://localhost:8000/emissions/upload-emissions/
curl -X POST -F "file=@emissions/tests/fixtures/purchased_goods_and_services.csv" http://localhost:8000/emissions/upload-emissions/
```

### 7. View the frontend
Open your browser and navigate to `http://localhost:8000/emissions/emissions/` to view the frontend page for viewing emission data.

---

## 🧪 Running Tests

```bash
pytest
```

---

## ✨ To Do

- [ ] Write a management command to seed the database
- [ ] Add an endpoint to update/create EmissionFactor records
- [ ] Investigate and improve validation for Activity Data
- [ ] Add Swagger/OpenAPI docs

---

## 📫 Contact

Made by Ali Sever