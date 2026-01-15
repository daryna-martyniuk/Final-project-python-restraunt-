# Cafe Management API

A REST API designed to automate cafe operations. The system manages the menu, processes orders, assigns them to tables, and applies promotional offers.

## Operational Description and Rules

The program implements the full client service cycle from order creation to completion.

Key Business Logic Rules:
1. Single Active Order per Table: A table can have only one active (not completed) order at a time. The system blocks attempts to create a new order for an occupied table.
2. Order Lifecycle: An order is created with an "active" status. After payment or service completion, it transitions to a "completed" status (is_completed = True).
3. Cost Calculation: Active promotions are automatically checked when calculating the order total. If a dish is part of a valid promotion (based on date and time), a discount is applied.
4. Data Validation: The system validates the existence of dishes and tables in the database before order creation and ensures that item quantities are positive.

## Database Entities

The system is built on a relational database and includes the following entities:

* DishCategory — Grouping for dishes (e.g., Drinks, Desserts).
* Dish — A specific menu item with a name, price, and description.
* CafeTable — A physical table in the establishment with a number and location.
* Order — The main entity linked to a table and creation time.
* OrderItem — An intermediate entity linking an order to specific dishes and their quantities.
* Promotion — Discount rules applicable to specific dishes during a defined time period.

## Technologies

The project utilizes a modern Python web development stack:

* Python 3.12
* FastAPI — Web framework for building APIs.
* PostgreSQL — Relational database.
* SQLAlchemy 2.0 — ORM for database interaction.
* Pydantic v2 — Data validation and serialization.
* Alembic — Database migration management tool.
* Docker — Application containerization.