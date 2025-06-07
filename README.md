# 计算器 MCP 服务器
[![smithery badge](https://smithery.ai/badge/@mzdz/calc-mcp-server)](https://smithery.ai/server/@mzdz/calc-mcp-server)

这是一个使用 [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/python-sdk) 开发的计算器服务器，提供基本的算术运算功能。

## 功能特点

### 基本计算器功能
- 加法、减法、乘法、除法的基本运算
- 自动记录计算历史
- 通过资源 API 访问帮助信息和历史记录

### 高级计算器功能
- 幂运算和平方根计算
- 表达式计算（使用安全的表达式求值）
- 资源更新通知（当历史记录更新时）

## 安装要求

1. Python 3.7 或更高版本
2. MCP Python SDK

## 安装步骤

### Installing via Smithery

To install 计算器 MCP 服务器 for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@mzdz/calc-mcp):

```bash
npx -y @smithery/cli install @mzdz/calc-mcp --client claude
```

### Manual Installation
1. 克隆或下载此仓库
2. 安装依赖项：

```bash
pip install -r requirements.txt
```

## 使用方法

### 运行基本计算器服务器

```bash
python calculator_server.py
```

或者使用 MCP 命令：

```bash
mcp run calculator_server.py
```

### 运行高级计算器服务器

```bash
python advanced_calculator_server.py
```

### 运行客户端示例

```bash
python calculator_client.py
```

## 可用工具

### 基本工具：
- `add(a, b)`: 计算 a + b
- `subtract(a, b)`: 计算 a - b
- `multiply(a, b)`: 计算 a * b
- `divide(a, b)`: 计算 a / b

### 高级工具（仅在高级计算器中可用）：
- `power(base, exponent)`: 计算 base 的 exponent 次幂
- `sqrt(value)`: 计算平方根
- `evaluate_expression(expression)`: 计算数学表达式字符串

## 可用资源

- `calculator://help`: 获取帮助信息
- `calculator://history`: 获取计算历史记录

## 示例代码

### 使用 Python 客户端调用计算器服务器

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["advanced_calculator_server.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 调用加法工具
            result = await session.call_tool("add", {"a": 5, "b": 3})
            print(f"5 + 3 = {result}")
            
            # 读取计算历史
            history, _ = await session.read_resource("calculator://history")
            print(history)

if __name__ == "__main__":
    asyncio.run(main())
```

## 项目结构

- `calculator_server.py`: 基本计算器 MCP 服务器
- `advanced_calculator_server.py`: 高级计算器 MCP 服务器，带有更多功能
- `calculator_client.py`: 计算器客户端示例
- `requirements.txt`: 项目依赖
- `README.md`: 项目文档

## 进一步开发

你可以通过以下方式扩展这个计算器服务器：

1. 添加更多数学函数（如三角函数、对数等）
2. 实现更复杂的表达式解析器
3. 添加图形界面
4. 实现持久化存储计算历史
5. 添加用户自定义变量和函数

## 许可证

MIT 许可证 
