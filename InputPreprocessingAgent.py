from autogen import UserProxyAgent, AssistantAgent, config_list_from_json
from textblob import TextBlob
import re

# 1. AutoGen Config Setup
config_list = config_list_from_json(env_or_file="C:\\Users\\memo_\\Desktop\\Projeler\\MultiAssistant\\OAI_CONFIG_LIST.json")

# 2. Preprocessing Function
def preprocess_input(message: str) -> str:
    # Remove special characters
    cleaned = re.sub(r'[^\w\sğüşıöçĞÜŞİÖÇ]', '', message, flags=re.IGNORECASE)
    # Correct spelling (using TextBlob)
    # Basic tokenization and lowercase
    tokens = cleaned.lower().split()
    return " ".join(tokens)

# 3. Input Preprocessing Agent (AutoGen UserProxyAgent)
class InputPreprocessingAgent(UserProxyAgent):
    def __init__(self, name):
        super().__init__(
            name=name,
            human_input_mode="NEVER",
            code_execution_config=False,
            llm_config=False,
            default_auto_reply="Input processed. Routing to next agent..."
        )
    
    def initiate_chat(self, recipient, message, **kwargs):
        processed_msg = preprocess_input(message)
        super().initiate_chat(recipient, message=processed_msg, **kwargs)

# 4. Initialize Agents
input_preprocessor = InputPreprocessingAgent(name="Input_Preprocessor")
intent_agent = AssistantAgent(
    name="Intent_Agent",
    system_message="Analyze user intent and route to appropriate specialist agent.",
    llm_config={"config_list": config_list}
)

# 5. Test the Flow
input_preprocessor.initiate_chat(
    recipient=intent_agent,
    max_turns=1,
    message="Please schedule a team meeting tomorrow at 3pm!"
)

# Expected Output:
# Intent_Agent receives: "yarın saat 3te takım toplantısı ayarla lutfen"