# ClientLine Backend

A FastAPI backend application for appointment and client management.

## Overview

ClientLine is a comprehensive appointment management system designed for organizations to manage their clients, staff, services, and payments. The system supports multi-organization architecture with role-based access control.

<img width="1680" height="793" alt="Database Diagram" src="https://github.com/user-attachments/assets/196375ff-5edd-416a-9c18-0118afdb0536" />

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
