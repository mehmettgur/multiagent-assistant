# Multi Agent Personal Assistant

## Project Overview

`multiagent-assistant` is a multi-agent personal assistant prototype designed to run in a local Jupyter notebook or Python environment. Using AutoGen AgentChat’s `SelectorGroupChat` framework, it:

- Breaks down complex natural-language user requests into discrete steps
- Delegates tasks like web research, summarization, email drafting, sentiment analysis, and meeting planning to specialized agents
- Ensures each agent invokes only the tools it needs (e.g., web search, saving drafts, adding to‑dos, scheduling, logging)

This README explains how to clone, configure, and run the project, as well as export the agent configuration to JSON for AutoGen Studio.

> ⚠ **Note:** The AutoGen framework is under active development; APIs and agent behavior may change in future releases. Check the official AutoGen repository for the latest updates.

---

## Features

- **Modular Agent Architecture**: Each task is encapsulated in its own `AssistantAgent`, making it easy to add or remove agents.
- **Tool Integration**: Built-in functions for web search (`perform_web_search`), email draft saving (`save_email_draft`), to‑do list management (`add_todo_item`), calendar scheduling (`add_scheduled_event`), and event logging (`log_event`).
- **Smart Planning**: The `Intent_Task_Router` converts a cleaned user query into a step-by-step execution plan.
- **Flexible Termination**: Conversations end on the "TERMINATE" keyword or after a configurable maximum message count.
- **Interactive Input**: The `UserProxyAgent` can prompt the user for clarification when needed.

---

## Agents and Responsibilities

- **Orchestrator**: Receives the execution plan, delegates tasks to agents, and coordinates tool calls.
- **UserProxyAgent**:  Handles interactive prompts to gather missing information from the user.
- **Input\_Preprocessor**: Cleans and normalizes the raw user query, correcting grammar and extracting key entities.
- **Intent\_Task\_Router**: Analyzes the preprocessed query and generates a sequential plan listing which agent performs each step.
- **Web\_Search\_Agent**: Executes DuckDuckGo searches and returns raw results.
- **Summarization\_Agent**: Condenses provided text (e.g., into a bullet-point summary).
- **Scheduling\_Calendar\_Agent**: Simulates creating calendar events based on time preferences and attendees.
- **Email\_Composition\_Sentiment\_Agent**:
  - *Mode 1*: Drafts the email body.
  - *Mode 2*: Calls the tool to save the draft.
  - *Mode 3*: Performs sentiment analysis on the draft text.
- **To\_Do\_List\_Agent**: Adds tasks to a to‑do list file.
- **Clarification\_Agent**: Asks concise follow-up questions when required data is missing.
- **Analytics\_Logging\_Agent**: Logs events and tool results to a log file.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mehmettgur/multiagent-assistant.git
cd multiagent-assistant
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Your OpenAI API Key Configure Your OpenAI API Key

The project supports two methods for providing your API key:

#### Via JSON config file (`your_api_key.json`)

```json
[
  {
    "model": "gpt-4",
    "api_key": "YOUR_OPENAI_API_KEY"
  }
]
```

Replace `YOUR_OPENAI_API_KEY` with your actual key from OpenAI.

---

## Exporting to AutoGen Studio (JSON)

To load your agent configuration into AutoGen Studio, serialize the team to JSON:

```python
# After creating `team = SelectorGroupChat(...)` in your script:
team_component = team.dump_component()

# Pydantic v2+ method:
team_dict = team_component.model_dump(mode="json")
# Or for older versions:
# team_dict = team_component.dict()

import json
with open("orchestrated_team_config.json", "w", encoding="utf-8") as f:
    json.dump(team_dict, f, indent=2, ensure_ascii=False)
```

You can then import `orchestrated_team_config.json` into AutoGen Studio for visualization and further editing.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

