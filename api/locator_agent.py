# api/locator_agent.py
import logging
logger = logging.getLogger(__name__)

class LocatorAgent:
    def __init__(self):
        logger.info("初始化定位智能体...")
        self.rule_engine = RuleEngineClient()
    
    async def analyze_fault(self, fault_data: dict):
        """故障分析入口方法"""
        try:
            response = self.rule_engine.execute_rule(
                fault_type=fault_data["type"],
                port=fault_data["port"]
            )
            return {"conclusion": response.conclusion}
        except Exception as e:
            return {"error": str(e)}
