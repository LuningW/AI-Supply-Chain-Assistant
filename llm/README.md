# 供应链优化LLM辅助框架

本框架使用大型语言模型(LLM)配合优化求解器，为供应链优化问题提供人性化的交互和解释。框架遵循这样的流程：

问题的输入 → 不直接交给LLM，而是转化为optimization code → solver执行优化 → 得到解 → 把优化结果传给LLM → LLM生成解释或可视化回答

## 架构

框架主要由以下几个部分组成：

1. **中央分发模块**：根据用户问题类型将问题分类为计算型、解释型、假设型、约束型或优化型。
2. **参数提取器**：从用户问题中提取关键参数，用于调整优化模型。
3. **优化求解器**：接收参数并执行优化计算。
4. **结果解释器**：将优化结果转化为人类可理解的回答。
5. **可视化辅助工具**：生成图表以直观展示优化结果。

## 文件结构

- `supply_chain_optimization_framework.py` - 主框架实现
- `demo_solver.py` - 示例优化求解器
- `visualization_helper.py` - 可视化辅助模块
- `usage_example.py` - 使用示例
- `dispatch_prompt_updated.json` - 分发提示配置
- `supply_chain_prompts_english.json` - 供应链提示配置

## 安装与依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- numpy
- matplotlib
- networkx
- requests

## 使用方法

### 1. 配置提示模板

确保`dispatch_prompt_updated.json`和`supply_chain_prompts_english.json`文件配置正确。

### 2. 设置API密钥

设置环境变量：

```bash
export LLM_API_KEY=your_api_key_here
export LLM_ENDPOINT=https://api.openai.com/v1/chat/completions
```

### 3. 运行示例

```bash
python usage_example.py
```

### 4. 集成到您的应用

```python
from supply_chain_optimization_framework import SupplyChainOptimizationFramework

# 初始化框架
framework = SupplyChainOptimizationFramework(
    llm_api_key="your_api_key",
    llm_endpoint="https://api.openai.com/v1/chat/completions",
    dispatch_prompt_path="dispatch_prompt_updated.json",
    supply_chain_prompts_path="supply_chain_prompts_english.json"
)

# 处理用户问题
response = framework.handle_user_question("What would happen if the demand at market c1 increased by 10%?")
print(response)
```

## 支持的问题类型

1. **computation**：需要具体数值计算的问题
   - 例如：计算安全库存、再订货点等

2. **explanation**：需要解释优化决策的问题
   - 例如：解释为什么某个工厂供应更多到某个仓库

3. **whatif**：假设性问题
   - 例如：如果某市场需求增加10%会怎样

4. **constraint**：探讨约束影响的问题
   - 例如：能否只使用某个仓库供应某个市场

5. **optimization**：寻找最优解的问题
   - 例如：确定最优订货量

## 自定义求解器

您可以通过继承和扩展`demo_solver.py`中的`SupplyChainSolver`类来自定义您的优化求解器。确保实现以下方法：

```python
def solve(self, question_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据问题类型和参数解决问题
    
    Args:
        question_type: 问题类型
        params: 问题参数
        
    Returns:
        解决结果
    """
    # 您的实现...
```

## 注意事项

- 本框架需要访问LLM API，请确保您有足够的API调用额度。
- 优化模型的复杂性会影响响应时间。
- 参数提取可能会因为提问方式不明确而不准确，请使用清晰明确的问题表述。

## 贡献

欢迎提交问题报告和功能建议。如需贡献代码，请先提出讨论。

## 许可

MIT
