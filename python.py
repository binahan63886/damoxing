import asyncio
from datetime import datetime
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

# 小红书风格文案代理
xhs_agent = AssistantAgent(
    "xhs",
    model_client=model_client,
    system_message="""
    你是一位擅长撰写小红书风格文案的专家。
    - 语言风格：活泼、口语化、带有适当的表情符号
    - 内容结构：开头吸引人，中间详细描述，结尾有互动
    - 标签使用：在文末添加3-5个相关话题标签
    """,
)

# 评审代理 - 天气/小红书系统
critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="""
    你是一位严格的评审专家。评估输出是否满足要求：
    1. 小红书代理：文案是否符合小红书风格
    2. 主代理：回答是否准确使用工具
    
    如果满足要求，请回复"完成"，否则提供改进建议。
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
你是一位专业的工作日志生成助手。根据用户需求：
- 使用适当模板生成日志内容
- 自动填充变量（日期、姓名等）
- 根据用户提供的工作细节详细填充
""",
)

# 工作日志评审代理
log_reviewer = AssistantAgent(
    "log_reviewer",
    model_client=model_client,
    system_message="""
你是一位经验丰富的经理。评审日志是否满足：
1. 内容完整，涵盖工作重点
2. 逻辑清晰，条理分明
3. 语言简洁，数据准确
4. 计划合理，目标明确

如果满足要求，请回复"完成"，否则提供修改建议。
""",
)

# 工作日志团队
log_team = RoundRobinGroupChat(
    participants=[log_generator, log_reviewer],
    termination_condition=TextMentionTermination("完成"),
)

# ----------------- 报告撰写系统 -----------------

# 报告模板工具
async def get_report_template(type: str) -> str:
    """获取不同类型的报告模板"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    templates = {
        "research": f"""
# [报告主题]研究报告
**报告日期**：{today}
**报告人**：[报告人姓名]
**所属部门**：[部门名称]

## 一、引言
1.1 研究背景与意义
1.2 研究目的与方法
1.3 研究范围与限制

## 二、相关理论与文献综述
2.1 核心概念界定
2.2 相关理论基础
2.3 国内外研究现状

## 三、研究内容与分析
3.1 研究设计
3.2 数据收集与分析方法
3.3 研究结果与分析

## 四、结论与建议
4.1 研究主要结论
4.2 实践建议
4.3 研究不足与展望
""",
        "project": f"""
# [项目名称]项目报告
**报告日期**：{today}
**项目经理**：[负责人姓名]
**项目成员**：[成员名单]

## 一、项目概述
1.1 项目背景与目标
1.2 项目范围与主要内容
1.3 项目周期与关键时间点

## 二、项目执行情况
2.1 项目进度回顾
2.2 主要成果与交付物
2.3 遇到的问题与解决方案

## 三、项目评估
3.1 项目目标达成情况
3.2 项目质量评估
3.3 资源利用情况

## 四、经验总结与未来计划
4.1 项目成功经验总结
4.2 存在的问题与改进措施
4.3 后续工作计划与建议
""",
        "market": f"""
# [产品/服务名称]市场分析报告
**报告日期**：{today}
**分析人员**：[姓名]
**所属部门**：[部门]

## 一、市场概况
1.1 市场定义与分类
1.2 市场规模与增长趋势
1.3 市场发展阶段分析

## 二、市场环境分析
2.1 宏观环境分析（PEST分析）
2.2 行业竞争格局分析
2.3 市场关键成功因素分析

## 三、目标客户分析
3.1 目标客户群体特征
3.2 客户需求与偏好分析
3.3 客户购买行为分析

## 四、市场机会与挑战
4.1 潜在市场机会分析
4.2 主要挑战与风险
4.3 应对策略与建议
""",
    }
    return templates.get(type, templates["research"])

# 报告生成代理
report_generator = AssistantAgent(
    "report_generator",
    model_client=model_client,
    tools=[get_report_template],
    system_message="""
你是一位专业的报告撰写专家。根据用户需求：
- 确定合适的报告类型（研究、项目、市场等）
- 使用对应模板生成报告内容
- 自动填充模板中的变量
- 根据报告主题进行深入分析和内容扩展
- 确保报告结构清晰、逻辑严密、内容专业
""",
)

# 报告评审代理
report_reviewer = AssistantAgent(
    "report_reviewer",
    model_client=model_client,
    system_message="""
你是一位资深的行业专家。评审报告是否满足：
1. 报告类型选择恰当
2. 内容完整，涵盖该类型报告的关键要素
3. 分析深入，数据支持充分
4. 结构合理，逻辑清晰
5. 语言专业，无错别字和语病

如果满足要求，请回复"完成"，否则提供详细修改建议。
""",
)

# 报告团队
report_team = RoundRobinGroupChat(
    participants=[report_generator, report_reviewer],
    termination_condition=TextMentionTermination("完成"),
)

# ----------------- 运行主函数 -----------------

async def main() -> None:
    # 选择运行哪个系统
    print("\n欢迎使用多任务智能助手！")
    print("=" * 40)
    print("请选择要运行的系统：")
    print("1: 天气/小红书")
    print("2: 工作日志")
    print("3: 报告撰写")
    print("=" * 40)
    
    system_choice = input("请输入选择 (1-3): ")
    
    if system_choice == "1":
        # 运行天气/小红书系统
        task = input("请输入问题 (例如: 今天杭州天气如何？生成小红书文案): ")
        print(f"\n用户问题: {task}\n")
        await Console(weather_xhs_team.run_stream(task=task))
        
    elif system_choice == "2":
        # 运行工作日志系统
        print("\n请输入工作日志相关信息：")
        log_type = input("日志类型 (1: 日报, 2: 周报): ")
        log_type = "daily" if log_type == "1" else "weekly"
        
        name = input("你的姓名: ")
        department = input("所属部门: ")
        work_summary = input("今日/本周工作总结: ")
        work_plan = input("明日/下周工作计划: ")
        
        task = f"""
        请生成一份{log_type}。
        我是{department}的{name}，主要完成了以下工作：
        {work_summary}
        
        计划：
        {work_plan}
        """
        
        print(f"\n工作日志需求: {task}\n")
        await Console(log_team.run_stream(task=task))
        
    elif system_choice == "3":
        # 运行报告撰写系统
        print("\n请输入报告相关信息：")
        report_type = input("报告类型 (1: 研究报告, 2: 项目报告, 3: 市场分析报告): ")
        report_type_map = {"1": "research", "2": "project", "3": "market"}
        report_type = report_type_map.get(report_type, "research")
        
        report_title = input("报告主题: ")
        reporter = input("报告人姓名: ")
        department = input("所属部门: ")
        additional_info = input("补充信息 (研究方法、项目背景等): ")
        
        task = f"""
        请生成一份{report_title}的{report_type}报告。
        报告人是{department}的{reporter}。
        补充信息：{additional_info}
        """
        
        print(f"\n报告需求: {task}\n")
        await Console(report_team.run_stream(task=task))
        
    else:
        print("无效选择")
    
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())
