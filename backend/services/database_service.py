import asyncpg
import asyncio
from typing import List, Dict, Any
import os
from contextlib import asynccontextmanager

class DatabaseService:
    def __init__(self):
        self.connection_pool = None
        self.db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "5432")),
            "database": os.getenv("DB_NAME", "text_to_sql_db"),
            "user": os.getenv("DB_USER", "aymanelbery"),
            "password": os.getenv("DB_PASSWORD", "361036")
        }
    
    async def initialize_pool(self):
        """Initialize connection pool"""
        if not self.connection_pool:
            self.connection_pool = await asyncpg.create_pool(**self.db_config)
    
    async def execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        await self.initialize_pool()
        
        async with self.connection_pool.acquire() as connection:
            try:
                # Security check - basic SQL injection prevention
                if self.is_safe_query(sql_query):
                    rows = await connection.fetch(sql_query)
                    
                    # Convert rows to list of dictionaries
                    results = []
                    for row in rows:
                        results.append(dict(row))
                    
                    return results
                else:
                    raise Exception("Unsafe SQL query detected")
                    
            except Exception as e:
                raise Exception(f"Database error: {str(e)}")
    
    def is_safe_query(self, query: str) -> bool:
        """Basic SQL injection prevention"""
        dangerous_keywords = [
            'DROP', 
            'DELETE', 
            'UPDATE', 
            'INSERT', 
            'ALTER', 
            #'CREATE', 
            'TRUNCATE', 
            'EXEC', 
            'EXECUTE'
        ]
        
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False
        
        return True
    
    async def get_schema_info(self) -> Dict[str, Any]:
        """Get database schema information"""
        schema_query = """
        SELECT 
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns 
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        
        return await self.execute_query(schema_query)