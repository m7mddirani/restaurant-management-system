# Restaurant Management System

## Introduction

The Restaurant Management System is designed to streamline the operations of a restaurant, from managing orders to handling warehouse inventory. The system is divided into a client-server architecture to separate the responsibilities of order taking and backend processing. This project provides comprehensive management functionalities including order processing, warehouse management, and reporting.

## Project Structure

### Client Directory
- **main.py**: Initializes and starts the client application.
- **backend**:
  - **network.py**: Handles network communication between client and server.
  - **save_data.py**: Manages saving and loading of local client data.
  - **send_data.py**: Prepares data to be sent to the server.
- **frontend**:
  - **address.py**: Manages customer address input and validation.
  - **menu.py**: Displays the menu and handles order creation.
  - **images**: Contains images used in the client UI.

### Server Directory
- **main.py**: Initializes and starts the server application.
- **backend**:
  - **network.py**: Manages server-side network communication.
  - **save_data.py**: Handles saving and loading of server data.
  - **customer_history.py, earnings.py, economic_package_report.py, expiration_dates.py, low_stock_alert.py, materials_quantities.py, most_ordered.py, most_visited_days.py, most_visited_times.py, order_correction_report.py, order_delivery_report.py, reports_page.py, stock_aging_report.py, turnover_report.py, valuable_customer.py, warehouse_page.py**: Various reports and functionalities for managing restaurant operations.
- **frontend**:
  - **server_page.py**: Manages the main server UI.
  - **menu_page.py**: Displays the menu and handles order processing.
- **images**: Contains images used in the server UI.
- **data files**: JSON files for storing data like `customer_codes.json`, `menu.json`, `minimum_stock_levels.json`, `order_corrections.json`, `order_times.json`, `orders.json`, and `warehouse_data.json`.

## Key Functionalities

### Order Processing
- **Client Side**: Customers can browse the menu, select items, and place orders. The interface is user-friendly and allows customers to easily add or remove items from their orders.
- **Server Side**: Orders are received, processed, and managed. Each order contains detailed customer information and order items. The server provides functionalities to filter, edit, and print orders.

### Warehouse Management
- **Add/Edit/Remove Items**: Inventory can be managed through the warehouse page. Items can be added, edited, or removed with ease.
- **Stock Management**: The system provides various reports to monitor stock levels, expiration dates, and item usage. This helps in maintaining an optimal inventory and reducing waste.

### Reporting
The reporting functionality provides valuable insights into various aspects of the restaurant operations. Some of the key reports include:
- **Valuable Customers Report**: Helps in recognizing and rewarding loyal customers.
- **Low Stock Alert Report**: Ensures sufficient inventory and avoids stockouts.
- **Stock Aging Report**: Helps in managing freshness and reducing waste.
- **Warehouse Turnover Report**: Provides insights into the movement of inventory and helps in managing stock levels.

## Installation

**1. Clone the repository:**
```bash
   git clone https://github.com/your-repo/restaurant-management-system.git
```
**2. Navigate to the project directory:**
```bash
cd restaurant-management-system
```
**3. Create a virtual environment:**

```bash
python -m venv venv
```
**4. Activate the virtual environment:**  

**- On Windows:**  

```bash
venv\Scripts\activate
```
**- On macOS/Linux:**  

```bash
source venv/bin/activate
Install the required dependencies:
pip install -r requirements.txt
```  
## Usage
**1. Start the server:**

```bash
python server/main.py
```
**2. Start the client:**
```bash
python client/main.py
```
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes.