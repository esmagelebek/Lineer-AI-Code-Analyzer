import requests
from radon.visitors import ComplexityVisitor
import lizard
import ast

class CodeDebtAnalyst:
    @staticmethod
    def analyze_source(file_name, content):
        results = []
        try:
            visitor = ComplexityVisitor.from_code(content)
            liz = lizard.analyze_file.analyze_source_code(file_name, content)
            
            # Fonksiyonları analiz et
            for func in visitor.functions:
                liz_func = next((f for f in liz.function_list if f.name == func.name), None)
                results.append({
                    "Dosya": file_name,
                    "Tip": "Fonksiyon",
                    "İsim": func.name,
                    "Karmaşıklık": func.complexity,
                    "Satır": liz_func.length if liz_func else 0,
                    "Kod": CodeDebtAnalyst.get_function_source(content, func.name)
                })
            
            # Tüm dosyayı da bir "Bütün" olarak ekle
            results.append({
                "Dosya": file_name,
                "Tip": "Dosya Genel",
                "İsim": "TÜM DOSYA",
                "Karmaşıklık": getattr(liz, 'average_cyclomatic_complexity', 0),
                "Satır": len(content.splitlines()),
                "Kod": content
            })
        except Exception as e:
            print(f"Hata: {e}")
        return results

    @staticmethod
    def get_function_source(source_code, function_name):
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    lines = source_code.splitlines()
                    return "\n".join(lines[node.lineno - 1 : node.end_lineno])
        except: pass
        return "Kod çekilemedi."

    @staticmethod
    def get_ai_refactor_suggestion(code, api_key, mode="Fonksiyon"):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prompt'u biraz daha netleştirelim
        if mode == "Dosya Genel":
            prompt = f"Bir kıdemli yazılım geliştirici gibi davran. Aşağıdaki Python kodunu bütünsel olarak incele; mimari, isimlendirme ve temiz kod prensipleri açısından önerilerini madde madde yaz:\n\n{code}"
        else:
            prompt = f"Aşağıdaki Python fonksiyonunu refactor et, daha okunabilir ve performanslı bir versiyonunu yaz:\n\n{code}"
        
        data = {
            "model": "llama-3.3-70b-versatile", # Daha güncel ve stabil bir model ismi
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()
            
            # Hata ayıklama: Eğer 'choices' yoksa API'den gelen asıl mesajı göster
            if 'choices' in response_json:
                return response_json['choices'][0]['message']['content']
            else:
                error_msg = response_json.get('error', {}).get('message', 'Bilinmeyen API Hatası')
                return f"⚠️ Groq API Hatası: {error_msg}"
                
        except Exception as e:
            return f"❌ Bağlantı Hatası: {str(e)}"