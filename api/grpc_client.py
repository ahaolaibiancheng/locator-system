# main.py 添加路径处理（首行添加）
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))
import grpc
from proto import rule_engine_pb2, rule_engine_pb2_grpc
from proto.rule_engine_pb2 import RuleRequest, RuleResponse
# from proto.rule_engine_pb2_grpc import RuleEngineStub

class RuleEngineClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = rule_engine_pb2_grpc.RuleEngineServiceStub(self.channel)
    
    def match(self, request):
        req = rule_engine_pb2.RuleRequest(
            log=request.get("log", ""),
            command=request.get("command", ""),
            code=request.get("code", "")
        )
        return self.stub.MatchRules(req)