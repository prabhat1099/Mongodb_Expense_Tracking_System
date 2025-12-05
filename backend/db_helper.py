from fastapi import FastAPI,HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import pandas as pd 
from logging_setup import setup_logger

import asyncio
load_dotenv()

logger = setup_logger("db_helper")

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
my_db = client["expense_manager"]
my_coll = my_db["expenses"]

# fetch records for expense date:
async def fetch_expenses_for_date(expense_date: str):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    expenses = await my_coll.find({"expense_date": expense_date},{"_id": 0} ).to_list(None)
    if not expenses :
          return []

    return expenses
 
# Insert record for expense date:
async def insert_expense(expense_date, amount, category, notes):
       logger.info(f"insert_expense called with date: {expense_date}, amount: {amount},category: {category}, notes: {notes}")
       docs = {
            "expense_date": expense_date, 
            "amount":amount, 
            "category":category, 
            "notes":notes  }
       result = await my_coll.insert_one(docs)
       return f"Records inserted successfully with id :{str(result.inserted_id)}"

# Delete record for expense date:
async  def delete_expenses_for_date(expense_date):
        logger.info(f"delete_expenses_for_date called with {expense_date}")
        existing = await my_coll.find_one({"expense_date": expense_date}, {"_id": 0})

        if not existing:
           return {"message": f"No records found for expense_date: {expense_date}"}
        result = await my_coll.delete_many({"expense_date":expense_date})
    
        return f"Total deteted records : {result.deleted_count}"

# Delete based on expense_date, category, and amount

async def delete_expenses_for_date_category_amount(expense_date: str, category: str, amount: float):

    logger.info(f"delete_expenses_for_date called with date={expense_date},category={category}, amount={amount}")

    # Build the query
    query = {"expense_date": expense_date,"category": category, "amount": amount}

    #  Check if any matching document exists
    existing = await my_coll.find_one(query, {"_id": 0})

    if not existing:
        return {"message": (f"No records found for expense_date={expense_date},category={category}, amount={amount}")}
     
    #  Delete all matching docs
    result = await my_coll.delete_many(query)

    return { "message": f"Total deleted records: {result.deleted_count}" }
       
   

     
# expense summary for analytics:     
async def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")

    pipeline = [
        {"$match": {
            "expense_date": {"$gte": start_date, "$lte": end_date}  }},
      
        {"$group": {
            "_id": "$category",
            "total": {"$sum": "$amount"}  }},
      
        {"$project": {
            "category": "$_id",
            "total": 1,
            "_id": 0}}      ]

    summary = await my_coll.aggregate(pipeline).to_list(None)
    return summary


if __name__ == "__main__":
    #result = asyncio.run(delete_expenses_for_date("2025-12-02"))
    #result = asyncio.run(insert_expense("2025-12-02", 2000, "Shopping", "Buy Blazer"))
    #result  = asyncio.run(fetch_expenses_for_date("2025-12-02"))
    result  = asyncio.run(fetch_expense_summary("2025-12-02","2025-12-05"))
    
    print(result)