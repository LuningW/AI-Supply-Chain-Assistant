#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
供应链优化LLM辅助框架使用示例
"""

import json
import os
from supply_chain_framework import SupplyChainOptimizationFramework

def main():
    """
    展示如何使用供应链优化框架的主函数
    """
    # 加载配置（实际应用中应从配置文件或环境变量中获取）
    llm_api_key = os.environ.get("LLM_API_KEY", "") # ""里填写api
    llm_endpoint = os.environ.get("LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions")
    dispatch_prompt_path = "dispatch_prompt_updated.json"
    supply_chain_prompts_path = "supply_chain_prompts_english.json"
    
    # 初始化框架
    framework = SupplyChainOptimizationFramework(
        llm_api_key=llm_api_key,
        llm_endpoint=llm_endpoint,
        dispatch_prompt_path=dispatch_prompt_path,
        supply_chain_prompts_path=supply_chain_prompts_path
    )
    
    # 处理一系列用户问题进行演示
    questions = [
        "What would happen if the demand at market c1 increased by 10%?",
        "Why does plant p1 produce more products for market c2 than for market c1?",
        "Can I use warehouse w1 only for market c3?",
        "What if plant p2 can now supply only half of its original capacity?",
        "What's the optimal order quantity when demand is 330 tables per month?"
    ]
    
    # 处理每个问题并打印结果
    for i, question in enumerate(questions):
        print(f"\n--- Question {i+1}: {question} ---")
        response = framework.handle_user_question(question)
        print(f"--- Response {i+1}: ---\n{response}\n")
        print("-" * 80)

if __name__ == "__main__":
    main()