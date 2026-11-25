
class AgentManager:

    def __init__(self):
        self.agents = {}

    def add_agent(self, agent_id, information):
        self.agents[agent_id] = information
        print(f"Agent {agent_id} enregistré.")

    def list_agents(self):
        return self.agents.copy()

    def remove_agent(self, agent_id):
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"Agent {agent_id} supprimé.")
        else:
            print(f"Agent {agent_id} introuvable.")
