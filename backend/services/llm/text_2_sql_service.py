from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_cpp import Llama

class Text2SQLService:
    def __init__(self):
        self.text_2_sql_tokenizer = None
        self.text_2_sql_model = None

        self.initialize_text_2_sql_model()

    def initialize_text_2_sql_model(self):
        """Initialize the local LLM model"""
        try:
            
            self.text_2_sql_model = Llama.from_pretrained(
                repo_id="Ellbendls/Qwen-3-4b-Text_to_SQL-GGUF",
                filename="Qwen-3-4b-Text_to_SQL-F16.gguf",
            )

            print("Text_to_SQL LLM Model initialized successfully")
        except Exception as e:
            print(f"Error initializing model: {e}")
            # Fallback to a simpler model or rule-based approach
            self.use_fallback_model()

    def use_fallback_model(self):
        """Fallback to a lightweight model or rule-based approach"""
        # You can implement a rule-based SQL generator here
        pass
    
    async def generate_sql(self, natural_query: str, language: str) -> str:
        """Convert natural language to SQL query"""
        
        # Create prompt based on language
        # Database schema context (you should load this from your actual DB)
        schema_context = """
        Database Schema:
        - users (id, name, email, created_at, gender[F, M], age, country)
        - orders (id, user_id, product_id, amount, order_date)
        - products (id, name, category, price, stock)
        - sales (id, product_id, quantity, sale_date)
        """
        
        prompt = f"""
        You are an expert SQL assistant.
        You are given the database schema and a Question.
        Generate only valid SQL for PostgreSQL. Do not include explanations.
        If multiple tables are needed, use JOINs correctly.
        Never use tables or columns not in the schema.
        
        {schema_context}
        
        Query: {natural_query}
        
        SQL:"""

        try:
            
            generated_text = self.text_2_sql_model(prompt, max_tokens=256, temperature=0.2, top_p=0.9)

            # Extract SQL from the generated text
            sql_query = self.extract_sql_from_response(generated_text["choices"][0]["text"].strip(), prompt)
            
            return sql_query
            
        except Exception as e:
            print(f"Error generating SQL: {e}")
            # Fallback to rule-based generation
            return self.fallback_sql_generation(natural_query, language)

    def extract_sql_from_response(self, response: str, prompt: str) -> str:
        """Extract clean SQL query from model response"""
        # Remove the prompt from response
        sql_part = response.replace(prompt, "").strip()
        
        # Clean up the SQL
        sql_lines = sql_part.split('\n')
        sql_query = ""
        return sql_lines[sql_lines.__len__()-1].strip()
        for line in sql_lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('--'):
                sql_query += line + " "
        
        return sql_query.strip().rstrip(';') + ';'
    
    def fallback_sql_generation(self, query: str, language: str) -> str:
        """Simple rule-based SQL generation as fallback"""
        query_lower = query.lower()
        
        # Simple keyword matching for common queries
        if any(word in query_lower for word in ['users', 'المستخدمين', 'العملاء']):
            if any(word in query_lower for word in ['count', 'عدد', 'كم']):
                return "SELECT COUNT(*) as total_users FROM users;"
            else:
                return "SELECT * FROM users LIMIT 10;"
        
        elif any(word in query_lower for word in ['orders', 'الطلبات']):
            return "SELECT * FROM orders LIMIT 10;"
        
        elif any(word in query_lower for word in ['sales', 'المبيعات']):
            return "SELECT * FROM sales LIMIT 10;"
        
        # Default fallback
        return "SELECT 'Please provide a more specific query' as message;"