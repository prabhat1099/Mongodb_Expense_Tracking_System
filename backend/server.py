from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel
import db_helper
from logging_setup import setup_logger
from fastapi.responses import JSONResponse

logger = setup_logger("server_logger")

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/")
async def home_page():
    return "welcome to expense tracker app"   

 # ---------------------------------------
# 1️⃣ FETCH EXPENSES FOR A GIVEN DATE
# ---------------------------------------

@app.get("/expenses/{expense_date}",response_model=List[Expense])
async  def get_expenses(expense_date: date):
    try:
      expenses =await db_helper.fetch_expenses_for_date(str(expense_date)) 

    except Exception as e:
        logger.error(str(e))
        return JSONResponse(status_code=500, content={"error": f"DB Error: {str(e)}"})
    if not  expenses :
         return JSONResponse(status_code=404, content={"message": "No expenses found"})
    return expenses

# ---------------------------------------
# 2️⃣ INSERT/UPDATE EXPENSES FOR A DATE
# ---------------------------------------

@app.post("/expenses/{expense_date}")
async def add_or_update_expenses(expense_date:date, expenses:List[Expense]):
        for expense in expenses:
              await db_helper.insert_expense(    
                  str(expense_date), expense.amount, expense.category, expense.notes)
              
        return f"Records added successfully for expense_date :{expense_date}"
 
@app.delete("/delete/{expense_date}")
async def delete_expenses_for_expense_date(expense_date:date):
        await db_helper.delete_expenses_for_date(str(expense_date))
        return f"Records deleted successfully for expense date :{expense_date}"
    
