import json
import os
import requests
from typing import Dict, List, Optional, Any, Tuple
solver_script_path = os.path.join(os.path.dirname(__file__), "demo_solver.py")


class SupplyChainOptimizationFramework:
    def __init__(
        self, 
        llm_api_key: str, 
        llm_endpoint: str,
        dispatch_prompt_path: str,
        supply_chain_prompts_path: str,
        max_history: int = 3
    ):
        """
        初始化供应链优化框架
        
        Args:
            llm_api_key: LLM API的密钥
            llm_endpoint: LLM API的端点
            dispatch_prompt_path: 分发提示的JSON文件路径
            supply_chain_prompts_path: 供应链提示的JSON文件路径
            max_history: 保存的最大历史对话轮数
        """
        self.llm_api_key = llm_api_key
        self.llm_endpoint = llm_endpoint
        self.dispatch_prompt_path = dispatch_prompt_path
        self.supply_chain_prompts_path = supply_chain_prompts_path
        self.max_history = max_history
        self.conversation_history = []
        
        # 加载提示模板
        with open(dispatch_prompt_path, 'r', encoding='utf-8') as f:
            self.dispatch_prompt = json.load(f)
        
        with open(supply_chain_prompts_path, 'r', encoding='utf-8') as f:
            self.supply_chain_prompts = json.load(f)
    
    def add_to_history(self, user_question: str, bot_response: str) -> None:
        """添加一轮对话到历史记录中"""
        self.conversation_history.append({"user": user_question, "bot": bot_response})
        # 保持历史记录不超过最大长度
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def format_history(self) -> str:
        """格式化历史对话记录"""
        formatted_history = ""
        for interaction in self.conversation_history:
            formatted_history += f"User: {interaction['user']}\nAssistant: {interaction['bot']}\n\n"
        return formatted_history.strip()
    
    def call_llm_api(self, prompt: str) -> str:
        """
        调用LLM API
        
        Args:
            prompt: 发送给LLM的提示
            
        Returns:
            LLM的响应
        """
        # 这里应该实现具体的API调用逻辑
        # 这是一个示例实现，需要根据您使用的实际API进行调整
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4", # 或其他适合的模型
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        response = requests.post(self.llm_endpoint, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API调用失败: {response.status_code}, {response.text}")
    
    def dispatch_question(self, question: str) -> str:
        """
        将问题分发到相应的处理类型
        
        Args:
            question: 用户的问题
            
        Returns:
            问题类型: computation, explanation, whatif, constraint 或 optimization
        """
        # 准备分发提示
        prompt_template = self.dispatch_prompt["dispatch_prompt"]
        
        # 替换变量
        previous_interactions = self.format_history()
        prompt = prompt_template["role"] + "\n\n" + prompt_template["task_instruction"] + "\n\n"
        
        # 添加指令
        prompt += prompt_template["instructions"] + "\n\n"
        
        # 添加示例
        prompt += "Examples:\n"
        for example in prompt_template["examples"]:
            prompt += f"User Question: {example['User Question']}\n"
            prompt += f"Dispatch Response: {example['Dispatch Response']}\n\n"
        
        # 添加历史交互和当前问题
        prompt += f"Previous interactions:\n{previous_interactions}\n\n"
        prompt += f"Current question: {question}\n"
        prompt += "Dispatch Response:"
        
        # 调用LLM API获取分发结果
        dispatch_result = self.call_llm_api(prompt).strip().lower()
        
        # 验证结果是否为有效的分类
        valid_types = ["computation", "explanation", "whatif", "constraint", "optimization"]
        if dispatch_result not in valid_types:
            raise ValueError(f"Invalid dispatch result: {dispatch_result}. Expected one of {valid_types}")
        
        return dispatch_result
    
    def process_question(self, question_type: str, question: str) -> str:
        """
        根据问题类型处理问题
        
        Args:
            question_type: 问题类型
            question: 用户问题
            
        Returns:
            处理结果
        """
        # 获取对应类型的提示模板
        if question_type not in self.supply_chain_prompts:
            raise ValueError(f"Unknown question type: {question_type}")
        
        prompt_template = self.supply_chain_prompts[question_type]
        
        # 替换变量
        previous_interactions = self.format_history()
        prompt = prompt_template["role"] + "\n\n" + prompt_template["task_instruction"] + "\n\n"
        
        # 添加指令
        prompt += prompt_template["instructions"] + "\n\n"
        
        # 添加示例(如果有)
        if prompt_template["examples"]:
            prompt += "Examples:\n"
            for example in prompt_template["examples"]:
                prompt += f"User Question: {example['User Question']}\n"
                prompt += f"Reference Answer: {example['Reference Answer']}\n\n"
        
        # 添加历史交互和当前问题
        prompt += f"Previous interactions:\n{previous_interactions}\n\n"
        prompt += f"Current question: {question}\n"
        
        # 解析问题并提取参数，用于solver
        solver_params = self.extract_solver_params(question_type, question)
        print("Solver params:", solver_params)

    
        # 调用优化solver
        solver_result = self.run_optimization_solver(question_type, solver_params)
        print("Solver result:", solver_result)

        # 将solver结果添加到提示中
        prompt += f"\nOptimization results:\n{solver_result}\n"
        prompt += "Your response:"
        
        # 调用LLM API获取最终答案
        final_response = self.call_llm_api(prompt)
        
        return final_response
    
    def extract_solver_params(self, question_type: str, question: str) -> Dict[str, Any]:
        """
        从问题中提取solver参数
        
        Args:
            question_type: 问题类型
            question: 用户问题
            
        Returns:
            solver参数字典
        """
        # 构建提取参数的prompt
        prompt = f"""
        You are a supply chain optimization parameter extractor. Given a question, extract the necessary parameters for our optimization solver.
        
        Question type: {question_type}
        User question: {question}
        
        Extract the parameters in JSON format. For example, if the question mentions changing demand from 50 to 60, output:
        {{
            "parameter": "demand",
            "entity": "market_name",
            "original_value": 50,
            "new_value": 60
        }}
        
        If there are multiple parameters, include all of them in an array.
        For 'whatif' questions, identify which variables need to be modified.
        For 'constraint' questions, identify which constraints need to be added.
        For 'optimization' questions, identify the objective and constraints.
        
        Your extracted parameters in JSON format:
        """
        
        # 调用LLM API提取参数
        params_json_str = self.call_llm_api(prompt)
        
        # 尝试解析JSON
        try:
            # 找到JSON部分
            import re
            json_match = re.search(r'({[\s\S]*})', params_json_str)
            if json_match:
                params_json_str = json_match.group(1)
            
            params = json.loads(params_json_str)
            return params
        except json.JSONDecodeError:
            # 如果解析失败，返回空字典
            print(f"Failed to parse parameters from: {params_json_str}")
            return {}
    
    def run_optimization_solver(self, question_type: str, params: Dict[str, Any]) -> str:
        """
        运行优化求解器
        
        Args:
            question_type: 问题类型
            params: 提取的参数
            
        Returns:
            优化结果
        """
        # 这里应该调用您的demo_solver.py或其他优化解决方案
        # 这是一个示例实现，需要根据实际情况进行调整
        
        # 示例：调用外部求解器脚本
        try:
            import subprocess
            import tempfile
            
            # 将参数写入临时文件
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(params, f)
                params_file = f.name
            
            # 调用求解器脚本
            result = subprocess.run(
                ["python", solver_script_path, "--type", question_type, "--params", params_file],
                capture_output=True,
                text=True,
                check=True
            )
           
            # 删除临时文件
            os.unlink(params_file)
            
            return result.stdout
        except Exception as e:
            return f"Error running optimization solver: {str(e)}"
    
    def handle_user_question(self, question: str) -> str:
        """
        处理用户问题的主函数
        
        Args:
            question: 用户问题
            
        Returns:
            回答
        """
        try:
            # 1. 分发问题
            question_type = self.dispatch_question(question)
            
            # 2. 处理问题
            response = self.process_question(question_type, question)
            
            # 3. 更新历史记录
            self.add_to_history(question, response)
            
            return response
        except Exception as e:
            error_message = f"Error processing your question: {str(e)}"
            print(error_message)
            return error_message


# 示例代码，说明如何使用此框架
if __name__ == "__main__":
    # 初始化框架
    framework = SupplyChainOptimizationFramework(
        llm_api_key="",
        llm_endpoint="https://api.openai.com/v1/chat/completions",
        dispatch_prompt_path="llm/dispatch_prompt_updated.json",
        supply_chain_prompts_path="llm/supply_chain_prompts_english.json"
    )
    
    # 处理用户问题
    question = "What would happen if the demand at market c1 increased by 10%?"
    response = framework.handle_user_question(question)
    print(f"Response: {response}")
