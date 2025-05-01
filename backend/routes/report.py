from fastapi import APIRouter, HTTPException
from utils.azure.kusto import add_data, run_query, add_user_entries_to_adx

router = APIRouter()

@router.post("/adx/{index}")
async def run_adx(index: int):
    try:
        # add_data()
        query_result = run_query(index)  # Store the query result
        # add_user_entries_to_adx()
        return {
            "response": "Success",
            "query_result": query_result  # Include the actual result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ADX operation failed: {str(e)}"
        )