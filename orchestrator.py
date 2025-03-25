class OrchestratorAgent:
    def __init__(self, intent_agent, specialized_agents, followup_agent, analytics_agent):
        self.intent_agent = intent_agent
        self.specialized_agents = specialized_agents
        self.followup_agent = followup_agent
        self.analytics_agent = analytics_agent