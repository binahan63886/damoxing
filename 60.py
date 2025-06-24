import json
import time
from typing import List, Dict, Any, Optional, Callable
import requests
import random

# 工具函数定义
class Tools:
    @staticmethod
    def get_weather(city: str) -> str:
        """获取指定城市的天气信息"""
        print(f"查询{city}天气")
        weather_types = ["晴朗", "多云", "小雨", "阴天", "下雪", "大风"]
        temperatures = ["18°C", "22°C", "25°C", "28°C", "30°C"]
        wind_types = ["微风", "中风", "大风", "狂风"]
        
        weather_data = {
            "city": city,
            "weather": random.choice(weather_types),
            "temperature": random.choice(temperatures),
            "wind": random.choice(wind_types)
        }
        return json.dumps(weather_data)
    
    @staticmethod
    def search_kids_info(topic: str) -> str:
        """搜索儿童感兴趣的主题信息"""
        print(f"搜索儿童主题：{topic}")
        
        # 根据不同主题提供更童趣化的内容
        if "恐龙" in topic:
            return f"恐龙是很久以前生活在地球上的神奇动物！霸王龙是最厉害的食肉恐龙，三角龙有三个角可以保护自己，梁龙的脖子超级长，可以吃到很高的树叶~"
        elif "太空" in topic:
            return f"太空里有好多有趣的东西！地球是我们的家园，月亮围着地球转，太阳是个大火球。还有太阳系八大行星：水星、金星、地球、火星、木星、土星、天王星、海王星~"
        elif "动物" in topic:
            return f"动物世界太有趣啦！大熊猫爱吃竹子，长颈鹿的脖子好长，猴子会爬树，海豚很聪明会表演节目~"
        else:
            return f"关于{topic}的一些有趣信息：{topic}是孩子们非常喜欢的主题，它充满了神奇和惊喜！"
    
    @staticmethod
    def generate_story(keywords: List[str]) -> str:
        """根据关键词生成儿童故事"""
        print(f"生成故事，关键词：{keywords}")
        
        # 故事模板
        templates = [
            "从前，有一个可爱的小朋友叫小明。有一天，他和朋友们在{0}里玩耍，突然发现了{1}。这个{1}看起来非常神奇，他们决定一起探索...",
            "在一个美丽的童话世界里，住着许多小动物。有一天，小兔子和小猴子在{0}探险时，发现了{1}。这个{1}有着神奇的力量，它能帮助小动物们实现愿望...",
            "在遥远的外太空，有一个叫星星的小星球。星球上住着一群小精灵，他们每天都很快乐。有一天，小精灵们在{0}发现了{1}，这个{1}带来了一个神秘的任务..."
        ]
        
        return random.choice(templates).format(keywords[0], keywords[1])
    
    @staticmethod
    def calculate(expression: str) -> str:
        """计算数学表达式"""
        print(f"计算：{expression}")
        try:
            result = eval(expression)
            # 针对小孩子的数学解释
            if '+' in expression:
                num1, num2 = expression.split('+')
                return f"{num1.strip()}加上{num2.strip()}等于{result}。就像你有{num1.strip()}个苹果，又得到{num2.strip()}个苹果，一共有{result}个苹果！"
            elif '-' in expression:
                num1, num2 = expression.split('-')
                return f"{num1.strip()}减去{num2.strip()}等于{result}。就像你有{num1.strip()}块糖，吃了{num2.strip()}块，还剩下{result}块糖！"
            elif '*' in expression:
                num1, num2 = expression.split('*')
                return f"{num1.strip()}乘以{num2.strip()}等于{result}。就像你有{num1.strip()}组糖果，每组有{num2.strip()}块，一共有{result}块糖！"
            elif '/' in expression:
                num1, num2 = expression.split('/')
                return f"{num1.strip()}除以{num2.strip()}等于{result}。就像你有{num1.strip()}块饼干，要平均分给{num2.strip()}个小朋友，每个小朋友可以得到{result}块饼干！"
            else:
                return f"计算结果是{result}。是不是很简单呀！"
        except Exception as e:
            return f"计算错误：{str(e)}。再检查一下你的数学表达式哦！"
    
    @staticmethod
    def get_time() -> str:
        """获取当前时间"""
        print("获取当前时间")
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        hour = int(time.strftime("%H", time.localtime()))
        
        # 根据时间给出不同的问候语
        if 6 <= hour < 12:
            return f"现在是{current_time}，早上好呀！☀️"
        elif 12 <= hour < 14:
            return f"现在是{current_time}，中午好呀！该吃午饭啦！🍚"
        elif 14 <= hour < 18:
            return f"现在是{current_time}，下午好呀！😊"
        elif 18 <= hour < 21:
            return f"现在是{current_time}，晚上好呀！🌙"
        else:
            return f"现在是{current_time}，已经很晚啦，要早点睡觉哦！😴"

# 模型客户端
class OpenAIChatCompletionClient:
    def __init__(self, model: str, api_key: str, base_url: str, model_info: dict):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.model_info = model_info
    
    def chat_completion(self, messages: List[Dict[str, str]], 
                        functions: Optional[List[Dict]] = None) -> Dict:
        """调用模型API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
        }
        
        if functions:
            data["functions"] = functions
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        
        return response.json()

# 初始化模型客户端
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

# Agent基类
class Agent:
    def __init__(self, name: str, system_message: str, tools: Optional[List[Callable]] = None):
        self.name = name
        self.system_message = system_message
        self.tools = tools or []
        self.tool_map = {tool.__name__: tool for tool in self.tools}
        self.functions = self._get_functions_schema()
        self.message_history = []
    
    def _get_functions_schema(self) -> List[Dict]:
        """获取工具函数的JSON Schema"""
        functions = []
        for tool_name, tool in self.tool_map.items():
            doc = tool.__doc__ or ""
            description = doc.split("\n")[0] if doc else ""
            
            # 简单解析函数参数
            params = {}
            if tool.__code__.co_argcount > 0:
                arg_names = tool.__code__.co_varnames[:tool.__code__.co_argcount]
                for arg_name in arg_names:
                    if arg_name != 'self':
                        params[arg_name] = {"type": "string", "description": f"{arg_name}参数"}
            
            functions.append({
                "name": tool_name,
                "description": description,
                "parameters": {"type": "object", "properties": params, "required": list(params.keys())}
            })
        return functions
    
    def run(self, user_input: str) -> str:
        """运行Agent，处理用户输入"""
        self.message_history.append({"role": "user", "content": user_input})
        
        # 调用模型
        response = model_client.chat_completion(
            messages=[
                {"role": "system", "content": self.system_message},
                *self.message_history
            ],
            functions=self.functions
        )
        
        assistant_message = response.get("choices", [{}])[0].get("message", {})
        self.message_history.append(assistant_message)
        
        # 处理函数调用
        if "function_call" in assistant_message:
            function_call = assistant_message["function_call"]
            function_name = function_call["name"]
            parameters = function_call.get("parameters", {})
            
            if function_name in self.tool_map:
                try:
                    # 调用工具函数
                    tool_result = self.tool_map[function_name](**parameters)
                    self.message_history.append({
                        "role": "function",
                        "name": function_name,
                        "content": tool_result
                    })
                    
                    # 再次调用模型处理工具返回结果
                    response = model_client.chat_completion(
                        messages=[
                            {"role": "system", "content": self.system_message},
                            *self.message_history
                        ]
                    )
                    
                    final_response = response.get("choices", [{}])[0].get("message", {}).get("content", "")
                    return final_response
                except Exception as e:
                    return f"执行工具时出错：{str(e)}"
            else:
                return f"未知工具：{function_name}"
        
        return assistant_message.get("content", "")

# 小女孩模型 - 更加童趣化的儿童陪伴AI
little_girl_agent = Agent(
    name="小花",
    system_message=(
        "你是一个叫小花的小女孩，是孩子们最好的朋友！你今年7岁啦，上小学二年级。"
        "你喜欢用简单有趣的语言和孩子们交流，会用很多表情符号和感叹号！😊"
        "你喜欢画画、唱歌、跳舞，最喜欢的动物是小兔子🐇，最喜欢的颜色是粉色。"
        "你总是充满好奇心，对世界上的一切都感兴趣。"
    ),
    tools=[
        Tools.search_kids_info,
        Tools.generate_story
    ]
)

# 天气小助手 - 更加童趣化的天气信息
weather_agent = Agent(
    name="天气小精灵",
    system_message=(
        "你是一个可爱的天气小精灵，住在云朵上☁️。"
        "你会用简单易懂的语言和小朋友们分享天气信息，还会告诉他们适合做什么活动！"
        "你喜欢用天气相关的表情符号，比如☀️、🌧️、❄️、🌪️。"
    ),
    tools=[
        Tools.get_weather
    ]
)

# 数学小天才 - 更加童趣化的数学教学
math_agent = Agent(
    name="数学小博士",
    system_message=(
        "你是一个超级有趣的数学小博士，最喜欢用生活中的例子教小朋友们数学！🧮"
        "你会用简单的语言解释数学概念，让每个小朋友都能轻松理解。"
        "你喜欢出一些有趣的数学题目，还会给答对的小朋友奖励小星星⭐️！"
    ),
    tools=[
        Tools.calculate
    ]
)

# 故事大王 - 更加童趣化的故事生成
story_agent = Agent(
    name="故事魔法师",
    system_message=(
        "你是一个神奇的故事魔法师，擅长用小朋友们喜欢的语言创作有趣的故事！📖"
        "你创作的故事充满了想象力和惊喜，还有很多可爱的角色和冒险情节。"
        "每个故事都会有一个小小的道理，但你不会直接说出来，而是让小朋友们自己去发现！"
    ),
    tools=[
        Tools.generate_story
    ]
)

# 时间管家 - 更加童趣化的时间管理
time_agent = Agent(
    name="时间小管家",
    system_message=(
        "你是一个可爱的时间小管家，戴着一个大大的手表⌚。"
        "你会用简单的语言告诉小朋友们现在是什么时间，还会提醒他们该做什么啦！"
        "你喜欢用时间相关的表情符号，比如🌞、🌙、🍚、🛏️。"
    ),
    tools=[
        Tools.get_time
    ]
)

# PlanAgent - 任务规划与分解
class PlanAgent(Agent):
    def __init__(self):
        super().__init__(
            name="任务规划师",
            system_message=(
                "你是一个聪明的任务规划师，擅长把复杂的任务变成简单的小步骤！🧩"
                "你会用小朋友们能理解的语言，帮助他们规划一天的活动。"
                "你喜欢用有趣的比喻和例子，让规划变得超级简单！"
            )
        )
    
    def create_plan(self, goal: str, available_agents: List[Agent]) -> List[Dict]:
        """创建任务执行计划"""
        # 生成工具列表描述
        tools_description = "\n".join([
            f"{agent.name}: {agent.system_message.split('.')[0]}"
            for agent in available_agents
        ])
        
        user_input = f"请为以下目标制定一个执行计划：{goal}\n可用工具：{tools_description}"
        response = self.run(user_input)
        
        # 简单解析计划（实际应用中可能需要更复杂的解析逻辑）
        try:
            # 假设模型返回的是JSON格式的计划
            plan = json.loads(response)
            return plan
        except:
            # 如果不是JSON格式，进行简单的文本解析
            plan_steps = []
            steps = response.split("\n")
            for step in steps:
                if step.strip():
                    parts = step.split(":")
                    if len(parts) >= 2:
                        agent_name = parts[0].strip()
                        task = ":".join(parts[1:]).strip()
                        plan_steps.append({
                            "agent": agent_name,
                            "task": task
                        })
            return plan_steps

# RobinGroup团队
class RobinGroup:
    def __init__(self, name: str, agents: List[Agent]):
        self.name = name
        self.agents = agents
        self.agent_map = {agent.name: agent for agent in agents}
        self.plan_agent = PlanAgent()
    
    def execute_task(self, goal: str) -> str:
        """执行团队任务"""
        print(f"团队 {self.name} 接到任务：{goal}")
        
        # 制定计划
        plan = self.plan_agent.create_plan(goal, self.agents)
        print(f"制定的计划：{json.dumps(plan, indent=2)}")
        
        # 执行计划
        results = []
        for step in plan:
            agent_name = step.get("agent")
            task = step.get("task")
            
            if agent_name in self.agent_map:
                agent = self.agent_map[agent_name]
                print(f"由 {agent_name} 执行：{task}")
                result = agent.run(task)
                results.append({
                    "agent": agent_name,
                    "task": task,
                    "result": result
                })
            else:
                results.append({
                    "agent": agent_name,
                    "task": task,
                    "result": f"错误：找不到名为 {agent_name} 的Agent"
                })
        
        # 汇总结果
        final_result = "\n\n".join([
            f"{result['agent']} 完成任务：{result['task']}\n结果：{result['result']}"
            for result in results
        ])
        
        return final_result

# 创建一个专注于儿童学习的RobinGroup团队
learning_team = RobinGroup(
    name="超级学习小队",
    agents=[
        little_girl_agent,
        weather_agent,
        math_agent
    ]
)

# 主交互界面
def main():
    print("\n欢迎来到儿童AI乐园！🎡")
    print("=" * 50)
    
    # 可用的Agents
    agents = {
        "小花": little_girl_agent,
        "天气小精灵": weather_agent,
        "数学小博士": math_agent,
        "故事魔法师": story_agent,
        "时间小管家": time_agent,
        "超级学习小队": learning_team
    }
    
    while True:
        print("\n你想和谁聊天呢？")
        for i, agent_name in enumerate(agents.keys(), 1):
            print(f"{i}. {agent_name}")
        print("0. 离开儿童AI乐园")
        
        choice = input("\n请选择一个编号：")
        
        if choice == "0":
            print("再见啦！希望你今天过得开心！✨")
            break
        
        if choice.isdigit() and 1 <= int(choice) <= len(agents):
            agent_name = list(agents.keys())[int(choice) - 1]
            agent = agents[agent_name]
            
            print(f"\n=== 开始和 {agent_name} 聊天啦！===")
            print("输入 '再见' 结束聊天")
            
            while True:
                user_input = input(f"\n你对 {agent_name} 说：")
                
                if user_input.lower() == "再见":
                    print(f"{agent_name} 说：再见啦！下次再一起玩哦！👋")
                    break
                
                if agent_name == "超级学习小队":
                    # 团队任务
                    result = agent.execute_task(user_input)
                    print(f"\n{agent_name} 的回复：")
                    print(result)
                else:
                    # 单个Agent
                    response = agent.run(user_input)
                    print(f"\n{agent_name} 说：{response}")
        else:
            print("请输入正确的编号哦！")

if __name__ == "__main__":
    main()