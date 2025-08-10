# 🛒 E-Commerce Backend (Project Nexus - ProDev BE)

## 📌 Overview
A Django REST Framework backend for managing an e-commerce product catalog with JWT authentication, filtering, sorting, and pagination. Built as part of ALX ProDev Backend Engineering – Project Nexus.

---

## 🚀 Features
- **CRUD APIs** for `product_category` and `product`
- **JWT authentication** (login/refresh)
- **Filtering** (by category, price range, status)
- **Sorting** (by price, date, title)
- **Pagination** for large datasets
- **OpenAPI/Swagger documentation** at `/api/docs/`
- **Optimized DB** with indexes and query optimizations

---

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Auth:** SimpleJWT
- **Database:** PostgreSQL
- **Docs:** drf-spectacular
- **Deployment:** Render/Railway

---

## 📂 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/moussahassana/alx-project-nexus.git
cd alx-project-nexus
````

### 2️⃣ Install dependencies (Poetry)

```bash
poetry install
```

### 3️⃣ Set environment variables

Copy `.env.example` to `.env` and fill in your values.

```env
SECRET_KEY=change-me
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=ecomm
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4️⃣ Apply migrations

```bash
poetry run python manage.py migrate
```

### 5️⃣ Create superuser

```bash
poetry run python manage.py createsuperuser
```

### 6️⃣ Run server

```bash
poetry run python manage.py runserver
```

---

## 📌 API Endpoints

### Auth

* `POST /api/auth/token/` – get access & refresh token
* `POST /api/auth/refresh/` – refresh access token

### Product Categories

* `GET /api/product-categories/`
* `POST /api/product-categories/`
* `PUT/PATCH /api/product-categories/{slug}/`
* `DELETE /api/product-categories/{slug}/`

### Products

* `GET /api/products/` – filters: `product_category`, `min_price`, `max_price`, `is_active`
* `POST /api/products/`
* `PUT/PATCH /api/products/{slug}/`
* `DELETE /api/products/{slug}/`

---

## 📊 API Docs

* OpenAPI Schema: `/api/schema/`
* Swagger UI: `/api/docs/`

---

## 🌐 Deployment

**Hosted API:** on render

---

## 📜 License

MIT
