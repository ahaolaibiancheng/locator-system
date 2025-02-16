# multimodal_encoder.py
import torch
from transformers import BertModel, BertTokenizer

class MultimodalEncoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.text_encoder = BertModel.from_pretrained('bert-base-uncased')
        self.code_encoder = BertModel.from_pretrained('microsoft/codebert-base')
        self.projection = torch.nn.Linear(768, 256)

    def forward(self, text_input, code_input):
        # 文本编码
        text_features = self.text_encoder(**text_input).last_hidden_state[:,0,:]
        # 代码编码
        code_features = self.code_encoder(**code_input).last_hidden_state[:,0,:]
        # 联合投影
        return self.projection(text_features + code_features)

# 定位推理Agent
class LocatorAgent:
    def __init__(self):
        self.encoder = MultimodalEncoder.load_from_checkpoint('encoder.ckpt')
        self.llm = pipeline('text-generation', model='gpt-3.5-turbo')

    def analyze(self, context):
        # 多模态编码
        embeddings = self.encoder(context['log'], context['code'])
        
        # 生成推理链
        prompt = f"""
        根据以下信息诊断故障：
        日志：{context['log']}
        代码片段：{context['code']}
        请生成执行步骤：
        """
        steps = self.llm(prompt, max_length=500)
        return self._parse_steps(steps)

    def _parse_steps(self, text):
        # 解析LLM输出为结构化指令（简化版）
        return {
            "actions": ["ssh登录设备", "执行show interface命令"],
            "expected_output": "端口状态=DOWN"
        }