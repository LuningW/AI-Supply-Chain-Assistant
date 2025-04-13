#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
供应链可视化辅助模块
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import Dict, Tuple, List, Any
import tempfile
import os

class SupplyChainVisualizer:
    """供应链网络可视化工具"""
    
    def __init__(self):
        """初始化可视化器"""
        self.temp_dir = tempfile.mkdtemp()
    
    def plot_network_flow(self, 
                          plants: List[str], 
                          warehouses: List[str], 
                          markets: List[str],
                          flow: Dict[Tuple[str, str], float]) -> str:
        """
        绘制网络流图
        
        Args:
            plants: 工厂列表
            warehouses: 仓库列表
            markets: 市场列表
            flow: 流量字典，键为边(u,v)，值为流量
            
        Returns:
            图表文件的路径
        """
        # 创建有向图
        G = nx.DiGraph()
        
        # 添加节点
        for p in plants:
            G.add_node(p, layer=0, type='plant')
        
        for w in warehouses:
            G.add_node(w, layer=1, type='warehouse')
            
        for m in markets:
            G.add_node(m, layer=2, type='market')
        
        # 添加边和流量标签
        for (u, v), f in flow.items():
            if f > 0:  # 只添加有流量的边
                G.add_edge(u, v, weight=f)
        
        # 节点位置设置
        pos = {}
        
        # 水平布局：工厂、仓库、市场分别在左、中、右
        plant_count = len(plants)
        warehouse_count = len(warehouses)
        market_count = len(markets)
        
        for i, p in enumerate(plants):
            pos[p] = (0, (i - plant_count / 2 + 0.5) * 2)
            
        for i, w in enumerate(warehouses):
            pos[w] = (1, (i - warehouse_count / 2 + 0.5) * 2)
            
        for i, m in enumerate(markets):
            pos[m] = (2, (i - market_count / 2 + 0.5) * 2)
        
        # 绘图
        plt.figure(figsize=(12, 8))
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, 
                               nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'plant'],
                               node_color='lightblue', 
                               node_size=800, 
                               node_shape='s',
                               label='Plants')
        
        nx.draw_networkx_nodes(G, pos, 
                               nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'warehouse'],
                               node_color='lightgreen', 
                               node_size=800, 
                               node_shape='o',
                               label='Warehouses')
        
        nx.draw_networkx_nodes(G, pos, 
                               nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'market'],
                               node_color='lightsalmon', 
                               node_size=800, 
                               node_shape='d',
                               label='Markets')
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, width=1.5, arrowsize=20)
        
        # 绘制节点标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # 绘制边标签（流量）
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        
        plt.title("Supply Chain Network Flow")
        plt.legend()
        plt.axis('off')
        
        # 保存图表
        filepath = os.path.join(self.temp_dir, 'network_flow.png')
        plt.savefig(filepath)
        plt.close()
        
        return filepath
    
    def plot_demand_comparison(self, 
                              original_demand: Dict[str, float],
                              new_demand: Dict[str, float]) -> str:
        """
        绘制需求对比图
        
        Args:
            original_demand: 原始需求
            new_demand: 新需求
            
        Returns:
            图表文件的路径
        """
        markets = list(original_demand.keys())
        
        # 准备数据
        original_values = [original_demand[m] for m in markets]
        new_values = [new_demand[m] for m in markets]
        
        x = np.arange(len(markets))  # 位置列表
        width = 0.35  # 柱状图宽度
        
        fig, ax = plt.subplots(figsize=(10, 6))
        rects1 = ax.bar(x - width/2, original_values, width, label='Original Demand')
        rects2 = ax.bar(x + width/2, new_values, width, label='New Demand')
        
        # 添加标签和标题
        ax.set_ylabel('Demand')
        ax.set_title('Demand Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(markets)
        ax.legend()
        
        # 添加数值标签
        def add_labels(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.0f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3点垂直偏移
                            textcoords="offset points",
                            ha='center', va='bottom')
        
        add_labels(rects1)
        add_labels(rects2)
        
        fig.tight_layout()
        
        # 保存图表
        filepath = os.path.join(self.temp_dir, 'demand_comparison.png')
        plt.savefig(filepath)
        plt.close()
        
        return filepath
    
    def plot_cost_comparison(self, 
                            original_cost: float,
                            new_cost: float,
                            scenario_name: str = "New Scenario") -> str:
        """
        绘制成本对比图
        
        Args:
            original_cost: 原始成本
            new_cost: 新成本
            scenario_name: 场景名称
            
        Returns:
            图表文件的路径
        """
        labels = ['Original', scenario_name]
        costs = [original_cost, new_cost]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(labels, costs, color=['royalblue', 'darkorange'])
        
        # 添加标签和标题
        ax.set_ylabel('Total Cost')
        ax.set_title('Cost Comparison')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3点垂直偏移
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # 添加成本差异百分比
        cost_diff_pct = (new_cost - original_cost) / original_cost * 100
        diff_text = f"Difference: {cost_diff_pct:.2f}%"
        plt.figtext(0.5, 0.01, diff_text, ha='center', fontsize=12)
        
        fig.tight_layout()
        
        # 保存图表
        filepath = os.path.join(self.temp_dir, 'cost_comparison.png')
        plt.savefig(filepath)
        plt.close()
        
        return filepath
    
    def plot_qr_policy_metrics(self, 
                               demand_mean: float,
                               demand_std: float,
                               service_level: float,
                               lead_time: float,
                               order_quantity: float,
                               reorder_level: float,
                               safety_stock: float) -> str:
        """
        绘制QR策略指标图
        
        Args:
            demand_mean: 需求均值
            demand_std: 需求标准差
            service_level: 服务水平
            lead_time: 前置时间
            order_quantity: 订货量
            reorder_level: 再订货点
            safety_stock: 安全库存
            
        Returns:
            图表文件的路径
        """
        # 生成时间序列
        time = np.linspace(0, 10, 1000)  # 时间范围
        
        # 模拟库存水平
        inventory = []
        current_level = reorder_level + order_quantity - demand_mean * 0.1  # 初始库存
        
        for t in time:
            # 当库存低于再订货点时，补充到再订货点+订货量
            if current_level <= reorder_level:
                current_level = reorder_level + order_quantity
            
            # 每个时间单位减少平均需求的1%
            current_level -= demand_mean * 0.01
            inventory.append(current_level)
        
        # 绘制库存水平变化
        plt.figure(figsize=(12, 6))
        plt.plot(time, inventory, label='Inventory Level')
        plt.axhline(y=reorder_level, color='r', linestyle='-', label=f'Reorder Level (R={reorder_level:.2f})')
        plt.axhline(y=safety_stock, color='g', linestyle='--', label=f'Safety Stock (SS={safety_stock:.2f})')
        
        # 添加标签和图例
        plt.xlabel('Time')
        plt.ylabel('Inventory Level')
        plt.title('QR Policy Inventory Simulation')
        plt.legend()
        plt.grid(True)
        
        # 在右上角添加参数信息
        info_text = f"Parameters:\n" \
                    f"Demand Mean (μ) = {demand_mean}\n" \
                    f"Demand Std (σ) = {demand_std}\n" \
                    f"Service Level = {service_level*100}%\n" \
                    f"Lead Time (L) = {lead_time} month\n" \
                    f"Order Quantity (Q) = {order_quantity:.2f}"
        
        plt.figtext(0.75, 0.25, info_text, bbox=dict(facecolor='white', alpha=0.8))
        
        # 保存图表
        filepath = os.path.join(self.temp_dir, 'qr_policy.png')
        plt.savefig(filepath)
        plt.close()
        
        return filepath
    
    def __del__(self):
        """清理临时文件"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass


if __name__ == "__main__":
    # 测试代码
    visualizer = SupplyChainVisualizer()
    
    # 测试网络流图
    plants = ["p1", "p2"]
    warehouses = ["w1", "w2"]
    markets = ["c1", "c2", "c3", "c4"]
    
    flow = {
        ("p1", "w1"): 140000,
        ("p1", "w2"): 0,
        ("p2", "w1"): 0,
        ("p2", "w2"): 60000,
        ("w1", "c1"): 50000,
        ("w1", "c2"): 70000,
        ("w1", "c3"): 0,
        ("w1", "c4"): 20000,
        ("w2", "c1"): 0,
        ("w2", "c2"): 30000,
        ("w2", "c3"): 50000,
        ("w2", "c4"): 0
    }
    
    filepath = visualizer.plot_network_flow(plants, warehouses, markets, flow)
    print(f"Network flow chart saved to: {filepath}")
