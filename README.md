# ClientLine Backend

A FastAPI backend application for appointment and client management.

## Overview

ClientLine is a comprehensive appointment management system designed for organizations to manage their clients, staff, services, and payments. The system supports multi-organization architecture with role-based access control.

## Database Schema

The following diagram illustrates the system architecture:

<img width="1680" height="793" alt="Database Diagram" src="https://github.com/user-attachments/assets/196375ff-5edd-416a-9c18-0118afdb0536" />

### Tables

#### Organizations
Central entity for multi-tenant support.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| name | varchar | NOT NULL | Organization name |
| email | varchar | UNIQUE, NOT NULL | Contact email |
| phone | varchar | - | Contact phone number |
| address | text | - | Physical address |
| is_active | boolean | DEFAULT: true | Active status |
| created_at | timestamp | DEFAULT: now() | Creation timestamp |

#### Users
Manages all users including admins, managers, staff, and clients.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| organization_id | integer | FOREIGN KEY, NOT NULL | Reference to organizations |
| name | varchar | NOT NULL | User's name |
| email | varchar | UNIQUE, NOT NULL | User's email |
| phone | varchar | - | Contact phone number |
| role | varchar | NOT NULL | Role: admin, manager, staff, client |
| is_active | boolean | DEFAULT: true | Active status |
| created_at | timestamp | DEFAULT: now() | Creation timestamp |

#### Services
Services offered by organizations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| organization_id | integer | FOREIGN KEY, NOT NULL | Reference to organizations |
| name | varchar | NOT NULL | Service name |
| description | text | - | Service description |
| duration | integer | - | Duration in minutes |
| price | decimal(10,2) | - | Service price |
| is_active | boolean | DEFAULT: true | Active status |
| created_at | timestamp | DEFAULT: now() | Creation timestamp |

#### Appointments
Tracks scheduled appointments between clients and staff.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| organization_id | integer | FOREIGN KEY, NOT NULL | Reference to organizations |
| client_id | integer | FOREIGN KEY, NOT NULL | Reference to users (client) |
| staff_id | integer | FOREIGN KEY, NOT NULL | Reference to users (staff) |
| service_id | integer | FOREIGN KEY, NOT NULL | Reference to services |
| appointment_date | timestamp | NOT NULL | Scheduled date and time |
| status | varchar | DEFAULT: 'scheduled' | Status: scheduled, completed, cancelled, no_show |
| notes | text | - | Additional notes |
| created_at | timestamp | DEFAULT: now() | Creation timestamp |

#### Payments
Payment tracking for appointments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier |
| organization_id | integer | FOREIGN KEY, NOT NULL | Reference to organizations |
| appointment_id | integer | FOREIGN KEY, NOT NULL | Reference to appointments |
| amount | decimal(10,2) | NOT NULL | Payment amount |
| payment_method | varchar | - | Method: cash, card, online |
| status | varchar | DEFAULT: 'pending' | Status: pending, completed, failed, refunded |
| created_at | timestamp | DEFAULT: now() | Creation timestamp |

### Entity Relationships

```
organizations 1──────────< users
organizations 1──────────< services
organizations 1──────────< appointments
organizations 1──────────< payments
users (client) 1──────────< appointments
users (staff) 1──────────< appointments
services 1──────────< appointments
appointments 1──────────< payments
```

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Validation**: Pydantic
- **Server**: Uvicorn

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SuDelk/ClientLine_Backend.git
   cd ClientLine_Backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file with your database connection settings.

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

Currently implemented endpoints:

- `GET /` - API root (health check)
- `/organizations` - Organization management
- `/users` - User management

Additional endpoints for services, appointments, and payments will be added in future updates.

## License

This project is proprietary and confidential.
