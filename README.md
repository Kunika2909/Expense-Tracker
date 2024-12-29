# Expense tracker
<img src="https://happay.com/blog/wp-content/uploads/sites/12/2022/08/non-operating-expenses.png" alt="Project Logo" width="300" height="200">

## Overview
This project is a Python-based application designed to streamline data management and analysis processes. It employs an Object-Oriented Design (OOD) approach, with classes that structure the application's logic for better readability, maintainability, and scalability. The project integrates a responsive UI, a backend, and a  database to provide CRUD operations, data visualization, and dashboard functionalities.
### Technologies Used :
- **Frontend/UI**: Streamlit 
- **Backend/API**: FastAPI 
- **Database**: MySQL
### Key Features :
**Seamless Navigation:** Switch between tabs for CRUD operations, data visualization, and the dashboard with ease.
- **Tab 1: CRUD Operations**
    -  Perform Create, Read, Update, and Delete operations through a dynamic interface.
    - Modular class design to handle CRUD logic, ensuring reusability and clarity.
    - Support for adding, editing, and deleting rows directly from the UI.
      
- **Tab 2: Analytics by category**
    - View spending trends by category within custom date ranges
      
- **Tab 3: Dashboard**
    - Refresh data and filter by month/year.
    - Highlight top spender.
    - KPIs: Total spend, Total earn, and Net balance.
    - Heatmap calendar for monthly debit flow.
    - Category-wise expense distribution.
### File and Folder Structure Explanation 
```
.
├── Backend
│   ├── API.py
│   ├── __pycache__
│   ├── db_helper.py
│   └── venv
├── Data
│   └── transactions.csv
├── Frontend
│   ├── __pycache__
│   ├── frontend.py
│   ├── tab_1.py
│   ├── tab_2.py
│   ├── tab_3.py
│   └── venv
├── README.md
└── requirements.txt
```
## Setup
Installing MySQL
1) In the terminal run :- 
```
brew install mysql
```
2) Starting mysql
```
brew services start mysql
```
3) Creating database
```
CREATE DATABASE expense_tracking
```
4) Utilised Chatgpt for creating data and storing it in csv
   [Download transactions.csv](/Expense-Tracker/Data/transactions.csv)
5) In Mysql Workbench navigate to created database and run :-
   ```
    CREATE TABLE expense_tracking.transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100) NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    transaction_date DATE NOT NULL, year VARCHAR(4) NOT NULL,
    month VARCHAR(10) NOT NULL,
    notes VARCHAR(256) NULL,
    CHECK (user_name IN ('Alice', 'Bob', 'Emily', 'Mark')),
    CHECK (category IN ('Income', 'Food', 'Healthcare', 'Housing', 'Personal Care', 'Travel')),
    CHECK (transaction_type IN ('Credit', 'Debit')) );
   ```

7) In the terminal run :-
```
LOAD DATA LOCAL INFILE 'path/to/file/transactions.csv' -> INTO TABLE expense_tracking.transactions -> FIELDS TERMINATED BY ',' -> LINES TERMINATED BY '\n' -> IGNORE 1 ROWS -> (transaction_id, user_name, category, subcategory, amount, transaction_type, @transaction_date, year, month, notes) -> SET transaction_date = STR_TO_DATE(@transaction_date, '%Y-%m-%d');

```

8) In new terminal navigate to project folder -

```
cd/path/to/your/expense-tracker-folder/Frontend
```
- Creating virtual environment
```
python3 -m venv venv
````
- Activate it
```
source venv/bin/activate
```
- Install the Requirements file
```
pip3 install -r requirements.txt
```
- Run
```
streamlit run frontend.py
```

9) In new terminal navigate to project folder -
```
cd/path/to/your/expense-tracker-folder/Backend
```
- Creating virtual environment
```
python3 -m venv venv
````
- Activate it
```
source venv/bin/activate
```
- Install the Requirements file
```
pip3 install -r requirements.txt
```
- Run
```
uvicorn app:API --reload
```


    
      


