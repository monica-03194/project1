# Client Query Management System

A full-stack **Client Query Management System** built with:

- 🐍 Python
- 🗄 MySQL
- 📊 Streamlit
- 🧮 Pandas

It allows **clients** to submit queries and **support teams** to track, close, and analyze them.

---

## 🎯 Features

### 👤 Authentication & Roles

- User registration with:
  - Username
  - Password (hashed using SHA-256)
  - Role: `Client` or `Support`
  - Mobile number
- Secure login and role-based dashboards.

### 📨 Client Features

- Submit new queries with:
  - Email
  - Mobile number
  - Query heading
  - Description
- Automatic:
  - `query_id` (format: `Q0001`, `Q0002`, ...)
  - `status = Open`
  - `date_raised = current timestamp`
- View:
  - **All queries**
  - **My queries** (filtered by mobile number)

### 🛠 Support Features

- View all client queries.
- Filter queries by status: `All / Open / Closed`.
- Close a query:
  - Updates `status` → `Closed`
  - Sets `date_closed = current timestamp`
- Analytics:
  - Total, Open, Closed counts.
  - Daily query trend (line chart).
  - Resolution time analysis:
    - Average resolution time
    - Fastest and slowest resolution
    - Per-query resolution hours chart.

---

## 🧱 Project Structure

```text
client-query-management-system/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── utils/
│   ├── db.py
│   ├── auth.py
│   ├── queries.py
│   └── analytics.py
└── database/
    ├── schema.sql
    └── seed_data.py
```
