
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 模型客户端配置
model_client = OpenAIChatCompletionClient(
    model="Qwen/Qwen3-30B-A3B",
    api_key="sk-vtizljmfspznmpucgkqalbyiiernhkynmlsuqtnuscaruxlo",
    base_url="https://api.siliconflow.cn/v1/",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "qwen",
        "structured_output": True,
        "multiple_system_messages": True,
    },
)

# ----------------- 天气/小红书系统 -----------------

# 定义天气工具
async def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"The weather in {city} is 73 degrees and Sunny."

# 主代理 - 负责获取天气信息
primary_agent = AssistantAgent(
    "primary",
    model_client=model_client,
    tools=[get_weather],
    system_message="你是一个知识渊博的助手，擅长回答各种问题。如果你不知道答案，可以使用提供的工具。",
)

# 小红书风格文案代理 - 负责将天气信息转化为小红书风格的文案
xhs_agent = AssistantAgent(
    "xhs",
    model_client=model_client,
    system_message="""
    你是一位擅长撰写小红书风格文案的专家。
    - 语言风格：活泼、口语化、带有适当的表情符号
    - 内容结构：开头吸引人，中间详细描述，结尾有互动
    - 标签使用：在文末添加3-5个相关话题标签
    
    例如：
    🌸今日天气好好呀！阳光明媚🌞温度适宜，太适合出门逛街啦～
    大家都打算怎么度过这个美好的周末呢？
    #天气好心情就好 #周末出行 #阳光明媚的一天
    """,
)

# 评审代理 - 负责评估最终输出质量
critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="""
    你是一位严格的评审专家。仔细评估输出内容是否满足以下要求：
    1. 小红书代理：文案是否符合小红书风格（语言活泼、有表情符号、结构合理、标签恰当）
    2. 主代理：回答是否准确、完整地使用了工具
    
    如果所有要求都满足，请回复"完成"，否则提供具体的改进建议。
    """,
)

# 天气/小红书团队
weather_xhs_team = RoundRobinGroupChat(
    participants=[primary_agent, xhs_agent, critic_agent],
    termination_condition=TextMentionTermination("完成"),
)

# ----------------- 工作日志系统 -----------------

# 工作日志模板工具
async def get_log_template(type: str) -> str:
    """获取不同类型的工作日志模板"""
    templates = {
        "daily": """
### 今日工作日志
**日期**：[日期]
**员工姓名**：[姓名]
**部门**：[部门]

#### 一、今日工作总结
1. 主要工作内容
2. 完成情况
3. 遇到的问题及解决方案

#### 二、明日工作计划
1. 计划完成的工作
2. 需协调的资源

#### 三、其他事项
1. 工作建议
2. 风险预警
""",
        "weekly": """
### 本周工作总结与计划
**日期范围**：[开始日期]-[结束日期]
**员工姓名**：[姓名]
**部门**：[部门]

#### 一、本周工作总结
1. 重点工作完成情况
2. 遇到的问题及解决情况
3. 工作成果与亮点

#### 二、下周工作计划
1. 主要工作目标
2. 具体工作安排
3. 需支持与协调事项

#### 三、自我评估
1. 本周成长与收获
2. 存在的不足与改进措施
""",
    }
    return templates.get(type, templates["daily"])

# 工作日志生成代理
log_generator = AssistantAgent(
    "log_generator",
    model_client=model_client,
    tools=[get_log_template],
    system_message="""
你是一位专业的工作日志生成助手。根据用户需求，使用适当的模板生成工作日志内容。
- 确保内容真实、具体、有条理
- 根据工作性质和需求选择合适的日志类型（日报/周报）
- 自动填充模板中的变量（日期、姓名等）
- 可根据用户提供的工作内容细节进行详细填充
""",
)

# 工作日志评审代理
log_reviewer = AssistantAgent(
    "log_reviewer",
    model_client=model_client,
    system_message="""
你是一位经验丰富的经理，擅长评审工作日志。仔细检查日志内容是否满足以下要求：
1. 内容完整，涵盖工作重点
2. 逻辑清晰，条理分明
3. 语言简洁，数据准确
4. 计划合理，目标明确

如果日志满足要求，请回复"完成"，否则提供具体的修改建议。
""",
)

# 工作日志团队
log_team = RoundRobinGroupChat(
    participants=[log_generator, log_reviewer],
    termination_condition=TextMentionTermination("完成"),
)

# ----------------- 运行主函数 -----------------

async def main() -> None:
    # 选择运行哪个系统
    system_choice = input("请选择要运行的系统 (1: 天气/小红书, 2: 工作日志): ")
    
    if system_choice == "1":
        # 运行天气/小红书系统
        task = input("请输入问题 (例如: 今天杭州天气怎么样？请生成一篇小红书风格的文案。): ")
        print(f"用户问题: {task}\n")
        await Console(weather_xhs_team.run_stream(task=task))
    elif system_choice == "2":
        # 运行工作日志系统
        task = input("请输入工作日志内容 (包括个人信息、工作内容等): ")
        print(f"工作日志需求: {task}\n")
        await Console(log_team.run_stream(task=task))
    else:
        print("无效选择")
    
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
