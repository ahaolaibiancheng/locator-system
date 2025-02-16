# main.py 添加路径处理（首行添加）
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))
import grpc
from proto import rule_engine_pb2, rule_engine_pb2_grpc
from proto.rule_engine_pb2 import RuleRequest, RuleResponse

import logging
logger = logging.getLogger(__name__)

class RuleEngineClient:
    def __init__(self, host='localhost', port=50051):
        logger.info(f"连接规则引擎服务: {host}:{port}")
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = rule_engine_pb2_grpc.RuleEngineServiceStub(self.channel)
    
    def execute_rule(self, raw_log: str, command: str, error_code: str = "") -> dict:
        request = rule_engine_pb2.RuleRequest(
            raw_log=raw_log,
            command=command,
            error_code=error_code
        )
        response = self.stub.ExecuteRule(request)
        return {
            "conclusion": response.conclusion,
            "action": response.action
        }