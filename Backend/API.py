from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel
from typing_extensions import Optional
import traceback

import db_helper

app = FastAPI()

# Pydantic model for a adding expense
class Transaction(BaseModel):
    user_name: str
    category: str
    subcategory: str
    amount: float
    transaction_type: str
    notes: Optional[str] = None


#pydantic model for retrieving expense
class Retrieve(BaseModel):
    transaction_id : int
    user_name: str
    category: str
    subcategory: str
    amount: float
    transaction_type: str
    notes: str

#pydantic model for analytics
class summary(BaseModel):
    start_date : date
    end_date:date

class analytics(BaseModel):
    Month : str
    total_sum :float

class DeleteTransactionRequest(BaseModel):
    transaction_ids: List[int]

class updateTransaction(BaseModel):
    transaction_id:int
    user_name: str
    category: str
    subcategory: str
    amount: float
    transaction_type: str
    transaction_date:str
    notes: Optional[str] = None



#insert data API
@app.post("/expenses/{expense_date}")
def add_transactions(expense_date: date, transaction: Transaction):
    try:
        # Set the transaction date
        transaction_date = expense_date

        # Insert data into the database for each transaction
        db_helper.insert_data(
                user_name=transaction.user_name,
                category=transaction.category,
                subcategory=transaction.subcategory,
                amount=transaction.amount,
                transaction_type=transaction.transaction_type,
                transaction_date=transaction_date,
                notes=transaction.notes
            )     

        # Return a success response after processing all transactions
        return {"message": "Transactions added successfully!"}

    except Exception as e:
        return {"error": str(e)}
# #Get request using retrieve model
@app.get("/expenses/{expense_date}", response_model=List[Retrieve])
def get_transactions(expense_date: date):
    expenses = db_helper.fetch_all_date(expense_date)
    return expenses

#post request for analytics

@app.post("/analytics")
def get_analytics(date_range:summary):
    data = db_helper.analytics(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code= 500,detail = "Failed to retrieve data for analytics")
    else:
        total = sum(record['total_sum'] for record in data)
        breakdown = {}

        for record in data:
            percentage = round((record['total_sum'] / total) * 100,2)if record['total_sum'] > 0 else 0
            breakdown[record['category']] = {
                "Total": record['total_sum'],"Percent%":percentage
            }
        return breakdown
#get request for month wise
@app.get("/month/analytics",response_model= list[analytics])
def get_month_analytics():
    data = db_helper.analytics_year()
    if data is None:
        raise HTTPException(status_code= 500,detail = "Failed to retrieve data for analytics")
    else:
        return data



@app.delete("/expenses")
def delete_transaction(request: DeleteTransactionRequest):
    # The request will automatically be parsed into the DeleteTransactionRequest model
    transaction_ids = request.transaction_ids

    # Check if transaction_ids is empty
    if not transaction_ids:
        return {"message": "No transaction IDs provided for deletion"}, 400

    try:
        # Call the delete_data function with the date and list of IDs
        success = db_helper.delete_data(transaction_ids)
        if success == 200:
            return {"message": "Transactions deleted successfully!"}
        elif success == 400:
            return {"message": "Bad Request: Invalid data provided."}, 400

        elif success == 404:
            return {"message": "No transactions found for deletion with the provided IDs."}, 404

        else:
            # Handle any unexpected status codes
            return {"message": "An unexpected error occurred."}, 500

    except Exception as e:
        # Return detailed error message in the response
        error_details = traceback.format_exc()
        return {"message": f"An error occurred: {str(e)}", "details": error_details}, 500
    

@app.put("/expenses/update")
def update_transaction(request: updateTransaction):
    # The request will automatically be parsed into the DeleteTransactionRequest model
    #transaction_id = request.transaction_id

    # Check if transaction_ids is empty
    if not request.transaction_id:
        return {"message": "No transaction IDs provided for deletion"}, 400
    try :
        db_helper.update_data(
                transaction_id=request.transaction_id,
                user_name=request.user_name,
                category=request.category,
                subcategory=request.subcategory,
                amount=request.amount,
                transaction_type=request.transaction_type,
                transaction_date=request.transaction_date,
                notes=request.notes
            )
        return {"message": "Successfully updated"}
    except Exception as e:
        raise e

 #retriving min and maximum date for tab2   
@app.get("/min_date")
def get_min_date():
    min_date  = db_helper.min_date()  # Call the function to get the min and max dates from the database
    return min_date  # Return the min and max dates as a dictionary
@app.get("/max_date")
def get_max_date():
    max_date  = db_helper.max_date()  # Call the function to get the min and max dates from the database
    return max_date  # Return the min and max dates as a dictionary