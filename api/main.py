# main.py 添加路径处理（首行添加）
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))
# main.py
from fastapi import FastAPI
from locator_agent import LocatorAgent
from grpc_client import RuleEngineClient  # 导入客户端类
import subprocess

app = FastAPI()

# 初始化组件
rule_engine = RuleEngineClient()  # 假设已封装Java规则引擎的gRPC客户端
locator_agent = LocatorAgent()

# 命令执行白名单
ALLOWED_COMMANDS = {'show interface', 'ping', 'traceroute'}

@app.post("/diagnose")
async def diagnose(request: dict):
    # Step 1: 规则引擎匹配
    rule_result = rule_engine.execute_rule(request)
    if rule_result['matched']:
        return {"conclusion": rule_result['conclusion']}

    # Step 2: 多模态Agent推理
    agent_plan = locator_agent.analyze(request)
    
    # Step 3: 执行Agent
    execution_log = []
    for action in agent_plan['actions']:
        if not _validate_action(action):
            return {"error": "非法操作指令"}
        
        result = execute_command(action['command'])
        execution_log.append(result)

    # Step 4: 生成结论并反馈
    conclusion = _generate_conclusion(execution_log)
    _update_rules(request, conclusion)  # 触发规则自动生成
    return {"conclusion": conclusion}

# main.py中修正路由
@app.post("/analyze")
async def analyze_fault(fault_data: dict):
    return await locator_agent.analyze_fault(fault_data)

def _validate_action(action):
    """校验命令是否在白名单内"""
    cmd = action.get('command', '').split()[0]
    return cmd in ALLOWED_COMMANDS

def execute_command(cmd):
    """在沙箱中执行命令"""
    try:
        result = subprocess.run(
            cmd, shell=True, 
            timeout=10, 
            capture_output=True
        )
        return {
            'output': result.stdout.decode(),
            'error': result.stderr.decode()
        }
    except Exception as e:
        return {'error': str(e)}

# 规则自动生成（简化示例）
def _update_rules(context, conclusion):
    new_rule = f"""
    rule \"AutoGen_{conclusion[:10]}\"
        when
            $log : LogMessage({context['log_keywords']})
            $cmd : CommandOutput({context['cmd_pattern']})
        then
            $ctx.setConclusion("{conclusion}");
    end
    """
    rule_engine.add_rule(new_rule)