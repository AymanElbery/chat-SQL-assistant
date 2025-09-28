from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, Literal
import asyncio
from services.llm.translation_service import TranslationService
from services.llm.text_2_sql_service import Text2SQLService
from services.database_service import DatabaseService
from services.result_processor import ResultProcessor

app = FastAPI(title="AI Reports Assistant", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
translation_service = TranslationService()
text_2_sql_service = Text2SQLService()
db_service = DatabaseService()
result_processor = ResultProcessor()

class QueryRequest(BaseModel):
    query: str
    language: Literal["ar", "en"]

class QueryResponse(BaseModel):
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # Step 0: Translate query if needed using local LLM
        if request.language == "ar":
            english_query = await translation_service.generate_english_query(
                request.query, 
                request.language
            )
        else:
            english_query = request.query

        #raise HTTPException(status_code=500, detail=str(english_query))

        # Step 1: Convert natural language to SQL
        sql_query = await text_2_sql_service.generate_sql(
            english_query, 
            request.language
        )
        
        #raise HTTPException(status_code=500, detail=str(sql_query))
        # Step 2: Execute SQL query
        raw_results = await db_service.execute_query(sql_query)
        
        # Step 3: Process results (determine if table, chart, or text)
        processed_result = await result_processor.process_results(
            raw_results, 
            request.query, 
            request.language
        )
        
        return QueryResponse(
            message=processed_result.get("message"),
            result=processed_result.get("result")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-09-26T17:26:28Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)