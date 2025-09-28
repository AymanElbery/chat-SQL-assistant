from transformers import AutoTokenizer, M2M100ForConditionalGeneration

class TranslationService:
    def __init__(self):
        self.translation_tokenizer = None
        self.translation_model = None

        self.initialize_translation_model()
    
    def initialize_translation_model(self):
        """Initialize the local translation LLM model"""
        try:
            
            self.translation_tokenizer = AutoTokenizer.from_pretrained("alirezamsh/small100")
            self.translation_model = M2M100ForConditionalGeneration.from_pretrained("alirezamsh/small100")

            print("Translation LLM Model initialized successfully")
        except Exception as e:
            print(f"Error initializing translation model: {e}")
            # Fallback to a simpler model or rule-based approach
            self.use_fallback_model()
    
    async def generate_english_query(self, natural_query: str, language: str) -> str:
        """Translate Arabic query to English using local LLM"""
        # Create prompt based on language

        try:
            self.translation_tokenizer.tgt_lang = "en"
            encoded_ar = self.translation_tokenizer(natural_query, return_tensors="pt")
            generated_tokens = self.translation_model.generate(**encoded_ar)
            response = self.translation_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            
            return response[0]
        except Exception as e:
            print(f"Error Translation to English: {e}")
            # Fallback to rule-based generation
            return self.fallback_translation_generation(natural_query, language)

    def use_fallback_model(self):
        """Fallback to a lightweight model or rule-based approach"""
        # You can implement a rule-based SQL generator here
        pass
    
    def fallback_translation_generation(self, query: str, language: str) -> str:
        """Simple rule-based SQL generation as fallback"""
        
        # Default fallback
        return "SELECT 'Please provide a more specific query' as message;"