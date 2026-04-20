class Router:
    def route(self, task_type: str) -> str:
        mapping = {
            "formatting": "skill",
            "extraction": "skill",
            "literature": "subagent",
            "data": "subagent",
            "measurement": "subagent",
            "analysis": "subagent",
            "audit": "subagent",
            "design_review": "team",
            "measurement_review": "team",
            "framing_review": "team",
        }
        return mapping.get(task_type, "subagent")
