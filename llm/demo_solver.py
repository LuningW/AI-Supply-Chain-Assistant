#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例优化求解器实现
"""

import json
import argparse
import sys
from typing import Dict, Any, List, Tuple
import numpy as np

class SupplyChainSolver:
    def __init__(self):
        """初始化供应链优化求解器"""
        # 默认参数设置
        self.init_network_problem()
    
    def init_network_problem(self):
        """初始化网络规划问题的参数"""
        # 初始化基础参数
        self.plants = ["p1", "p2"]
        self.warehouses = ["w1", "w2"]
        self.markets = ["c1", "c2", "c3", "c4"]
        
        # 产能
        self.plant_capacity = {"p1": float('inf'), "p2": 60000}  # p1容量无限，p2为60,000
        
        # 需求
        self.demand = {
            "c1": 50000,
            "c2": 100000,
            "c3": 50000,
            "c4": 20000
        }
        
        # 从工厂到仓库的运输成本
        self.plant_to_warehouse_cost = {
            ("p1", "w1"): 0,
            ("p1", "w2"): 5,
            ("p2", "w1"): 4,
            ("p2", "w2"): 2
        }
        
        # 从仓库到市场的运输成本
        self.warehouse_to_market_cost = {
            ("w1", "c1"): 3,
            ("w1", "c2"): 4,
            ("w1", "c3"): 5,
            ("w1", "c4"): 4,
            ("w2", "c1"): 2,
            ("w2", "c2"): 1,
            ("w2", "c3"): 2,
            ("w2", "c4"): float('inf')  # c4只能从w1供应，设为无穷大成本
        }
        
        # 优化结果
        self.optimal_flow = {
            # 工厂到仓库
            ("p1", "w1"): 140000,
            ("p1", "w2"): 0,
            ("p2", "w1"): 0,
            ("p2", "w2"): 60000,
            # 仓库到市场
            ("w1", "c1"): 50000,
            ("w1", "c2"): 70000,
            ("w1", "c3"): 0,
            ("w1", "c4"): 20000,
            ("w2", "c1"): 0,
            ("w2", "c2"): 30000,
            ("w2", "c3"): 50000,
            ("w2", "c4"): 0
        }
        
        # 计算当前总成本
        self.current_total_cost = self.calculate_total_cost(self.optimal_flow)
    
    def init_casting_problem(self):
        """初始化铸造问题的参数"""
        # 基础成本参数
        self.casting_cost = 700  # 每个铸件的生产成本
        self.machining_cost = 500  # 每个合格铸件的加工成本
        self.recycle_value = 300  # 每个未售出铸件的回收价值
        
        # 销售参数
        self.base_order = 20  # 基础订单数量
        self.base_price = 2000  # 基础订单单价
        self.additional_price = 1500  # 额外铸件单价
        self.max_additional = 2  # 最多额外购买数量
        
        # 概率分布 (简化为列表)
        self.yield_probabilities = {
            # 简化的良品率列表，索引是计划生产数量，值是良品率概率分布
            # 示例：当计划生产31个时的良品数量概率分布
            31: {
                12: 0.001, 13: 0.002, 14: 0.004, 15: 0.006, 16: 0.012,
                17: 0.018, 18: 0.03, 19: 0.044, 20: 0.07, 21: 0.09,
                22: 0.11, 23: 0.115, 24: 0.11, 25: 0.09, 26: 0.07,
                27: 0.045, 28: 0.03, 29: 0.02, 30: 0.01, 31: 0.003
            }
        }
        
        # 最优解
        self.optimal_quantity = 31  # 最优生产数量
        self.expected_profit = 30200.0  # 预期利润
    
    def init_qr_policy_problem(self):
        """初始化QR策略问题的参数"""
        # 基础参数
        self.monthly_demand_mean = 360  # 月需求均值
        self.monthly_demand_std = 45    # 月需求标准差
        self.service_level = 0.95       # 服务水平
        self.service_level_z = 1.65     # 对应的z值
        self.lead_time = 0.5            # 前置时间(月)
        self.order_cost = 900           # 每次订货固定成本
        self.annual_holding_cost = 240  # 每张桌子每年的持有成本
        
        # 计算最优订货量
        self.optimal_order_quantity = self.calculate_optimal_order_quantity()
        
        # 计算安全库存
        self.safety_stock = self.calculate_safety_stock()
        
        # 计算再订货点
        self.reorder_level = self.calculate_reorder_level()
    
    def calculate_optimal_order_quantity(self):
        """计算经济订货量"""
        # 转换为月度持有成本
        monthly_holding_cost = self.annual_holding_cost / 12
        
        # 经济订货量公式: sqrt(2*D*K/h)
        eoq = np.sqrt(2 * self.monthly_demand_mean * self.order_cost / monthly_holding_cost)
        return eoq
    
    def calculate_safety_stock(self):
        """计算安全库存"""
        safety_stock = self.service_level_z * self.monthly_demand_std * np.sqrt(self.lead_time)
        return safety_stock
    
    def calculate_reorder_level(self):
        """计算再订货点"""
        reorder_level = self.monthly_demand_mean * self.lead_time + self.safety_stock
        return reorder_level
    
    def calculate_total_cost(self, flow: Dict[Tuple[str, str], float]) -> float:
        """
        计算给定流量下的总成本
        
        Args:
            flow: 包含各边流量的字典
            
        Returns:
            总成本
        """
        total_cost = 0.0
        
        # 计算工厂到仓库的成本
        for (p, w), quantity in flow.items():
            if p in self.plants and w in self.warehouses:
                total_cost += quantity * self.plant_to_warehouse_cost.get((p, w), 0)
        
        # 计算仓库到市场的成本
        for (w, c), quantity in flow.items():
            if w in self.warehouses and c in self.markets:
                total_cost += quantity * self.warehouse_to_market_cost.get((w, c), 0)
        
        return total_cost
    
    def process_whatif_demand_increase(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理需求增加的假设情况
        
        Args:
            params: 包含需求增加信息的参数
            
        Returns:
            处理结果
        """
        result = {}
        
        # 从参数中提取市场和增长率
        market = params.get("entity", "")
        increase_percentage = params.get("new_value", 0)
        
        if not market or market not in self.markets:
            return {"error": f"Invalid market: {market}"}
        
        # 计算新需求
        original_demand = self.demand[market]
        new_demand = original_demand * (1 + increase_percentage / 100)
        
        # 为简化起见，我们只返回相关信息
        # 在实际实现中，您可能需要重新求解优化模型
        result["market"] = market
        result["original_demand"] = original_demand
        result["new_demand"] = new_demand
        result["increase_percentage"] = increase_percentage
        result["message"] = f"Demand for market {market} increased from {original_demand} to {new_demand} units."
        
        # 假设的新成本（实际应该重新计算）
        original_cost = self.current_total_cost
        estimated_new_cost = original_cost * (1 + (increase_percentage / 100) * (original_demand / sum(self.demand.values())))
        
        result["original_cost"] = original_cost
        result["estimated_new_cost"] = estimated_new_cost
        result["cost_difference"] = estimated_new_cost - original_cost
        result["cost_difference_percentage"] = (estimated_new_cost - original_cost) / original_cost * 100
        
        return result
    
    def process_constraint_warehouse_market(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理仓库只为特定市场服务的约束
        
        Args:
            params: 包含约束信息的参数
            
        Returns:
            处理结果
        """
        result = {}
        
        # 从参数中提取仓库和市场
        warehouse = params.get("entity1", "")
        market = params.get("entity2", "")
        
        if not warehouse or warehouse not in self.warehouses:
            return {"error": f"Invalid warehouse: {warehouse}"}
        
        if not market or market not in self.markets:
            return {"error": f"Invalid market: {market}"}
        
        # 检查是否可行
        if market == "c4" and warehouse == "w2":
            result["feasible"] = False
            result["reason"] = "Market c4 can only be served from warehouse w1."
            return result
        
        # 为简化起见，我们只返回相关信息
        # 在实际实现中，您可能需要重新求解优化模型
        result["warehouse"] = warehouse
        result["market"] = market
        result["feasible"] = True
        
        # 计算当前从该仓库到该市场的流量
        current_flow = self.optimal_flow.get((warehouse, market), 0)
        market_demand = self.demand[market]
        
        result["current_flow"] = current_flow
        result["market_demand"] = market_demand
        
        if current_flow < market_demand:
            result["additional_required"] = market_demand - current_flow
            result["message"] = f"Warehouse {warehouse} currently supplies {current_flow} units to market {market}, but would need to supply {market_demand} units to exclusively serve this market."
        else:
            result["message"] = f"Warehouse {warehouse} already supplies enough units ({current_flow}) to exclusively serve market {market} with demand {market_demand}."
        
        return result
    
    def process_optimization_query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理优化查询
        
        Args:
            params: 包含优化查询信息的参数
            
        Returns:
            处理结果
        """
        # 如果是QR策略相关的优化查询
        if params.get("type") == "qr_policy":
            self.init_qr_policy_problem()
            
            parameter = params.get("parameter", "")
            new_value = params.get("new_value", None)
            
            result = {}
            
            if parameter == "monthly_demand_mean":
                # 更新月需求均值并重新计算
                if new_value is not None:
                    self.monthly_demand_mean = new_value
                    self.optimal_order_quantity = self.calculate_optimal_order_quantity()
                    result["original_optimal_order_quantity"] = self.optimal_order_quantity
                    result["parameter"] = "月需求均值"
                    result["original_value"] = 360
                    result["new_value"] = new_value
                    result["new_optimal_order_quantity"] = self.optimal_order_quantity
            
            elif parameter == "lead_time":
                # 更新前置时间并重新计算
                if new_value is not None:
                    self.lead_time = new_value
                    self.reorder_level = self.calculate_reorder_level()
                    result["original_reorder_level"] = self.reorder_level
                    result["parameter"] = "前置时间"
                    result["original_value"] = 0.5
                    result["new_value"] = new_value
                    result["new_reorder_level"] = self.reorder_level
            
            return result
        
        # 如果是铸造问题的优化查询
        elif params.get("type") == "casting":
            self.init_casting_problem()
            
            parameter = params.get("parameter", "")
            new_value = params.get("new_value", None)
            
            result = {}
            
            if parameter == "recycle_value":
                # 更新回收价值
                if new_value is not None:
                    original_value = self.recycle_value
                    self.recycle_value = new_value
                    # 简化处理，实际应重新计算最优解
                    result["parameter"] = "回收价值"
                    result["original_value"] = original_value
                    result["new_value"] = new_value
                    result["impact"] = "降低回收价值会减少未售出铸件的收益，可能影响最优生产数量。"
            
            return result
        
        # 默认返回空结果
        return {}
    
    def solve(self, question_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据问题类型和参数解决问题
        
        Args:
            question_type: 问题类型
            params: 问题参数
            
        Returns:
            解决结果
        """
        if question_type == "whatif":
            parameter = params.get("parameter", "")
            
            if parameter == "demand" and "increase" in params.get("action", ""):
                return self.process_whatif_demand_increase(params)
            
        elif question_type == "constraint":
            constraint_type = params.get("constraint_type", "")
            
            if constraint_type == "warehouse_market_exclusive":
                return self.process_constraint_warehouse_market(params)
        
        elif question_type == "optimization":
            return self.process_optimization_query(params)
        
        elif question_type == "computation":
            # 处理计算类型的问题
            return self.process_optimization_query(params)
        
        elif question_type == "explanation":
            # 针对解释类型的问题，可能需要提供当前解决方案的详细信息
            return {
                "optimal_flow": self.optimal_flow,
                "total_cost": self.current_total_cost,
                "message": "Here is the detailed information about the current optimal solution."
            }
        
        # 如果无法识别问题类型或参数，返回错误信息
        return {"error": f"Unable to process question type: {question_type} with params: {params}"}


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Supply Chain Optimization Solver')
    parser.add_argument('--type', type=str, required=True, 
                        choices=['computation', 'explanation', 'whatif', 'constraint', 'optimization'],
                        help='Type of question')
    parser.add_argument('--params', type=str, required=True, 
                        help='Path to JSON file containing parameters')
    
    args = parser.parse_args()
    
    # 读取参数
    try:
        with open(args.params, 'r', encoding='utf-8') as f:
            params = json.load(f)
    except Exception as e:
        print(f"Error reading parameters file: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    # 初始化求解器
    solver = SupplyChainSolver()
    
    # 解决问题
    result = solver.solve(args.type, params)
    
    # 输出结果
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
