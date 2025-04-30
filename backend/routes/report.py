from fastapi import APIRouter, HTTPException
from utils.azure.kusto import add_data, run_query

router = APIRouter()

@router.post("/adx/")
async def run_adx():
    try:
        # add_data()
        query_result = run_query()  # Store the query result
    
        return {
            "response": "Success",
            "query_result": query_result  # Include the actual result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ADX operation failed: {str(e)}"
        )