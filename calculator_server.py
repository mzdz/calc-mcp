#!/usr/bin/env python
from mcp.server.fastmcp import FastMCP

# 创建MCP服务器实例
mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: float, b: float) -> float:
    """将两个数相加
    
    参数:
        a: 第一个数
        b: 第二个数
        
    返回:
        两个数的和
    """
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """从第一个数中减去第二个数
    
    参数:
        a: 第一个数
        b: 第二个数
        
    返回:
        两个数的差
    """
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """将两个数相乘
    
    参数:
        a: 第一个数
        b: 第二个数
        
    返回:
        两个数的积
    """
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """将第一个数除以第二个数
    
    参数:
        a: 被除数
        b: 除数
        
    返回:
        两个数的商
    
    抛出:
        ValueError: 当除数为0时
    """
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b

@mcp.prompt()
def calculate_prompt(operation: str, a: float, b: float) -> str:
    """创建一个计算提示
    
    参数:
        operation: 操作类型 (add, subtract, multiply, divide)
        a: 第一个数
        b: 第二个数
        
    返回:
        计算提示字符串
    """
    operations = {
        "add": "加",
        "subtract": "减",
        "multiply": "乘",
        "divide": "除"
    }
    op_text = operations.get(operation, operation)
    return f"请计算 {a} {op_text} {b} 的结果。"

@mcp.resource("calculator://help")
def help_resource() -> str:
    """提供计算器帮助信息"""
    return """
    计算器 MCP 服务器
    
    可用的工具:
    - add(a, b): 计算 a + b
    - subtract(a, b): 计算 a - b
    - multiply(a, b): 计算 a * b
    - divide(a, b): 计算 a / b (注意: b不能为0)
    
    可用的提示:
    - calculate_prompt(operation, a, b): 创建计算操作提示
    
    可用的资源:
    - calculator://help: 这个帮助信息
    - calculator://history: 最近的计算历史
    """

# 存储计算历史
calculation_history = []

@mcp.tool()
def save_calculation(operation: str, a: float, b: float, result: float) -> bool:
    """保存计算到历史记录
    
    参数:
        operation: 操作类型
        a: 第一个数
        b: 第二个数
        result: 计算结果
        
    返回:
        保存是否成功
    """
    calculation_history.append({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    })
    # 最多保存最近的10条历史记录
    if len(calculation_history) > 10:
        calculation_history.pop(0)
    return True

@mcp.resource("calculator://history")
def history_resource() -> str:
    """获取计算历史"""
    if not calculation_history:
        return "暂无计算历史"
    
    history_text = "计算历史:\n"
    for i, calc in enumerate(calculation_history, 1):
        op = calc["operation"]
        a = calc["a"]
        b = calc["b"]
        result = calc["result"]
        
        op_symbols = {
            "add": "+",
            "subtract": "-",
            "multiply": "*",
            "divide": "/"
        }
        op_symbol = op_symbols.get(op, op)
        
        history_text += f"{i}. {a} {op_symbol} {b} = {result}\n"
    
    return history_text

# 如果直接运行此文件，启动MCP服务器
if __name__ == "__main__":
    mcp.run() 