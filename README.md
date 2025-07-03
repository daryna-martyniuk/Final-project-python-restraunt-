The project is an improvised system for accounting for menu items, tables and promotions, as well as creating orders for each table. A database with various types of relationships between entities is implemented here, as well as business logic and data validation (the teacher advised to transfer this validation to paydentic schemes).
Basic logic:
1) We can create a category of dishes and add dishes to it (one-to-many relationship)
2) We can also add tables and promotions (promotions have a certain period of time, both in days and in hours, for the implementation of promotions such as "morning discount")
3) It is possible to create an order tied to a specific table (another order cannot be added to a table that already contains an active order until the previous one is closed). An order consists of order items that contain a dish and its quantity.
Essences and methods:
DishCategory
- get_all
- get_by_id
- get_by_name
- create
- update
- delete
Dish
- get_all
- get_by_id
- get_by_name
- get_by_category_id
- get_dishes_on_promotion
- get_most_popular_dish
- sort_dishes_by_price
- create
- update
- delete
Promotion
- get_all
- get_by_id
- get_active_promotion
- create
- update
- delete
Order
- get_all
- get_by_id
- get_active_orders
- get_total_price
- get_orders_by_period
- create
- update
- complete_order
- delete
OrderItem
- get_all
- get_by_id
- get_by_order_id
- create
- update
- delete
CafeTable
- get_all
- get_by_id
- get_by_number
- get_tables_by_occupancy
- is_occupied
- create
- update
- delete
