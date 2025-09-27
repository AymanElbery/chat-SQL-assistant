from typing import Dict, Any, List
import pandas as pd

class ResultProcessor:
    async def process_results(
        self, 
        raw_results: List[Dict[str, Any]], 
        original_query: str, 
        language: str
    ) -> Dict[str, Any]:
        """Process raw SQL results and determine output format"""
        
        if not raw_results:
            message = "لم يتم العثور على نتائج" if language == "ar" else "No results found"
            return {
                "message": message,
                "result": {
                    "type": "text",
                    "data": message
                }
            }
        
        # Determine result type based on data characteristics
        result_type = self.determine_result_type(raw_results, original_query)
        #result_type = "chart"
        if result_type == "chart":
            return {
                "result": {
                    "type": "chart",
                    "data": self.prepare_chart_data(raw_results, original_query, language)
                }
            }
        elif result_type == "table":
            return {
                "result": {
                    "type": "table",
                    "data": raw_results
                }
            }
        else:
            # Single value or simple text result
            return {
                "result": {
                    "type": "text",
                    "data": self.format_text_result(raw_results, language)
                }
            }
    
    def determine_result_type(self, results: List[Dict[str, Any]], query: str) -> str:
        """Determine if results should be displayed as table, chart, or text"""
        
        if len(results) == 1 and len(results[0]) == 1:
            # Single value result
            return "text"
        
        # Check for aggregation keywords that suggest charts
        chart_keywords = [
            'count', 'sum', 'avg', 'average', 'total', 'group by',
            'عدد', 'مجموع', 'متوسط', 'إجمالي'
        ]
        
        query_lower = query.lower()
        if any(keyword in query_lower for keyword in chart_keywords):
            # Check if we have numeric data suitable for charts
            if self.has_numeric_data(results):
                return "chart"
        
        # Default to table for multiple rows/columns
        if len(results) > 1 or len(results[0]) > 1:
            return "table"
        
        return "text"
    
    def has_numeric_data(self, results: List[Dict[str, Any]]) -> bool:
        """Check if results contain numeric data suitable for charts"""
        if not results:
            return False
        
        for row in results:
            for value in row.values():
                if isinstance(value, (int, float)):
                    return True
        
        return False
    
    def prepare_chart_data(
        self, 
        results: List[Dict[str, Any]], 
        query: str, 
        language: str
    ) -> Dict[str, Any]:
        """Prepare data for Chart.js"""
        
        if not results:
            return {}
        
        # Extract labels and data
        columns = list(results[0].keys())
        
        # Assume first column is labels, rest are data
        labels = [str(row[columns[0]]) for row in results]
        
        datasets = []
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
        
        for i, col in enumerate(columns[1:]):
            data = [row[col] if isinstance(row[col], (int, float)) else 0 for row in results]
            datasets.append({
                'label': col,
                'data': data,
                'backgroundColor': colors[i % len(colors)],
                'borderColor': colors[i % len(colors)],
                'borderWidth': 1
            })
        
        chart_title = "نتائج الاستعلام" if language == "ar" else "Query Results"
        
        return {
            'type': 'bar',  # Default to bar chart
            'title': chart_title,
            'chartData': {
                'labels': labels,
                'datasets': datasets
            }
        }
    
    def format_text_result(self, results: List[Dict[str, Any]], language: str) -> str:
        """Format simple results as text"""
        if len(results) == 1 and len(results[0]) == 1:
            value = list(results[0].values())[0]
            return str(value)
        
        # Multiple values - create summary
        summary = ""
        for row in results:
            for key, value in row.items():
                summary += f"{key}: {value}\n"
        
        return summary.strip()