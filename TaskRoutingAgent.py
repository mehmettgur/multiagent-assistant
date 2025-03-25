from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import json
import re  # Eksik olan import eklendi

# 1. AutoGen Config (Docker'sız çalışacak şekilde)
config_list = config_list_from_json(env_or_file="C:\\Users\\memo_\\Desktop\\Projeler\\MultiAssistant\\OAI_CONFIG_LIST.json")

# 2. Task Routing Agent (Güncellenmiş)
class TaskRoutingAgent(AssistantAgent):
    def __init__(self, name):
        super().__init__(
            name=name,
            system_message="""
            Sen bir **Task Routing Agent**sın. Görevler:
            1. Kullanıcı mesajını analiz et.
            2. YALNIZCA ŞU FORMATTA CEVAP VER:
               {
                 "task": "schedule|email|web_search|summarize|todo|recommend|clarify",
                 "params": {"key": "value"}
               }
            
            Kurallar:
            - TÜM ÇIKTILAR GEÇERLİ JSON OLMALI!
            - "task" değeri YUKARIDAKİ LİSTEDEN SEÇİLMELİ
            - "params" her zaman bulunmalı (boş olabilir: {})
            """,
            llm_config={
                "config_list": config_list,
                "temperature": 0
            }
        )

    def route_task(self, message: str) -> dict:
        try:
            response = self.generate_reply(messages=[{"content": message, "role": "user"}])
            print(f"Ham Yanıt: {response}")
            
            # JSON temizleme işlemi
            cleaned = re.sub(r'[\x00-\x1F]+', '', response).strip()
            if not cleaned.endswith("}"):
                cleaned += "}"
                
            return json.loads(cleaned)
        except Exception as e:
            print(f"Hata: {str(e)}")
            return {"task": "error", "reason": str(e)}

# Test Senaryosu
if __name__ == "__main__":
    input_preprocessor = UserProxyAgent(
        name="input_preprocessor",
        human_input_mode="NEVER",
        code_execution_config={"use_docker": False}
    )
    
    task_router = TaskRoutingAgent(name="task_router")
    
    # Test 1: Geçerli istek
    result = task_router.route_task("Yarın 14:00'da doktor randevusu oluştur")
    print(f"Sonuç 1: {result}")

    # Test 2: Eksik parametre
    result = task_router.route_task("Toplantı ekle")
    print(f"Sonuç 2: {result}")