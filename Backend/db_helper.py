#creating database in MySQL
import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database="expense_tracking")

    if connection.is_connected():
        print("Successfully connected")
    else:
        print("Failed to connect")
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit == True:
        connection.commit()
    cursor.close()
    connection.close()
#fetching all data
def fetch_all():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM Transactions")
        results = cursor.fetchall()
        return results

#fetching all data filtered by date
def fetch_all_date(transaction_date):
    results = {}
    with get_db_cursor() as cursor:
        query = "SELECT * FROM Transactions WHERE transaction_date =%s"
        params = (transaction_date,)
        cursor.execute(query,params)
        results = cursor.fetchall()
    return results

#fetching all data filtered by user name
def fetch_all_by_user(user_name):
    a = []
    with get_db_cursor() as cursor:
        query = "SELECT * FROM Transactions WHERE user_name =%s"
        params = (user_name,)
        cursor.execute(query, params)
        results = cursor.fetchall()
        if results:
            for result in results:
                a.append(result)
            return a
        else:
            return (f"No result found for {user_name}")
        
#Inserting data
def insert_data(user_name, category, subcategory, amount, transaction_type, transaction_date, notes):
    with get_db_cursor(commit=True) as cursor:
        query = '''
        INSERT INTO Transactions (user_name, category, subcategory, amount, transaction_type, transaction_date, month, year, notes)
        VALUES (%s, %s, %s, %s, %s, %s, LEFT(MONTHNAME(%s), 3), YEAR(%s), %s)
        '''
        values = (
            user_name, category, subcategory, amount, transaction_type, transaction_date,
            transaction_date, transaction_date, notes
        )

        try:
            cursor.execute(query, values)
            print("Transaction added successfully!")
            # Fetch the inserted row using the LAST_INSERT_ID() function
            cursor.execute("SELECT * FROM Transactions WHERE transaction_id = LAST_INSERT_ID()")
            result = cursor.fetchone()  # Fetch the inserted row
            print("Inserted Row:", result)
            print(f"Rows affected: {cursor.rowcount}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


#deleting data
# def delete_data(transaction_date, transaction_id):
#     with get_db_cursor(commit=True) as cursor:
#
#         # If only one transaction_id is provided, handle it as a single item tuple
#         if len(transaction_id) == 1:
#             format_strings = '%s'  # Just one placeholder
#         else:
#             format_strings = ','.join(['%s'] * len(transaction_id))  # Multiple placeholders
#
#         query = f"DELETE FROM Transactions WHERE transaction_date = %s AND transaction_id IN ({format_strings})"
#
#         # Combine the transaction_date and transaction_ids into a single tuple
#         params = (transaction_date, *transaction_id)
#
#         try:
#             cursor.execute(query, params)
#             rows_affected = cursor.rowcount
#
#             if rows_affected > 0:
#                 print(f"Rows affected: {rows_affected}")
#                 return 200
#             else:
#                 print("No rows affected.")
#                 return 404
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return 500




#updating data
def update_data(transaction_id, user_name=None, category=None, subcategory=None, amount=None, transaction_type=None, transaction_date=None, notes=None):
    with get_db_cursor(commit=True) as cursor:
        query = '''
        UPDATE Transactions
        SET user_name = COALESCE(%s, user_name),
            category = COALESCE(%s, category),
            subcategory = COALESCE(%s, subcategory),
            amount = COALESCE(%s, amount),
            transaction_type = COALESCE(%s, transaction_type),
            transaction_date = COALESCE(%s, transaction_date),
            notes = COALESCE(%s, notes)
        WHERE transaction_id = %s
        '''
        values = (user_name, category, subcategory, amount, transaction_type, transaction_date, notes,transaction_id)
        cursor.execute(query, values)
        rows_affected = cursor.rowcount
        if rows_affected > 0:
            print(f"Transaction {transaction_id} updated successfully!")
            return 200  # HTTP 200 OK if rows were deleted
        else:
            raise Exception("No rows affected.")
        
#analysis by category
def analytics(start_date,end_date):
    a = []
    with get_db_cursor() as cursor:
        query = ('''SELECT category ,sum(amount) as total_sum FROM Transactions WHERE transaction_date BETWEEN %s AND %s 
        AND transaction_type = 'Debit' GROUP BY category''')
        params = (start_date,end_date)
        cursor.execute(query, params)
        results = cursor.fetchall()
        if results:
            for result in results:
                a.append(result)
            return a
        else:
            return (f"No result found")

#analysis by month
def analytics_year():
    a = []
    with get_db_cursor() as cursor:
        query = '''SELECT month(transaction_date)as month_n,monthname(transaction_date) as Month,sum(amount) as total_sum 
                      FROM Transactions 
                      WHERE transaction_type = 'Debit'
                      GROUP BY 1,2
                      order by 1,2 '''
        cursor.execute(query)
        answers = cursor.fetchall()
    for answer in answers:
        a.append(answer)
    return a

#deleting data by transaction_id
def delete_data(transaction_ids):
    with get_db_cursor(commit=True) as cursor:
        # Handle case where transaction_ids has only one element
        format_strings = ','.join(['%s'] * len(transaction_ids))
        query = f"DELETE FROM Transactions WHERE transaction_id IN ({format_strings})"
        params = transaction_ids
        
        try:
            # Execute the query with the correct parameters
            cursor.execute(query, tuple(params))
            rows_affected = cursor.rowcount

            if rows_affected > 0:
                print(f"Rows affected: {rows_affected}")
                return 200  # HTTP 200 OK if rows were deleted
            else:
                print("No rows affected.")
                return 404  # HTTP 404 Not Found if no rows were deleted

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 500  # HTTP 500 Internal Server Error in case of an error

#minimum and maximum date
def min_date():
    with get_db_cursor() as cursor:
        query = "SELECT MIN(transaction_date) as min_date from transactions"
        cursor.execute(query)
        result = cursor.fetchone()
        min_date = result['min_date']
        return min_date

def max_date():
    with get_db_cursor() as cursor:
        query = "SELECT MAX(transaction_date) as max_date from transactions"
        cursor.execute(query)
        result = cursor.fetchone()
        max_date = result['max_date']
        return max_date
if __name__ == '__main__':

   print(min_date())


    

   #print(fetch_all_date("2024-11-27"))


  #insert_data("Alice", "Food", "Groceries", "500", "Debit", "2024-12-03", "Monthly grocery ")






