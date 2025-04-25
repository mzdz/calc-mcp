#!/usr/bin/env python
import asyncio
from typing import Tuple, Optional, Dict, Any
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

async def run_calculator_example():
    """运行计算器客户端示例"""
    # 创建连接到计算器服务器的参数
    server_params = StdioServerParameters(
        command="python",
        args=["advanced_calculator_server.py"],
    )
    
    print("连接到计算器 MCP 服务器...")
    
    # 连接到服务器
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()
            print("连接成功!")
            
            # 列出可用工具
            tools = await session.list_tools()
            print("\n可用工具:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
            
            # 列出可用资源
            resources = await session.list_resources()
            print("\n可用资源:")
            for resource in resources:
                print(f"- {resource.name}: {resource.description}")
            
            # 读取帮助资源
            help_content, _ = await session.read_resource("calculator://help")
            print("\n帮助信息:")
            print(help_content)
            
            # 执行一些基本计算
            print("\n执行基本计算:")
            
            # 加法
            add_result = await session.call_tool("add", {"a": 5, "b": 3})
            print(f"5 + 3 = {add_result}")
            
            # 减法
            subtract_result = await session.call_tool("subtract", {"a": 10, "b": 4})
            print(f"10 - 4 = {subtract_result}")
            
            # 乘法
            multiply_result = await session.call_tool("multiply", {"a": 6, "b": 7})
            print(f"6 * 7 = {multiply_result}")
            
            # 除法
            divide_result = await session.call_tool("divide", {"a": 20, "b": 5})
            print(f"20 / 5 = {divide_result}")
            
            # 执行高级计算
            print("\n执行高级计算:")
            
            # 幂运算
            power_result = await session.call_tool("power", {"base": 2, "exponent": 8})
            print(f"2^8 = {power_result}")
            
            # 平方根
            sqrt_result = await session.call_tool("sqrt", {"value": 144})
            print(f"√144 = {sqrt_result}")
            
            # 表达式计算
            expr_result = await session.call_tool("evaluate_expression", 
                                                  {"expression": "3 * (4 + 2) / 2"})
            print(f"3 * (4 + 2) / 2 = {expr_result}")
            
            # 获取计算历史
            history, _ = await session.read_resource("calculator://history")
            print("\n计算历史:")
            print(history)
            
            # 订阅历史资源变化
            subscription_id = await session.subscribe_resource("calculator://history")
            print(f"\n已订阅历史资源 (ID: {subscription_id})")
            
            # 再进行一次计算，应该会触发历史记录更新
            print("\n执行另一个计算来触发历史记录更新:")
            complex_expr_result = await session.call_tool("evaluate_expression", 
                                                          {"expression": "2 + 2 * 2"})
            print(f"2 + 2 * 2 = {complex_expr_result}")
            
            # 等待资源更新通知
            print("\n等待资源更新通知...")
            try:
                # 等待最多5秒获取通知
                notification = await asyncio.wait_for(session.next_notification(), 5.0)
                print(f"收到通知: {notification}")
                
                # 读取更新后的历史
                updated_history, _ = await session.read_resource("calculator://history")
                print("\n更新后的计算历史:")
                print(updated_history)
            except asyncio.TimeoutError:
                print("等待通知超时")
            
            # 取消订阅
            await session.unsubscribe_resource(subscription_id)
            print("\n已取消订阅历史资源")

if __name__ == "__main__":
    asyncio.run(run_calculator_example()) 