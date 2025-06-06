#!/usr/bin/env python
import re
from typing import Dict, List, Any, Optional, Union
import math
from mcp.server.fastmcp import FastMCP

# 创建MCP服务器实例
mcp = FastMCP("高级计算器(Advanced Calculator)")

# 存储计算历史
calculation_history = []

@mcp.tool()
def add(a: float, b: float) -> float:
    """
    将两个数相加
    Add two numbers.
    
    参数(Parameters):
        a: 第一个数 (First number)
        b: 第二个数 (Second number)
        
    返回(Return):
        两个数的和 (Sum of the two numbers)
    """
    result = a + b
    save_calculation("add", a, b, result)
    return result

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    从第一个数中减去第二个数
    Subtract the second number from the first number.
    
    参数(Parameters):
        a: 第一个数 (First number)
        b: 第二个数 (Second number)
        
    返回(Return):
        两个数的差 (Difference of the two numbers)
    """
    result = a - b
    save_calculation("subtract", a, b, result)
    return result

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    将两个数相乘
    Multiply two numbers.
    
    参数(Parameters):
        a: 第一个数 (First number)
        b: 第二个数 (Second number)
        
    返回(Return):
        两个数的积 (Product of the two numbers)
    """
    result = a * b
    save_calculation("multiply", a, b, result)
    return result

@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    将第一个数除以第二个数
    Divide the first number by the second number.
    
    参数(Parameters):
        a: 被除数 (Dividend)
        b: 除数 (Divisor)
        
    返回(Return):
        两个数的商 (Quotient of the two numbers)
    
    抛出(Raises):
        ValueError: 当除数为0时 (When divisor is zero)
    """
    if b == 0:
        raise ValueError("除数不能为0(Divisor cannot be zero)")
    result = a / b
    save_calculation("divide", a, b, result)
    return result

@mcp.tool()
def power(base: float, exponent: float) -> float:
    """
    计算一个数的幂
    Calculate the power of a number.
    
    参数(Parameters):
        base: 底数 (Base)
        exponent: 指数 (Exponent)
        
    返回(Return):
        底数的指数次幂 (Base raised to the power of exponent)
    """
    result = math.pow(base, exponent)
    save_to_history({
        "operation": "power",
        "base": base,
        "exponent": exponent,
        "result": result
    })
    return result

@mcp.tool()
def sqrt(value: float) -> float:
    """
    计算一个数的平方根
    Calculate the square root of a number.
    
    参数(Parameters):
        value: 要计算平方根的数 (The number to calculate the square root of)
        
    返回(Return):
        输入值的平方根 (Square root of the input value)
    
    抛出(Raises):
        ValueError: 当输入为负数时 (When input is negative)
    """
    if value < 0:
        raise ValueError("不能计算负数的平方根")
    result = math.sqrt(value)
    save_to_history({
        "operation": "sqrt",
        "value": value,
        "result": result
    })
    return result

@mcp.tool()
def evaluate_expression(expression: str) -> float:
    """
    计算数学表达式
    Evaluate a mathematical expression.
    
    参数(Parameters):
        expression: 要计算的数学表达式字符串 (The mathematical expression string to evaluate)
        
    返回(Return):
        表达式计算结果 (Result of the evaluated expression)
        
    抛出(Raises):
        ValueError: 当表达式无效或包含不安全代码时 (When the expression is invalid or contains unsafe code)
    """
    # 保存原始表达式用于显示
    original_expression = expression
    
    # 替换常见的数学常量（在安全检查之前）
    expression = expression.replace("pi", str(math.pi))
    expression = expression.replace("e", str(math.e))
    
    # 安全检查 - 只允许基本的数学表达式
    if not is_safe_expression(expression):
        raise ValueError("无效或不安全的表达式(Invalid or unsafe expression)")
    
    # 计算表达式
    try:
        # 注意: 这里使用了eval()，但我们已经在is_safe_expression()中进行了安全检查
        result = eval(expression, {"__builtins__": {}}, math_globals())
        save_to_history({
            "operation": "evaluate",
            "expression": original_expression,  # 保存原始表达式用于显示
            "result": result
        })
        return result
    except Exception as e:
        raise ValueError(f"计算表达式时出错: {str(e)}(Error evaluating expression: {str(e)})")

def is_safe_expression(expression: str) -> bool:
    """检查表达式是否安全，只允许基本的数学运算符和函数(Check if the expression is safe, only allow basic mathematical operators and functions)"""
    # 保存原始表达式用于危险模式检查
    original_expression = expression
    
    # 替换数学常量后的表达式
    temp_expression = expression.replace("pi", str(math.pi)).replace("e", str(math.e))
    
    # 允许数字、运算符、小数点、空格、括号、基本数学符号和字母（用于pi和e以及函数名）
    allowed_pattern = r'^[\d\s\+\-\*\/\(\)\.\,\%\^a-zA-Z_]+$'
    
    # 检查原始表达式是否包含允许的字符
    if not re.match(allowed_pattern, original_expression):
        return False
    
    # 定义允许的数学函数
    allowed_functions = {
        'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2',
        'sinh', 'cosh', 'tanh', 'log', 'log10', 'ln', 'exp',
        'sqrt', 'abs', 'pow', 'ceil', 'floor', 'fabs', 'fmod',
        'degrees', 'radians', 'hypot'
    }
    
    # 检查函数调用
    function_calls = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', original_expression)
    for func_name in function_calls:
        if func_name.lower() not in allowed_functions:
            return False
    
    # 检查是否只包含允许的数学常量（除了函数名）
    temp_for_constants = original_expression
    
    # 移除函数调用
    temp_for_constants = re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*\s*\(', '(', temp_for_constants)
    
    # 移除数学常量
    for const in ['pi', 'e']:
        temp_for_constants = temp_for_constants.replace(const, '')
    
    # 剩下的应该只包含数字和基本运算符
    basic_pattern = r'^[\d\s\+\-\*\/\(\)\.\,\%\^]+$'
    if not re.match(basic_pattern, temp_for_constants):
        return False
    
    # 额外的安全检查：确保不包含危险的模式
    dangerous_patterns = [
        r'__\w+__',  # 防止访问特殊方法
        r'import\s+',  # 防止import语句
        r'exec\s*\(',  # 防止exec调用
        r'eval\s*\(',  # 防止嵌套eval调用
        r'open\s*\(',  # 防止文件操作
        r'input\s*\(',  # 防止输入函数
        r'print\s*\(',  # 防止print函数
        r'file\s*\(',  # 防止文件操作
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, original_expression, re.IGNORECASE):
            return False
    
    return True

def math_globals() -> Dict[str, Any]:
    """创建用于表达式计算的安全数学函数全局字典"""
    safe_list = [
        'math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos',
        'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod',
        'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi',
        'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh'
    ]
    
    safe_dict = {}
    for k in safe_list:
        if hasattr(math, k):
            safe_dict[k] = getattr(math, k)
    
    # 添加一些常量和别名
    safe_dict['pi'] = math.pi
    safe_dict['e'] = math.e
    safe_dict['ln'] = math.log  # 自然对数别名
    safe_dict['abs'] = abs  # 绝对值函数
    
    return safe_dict

def save_calculation(operation: str, a: float, b: float, result: float) -> None:
    """保存基本计算到历史记录(Save basic calculation to history)"""
    save_to_history({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    })

def save_to_history(data: Dict[str, Any]) -> None:
    """将计算保存到历史记录并发送通知(Save calculation to history and send notification)"""
    calculation_history.append(data)
    # 最多保存最近的20条历史记录
    if len(calculation_history) > 20:
        calculation_history.pop(0)
    
    # 发送资源更新通知（如果支持的话）
    if hasattr(mcp, 'notify_resource_changed'):
        mcp.notify_resource_changed("calculator://history")

@mcp.resource("calculator://help")
def help_resource() -> str:
    """
    提供计算器帮助信息
    Provide help information for the calculator.

    返回(Return):
        帮助信息字符串 (Help information string)
    """
    return """
    高级计算器 MCP 服务器
    
    基本运算工具:
    - add(a, b): 计算 a + b
    - subtract(a, b): 计算 a - b
    - multiply(a, b): 计算 a * b
    - divide(a, b): 计算 a / b (注意: b不能为0)
    
    高级运算工具:
    - power(base, exponent): 计算 base 的 exponent 次幂
    - sqrt(value): 计算平方根
    - evaluate_expression(expression): 计算数学表达式字符串
    
    可用的资源:
    - calculator://help: 这个帮助信息
    - calculator://history: 最近的计算历史
    """

@mcp.resource("calculator://history")
def history_resource() -> str:
    """
    获取计算历史
    Get calculation history.

    返回(Return):
        最近的计算历史字符串 (Recent calculation history string)
    """
    if not calculation_history:
        return "暂无计算历史(No calculation history)"
    
    history_text = "计算历史(Calculation history):\n"
    for i, calc in enumerate(calculation_history, 1):
        op = calc["operation"]
        
        if op in ["add", "subtract", "multiply", "divide"]:
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
        
        elif op == "power":
            base = calc["base"]
            exponent = calc["exponent"]
            result = calc["result"]
            history_text += f"{i}. {base}^{exponent} = {result}\n"
        
        elif op == "sqrt":
            value = calc["value"]
            result = calc["result"]
            history_text += f"{i}. √{value} = {result}\n"
        
        elif op == "evaluate":
            expression = calc["expression"]
            result = calc["result"]
            history_text += f"{i}. 表达式(Expression): {expression} = {result}\n"
    
    return history_text

@mcp.prompt()
def calculate_prompt(operation: str, a: Optional[float] = None, b: Optional[float] = None, expression: Optional[str] = None) -> str:
    """
    创建一个计算提示
    Create a calculation prompt.

    参数(Parameters):
        operation: 操作类型 (Operation type: add, subtract, multiply, divide, power, sqrt, evaluate)
        a: 第一个数 (First number, for basic operations)
        b: 第二个数 (Second number, for basic operations)
        expression: 表达式 (Expression, for evaluate operation)

    返回(Return):
        计算提示字符串 (Calculation prompt string)
    """
    if operation == "evaluate" and expression:
        return f"请计算表达式: {expression}(Please calculate the expression: {expression})"
    
    if operation in ["add", "subtract", "multiply", "divide"] and a is not None and b is not None:
        operations = {
            "add": "加(Add)",
            "subtract": "减(Subtract)",
            "multiply": "乘(Multiply)",
            "divide": "除(Divide)"
        }
        op_text = operations.get(operation, operation)
        return f"请计算 {a} {op_text} {b} 的结果。(Please calculate the result of {a} {op_text} {b})"
    
    if operation == "power" and a is not None and b is not None:
        return f"请计算 {a} 的 {b} 次方。(Please calculate {a} to the power of {b})"
    
    if operation == "sqrt" and a is not None:
        return f"请计算 {a} 的平方根。(Please calculate the square root of {a})"
    
    return "请指定有效的计算操作和参数。(Please specify a valid calculation operation and parameters)"

# 如果直接运行此文件，启动MCP服务器
if __name__ == "__main__":
    mcp.run() 