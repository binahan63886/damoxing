import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination, SourceMatchTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 定义模型客户端
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

# 定义售前工具函数
async def get_phone_info(phone_model: str) -> str:
    """获取手机型号信息"""
    phone_specs = {
        "小米15": "2025年新出的手机，搭配了16GB运存，256GB储存，搭载最新处理器，支持120W快充",
        "华为Mate80": "高端旗舰机型，配备徕卡四摄，5000mAh大电池，支持无线充电",
        "苹果iPhone16": "搭载A19处理器，6.1英寸OLED屏幕，全新的影像系统",
        "三星Galaxy S25": "2K分辨率屏幕，2亿像素主摄，防水防尘等级IP68"
    }
    return phone_specs.get(phone_model, f"抱歉，我没有找到{phone_model}的相关信息。")

# 定义售后工具函数
async def diagnose_issue(issue: str) -> str:
    """诊断手机问题"""
    common_issues = {
        "无法开机": "请检查手机是否有足够电量，可以尝试长按电源键10秒强制重启。如果问题仍然存在，请联系售后。",
        "电池耗电快": "请检查是否有异常耗电的应用程序，尝试关闭后台运行的程序。如果问题仍然存在，请联系售后。",
        "屏幕损坏": "屏幕损坏需要更换屏幕，请携带购机凭证到售后服务中心进行维修。",
        "充电问题": "请检查充电线和充电器是否正常工作，尝试更换充电线或充电器。如果问题仍然存在，请联系售后。"
    }
    return common_issues.get(issue, f"抱歉，我无法诊断这个问题：{issue}。请联系售后获取帮助。")

# 初始化售前客服
before_agent = AssistantAgent(
    name='before_agent',
    model_client=model_client,
    tools=[get_phone_info],
    system_message="你是一个手机店售前客服，帮助用户了解产品，完成销售工作。你可以回答关于手机型号、配置、价格等问题。",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# 初始化售后客服
after_agent = AssistantAgent(
    name="after_agent",
    model_client=model_client,
    tools=[diagnose_issue],
    system_message="你是一个手机店售后客服，帮助用户解决使用上遇到的问题和一些退换货请求。你可以诊断手机问题并提供解决方案。",
    reflect_on_tool_use=True,
    model_client_stream=True,
)

# 定义角色描述 - 以字符串形式定义，避免字典格式问题
roles_description = """
- before_agent: 售前客服：负责解答产品信息、配置、价格等问题
- after_agent: 售后客服：负责解决手机使用问题、提供维修建议和处理退换货
"""

# 定义终止条件
source_termination = SourceMatchTermination(['before_agent', 'after_agent'])

# 定义选择器提示 - 使用字符串形式，避免格式化问题
selector_prompt = f"选择一个agent去完成任务，这是agent的职责：\n{roles_description}\n这是当前任务的上下文消息：{{history}}"

# 创建选择器团队
team = SelectorGroupChat(
    [before_agent, after_agent],
    model_client=model_client,
    selector_prompt=selector_prompt,
    termination_condition=source_termination,
    allow_repeated_speaker=True,
)

# 运行对话
async def main() -> None:
    # 显示欢迎消息
    print("欢迎来到手机店客服系统！")
    print("售前客服：负责解答产品信息、配置、价格等问题")
    print("售后客服：负责解决手机使用问题、提供维修建议和处理退换货")
    print("=" * 50)
    
    # 启动对话
    await Console(team.run_stream(task="我的小米15手机无法开机了"))
    
    # 关闭模型客户端连接
    await model_client.close()

# 运行主函数
asyncio.run(main())
