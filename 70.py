import json
import time
from typing import List, Dict, Any, Optional, Callable
import requests
import random
import os
from datetime import datetime

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
    
    @staticmethod
    def save_task_state(task_id: str, state: Dict) -> str:
        """保存任务状态"""
        print(f"保存任务 {task_id} 的状态")
        try:
            # 创建保存目录
            if not os.path.exists("task_states"):
                os.makedirs("task_states")
                
            file_path = f"task_states/{task_id}.json"
            with open(file_path, 'w') as f:
                json.dump(state, f, indent=2)
                
            return f"任务状态已成功保存"
        except Exception as e:
            return f"保存任务状态失败：{str(e)}"
    
    @staticmethod
    def load_task_state(task_id: str) -> Dict:
        """加载任务状态"""
        print(f"加载任务 {task_id} 的状态")
        try:
            file_path = f"task_states/{task_id}.json"
            if not os.path.exists(file_path):
                return {"error": f"找不到任务 {task_id} 的状态文件"}
                
            with open(file_path, 'r') as f:
                state = json.load(f)
                
            return state
        except Exception as e:
            return {"error": f"加载任务状态失败：{str(e)}"}

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
    
    def get_state(self) -> Dict:
        """获取Agent当前状态"""
        return {
            "name": self.name,
            "system_message": self.system_message,
            "message_history": self.message_history
        }
    
    def load_state(self, state: Dict) -> None:
        """加载Agent状态"""
        self.name = state.get("name", self.name)
        self.system_message = state.get("system_message", self.system_message)
        self.message_history = state.get("message_history", [])

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

# 任务状态管理
class TaskManager:
    @staticmethod
    def generate_task_id() -> str:
        """生成唯一的任务ID"""
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    @staticmethod
    def save_task(team_name: str, goal: str, current_step: int, steps: List[Dict], results: List[Dict]) -> str:
        """保存任务状态"""
        task_id = TaskManager.generate_task_id()
        state = {
            "team_name": team_name,
            "goal": goal,
            "current_step": current_step,
            "steps": steps,
            "results": results
        }
        
        save_result = Tools.save_task_state(task_id, state)
        if "失败" in save_result:
            print(f"任务保存失败：{save_result}")
            return None
            
        print(f"任务已成功保存，任务ID：{task_id}")
        return task_id
    
    @staticmethod
    def save_task_with_id(task_id: str, team_name: str, goal: str, current_step: int, steps: List[Dict], results: List[Dict]) -> str:
        """使用指定的任务ID保存任务状态"""
        state = {
            "team_name": team_name,
            "goal": goal,
            "current_step": current_step,
            "steps": steps,
            "results": results
        }
        
        save_result = Tools.save_task_state(task_id, state)
        if "失败" in save_result:
            print(f"任务保存失败：{save_result}")
            return None
            
        print(f"任务已成功保存，任务ID：{task_id}")
        return task_id
    
    @staticmethod
    def load_task(task_id: str) -> Dict:
        """加载任务状态"""
        return Tools.load_task_state(task_id)
    
    @staticmethod
    def list_tasks() -> List[str]:
        """列出所有保存的任务ID"""
        if not os.path.exists("task_states"):
            return []
            
        return [f.replace(".json", "") for f in os.listdir("task_states") if f.endswith(".json")]
    
    @staticmethod
    def find_incomplete_task(team_name: str, goal: str) -> Optional[str]:
        """查找团队未完成的相同目标任务"""
        task_ids = TaskManager.list_tasks()
        for task_id in task_ids:
            task_state = TaskManager.load_task(task_id)
            if "error" in task_state:
                continue
                
            if (task_state.get("team_name") == team_name and 
                task_state.get("goal") == goal and 
                task_state.get("current_step", 0) < len(task_state.get("steps", []))):
                return task_id
                
        return None

# PlanAgent - 任务规划与分解
class PlanAgent(Agent):
    def __init__(self):
        super().__init__(
            name="任务规划师",
            system_message=(
                "你是一个聪明的任务规划师，擅长把复杂的任务变成简单的小步骤！🧩"
                "你会用小朋友们能理解的语言，帮助他们规划一天的活动。"
                "你喜欢用有趣的比喻和例子，让规划变得超级简单！"
                "对于学习任务，保持步骤简洁明了。"
                "当被要求制定计划时，总是返回至少一个步骤。"
            )
        )
    
    def create_plan(self, goal: str, available_agents: List[Agent]) -> List[Dict]:
        """创建任务执行计划"""
        # 针对常见学习任务的硬编码优化
        if "学习加减法" in goal:
            return [
                {
                    "agent": "数学小博士",
                    "task": "用生活中的例子教小朋友学习加减法，如：3+2=?, 5-1=?"
                }
            ]
        elif "学习天气" in goal:
            return [
                {
                    "agent": "天气小精灵",
                    "task": "用简单易懂的语言教小朋友认识不同的天气类型"
                }
            ]
        elif "讲故事" in goal or "故事" in goal:
            return [
                {
                    "agent": "故事魔法师",
                    "task": "创作一个有趣的故事，主题可以是动物、太空或冒险"
                }
            ]
        
        # 生成工具列表描述
        tools_description = "\n".join([
            f"{agent.name}: {agent.system_message.split('.')[0]}"
            for agent in available_agents
        ])
        
        user_input = f"请为以下目标制定一个执行计划：{goal}\n可用工具：{tools_description}"
        response = self.run(user_input)
        
        # 增强型计划解析逻辑
        try:
            # 尝试解析JSON格式的计划
            plan = json.loads(response)
            if not isinstance(plan, list) or len(plan) == 0:
                raise ValueError("计划为空")
            return plan
        except:
            # 如果不是JSON格式，进行更健壮的文本解析
            plan_steps = []
            
            # 检查是否有步骤编号（如1. 2. 等）
            if any(f"{i}." in response for i in range(1, 10)):
                lines = response.split("\n")
                current_step = None
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 检查是否是步骤编号
                    for i in range(1, 10):
                        if line.startswith(f"{i}."):
                            step_text = line[2:].strip()
                            # 尝试从步骤文本中提取agent和任务
                            if "：" in step_text:
                                agent_name, task = step_text.split("：", 1)
                                plan_steps.append({
                                    "agent": agent_name.strip(),
                                    "task": task.strip()
                                })
                            else:
                                # 如果没有明确的分隔符，尝试根据agent名称猜测
                                for agent in available_agents:
                                    if agent.name in step_text:
                                        agent_name = agent.name
                                        task = step_text.replace(agent_name, "").strip()
                                        plan_steps.append({
                                            "agent": agent_name,
                                            "task": task
                                        })
                                        break
                                else:
                                    # 默认使用第一个agent
                                    plan_steps.append({
                                        "agent": available_agents[0].name,
                                        "task": step_text
                                    })
                            current_step = i
                            break
            else:
                # 如果没有步骤编号，尝试基于agent名称拆分
                agent_names = [agent.name for agent in available_agents]
                for agent_name in agent_names:
                    if agent_name in response:
                        parts = response.split(agent_name)
                        for i in range(1, len(parts)):
                            task = parts[i].strip()
                            if task and not task.startswith(":"):
                                task = f":{task}"
                            task = task.lstrip(":").strip()
                            if task:
                                plan_steps.append({
                                    "agent": agent_name,
                                    "task": task
                                })
            
            # 如果解析失败，创建一个默认步骤
            if not plan_steps:
                # 选择最相关的agent
                relevant_agent = None
                if "数学" in goal or "加减法" in goal or "计算" in goal:
                    relevant_agent = next((agent for agent in available_agents if agent.name == "数学小博士"), None)
                elif "天气" in goal:
                    relevant_agent = next((agent for agent in available_agents if agent.name == "天气小精灵"), None)
                elif "故事" in goal or "兴趣" in goal:
                    relevant_agent = next((agent for agent in available_agents if agent.name == "小花"), None)
                
                if not relevant_agent:
                    relevant_agent = available_agents[0]
                
                plan_steps.append({
                    "agent": relevant_agent.name,
                    "task": f"处理任务：{goal}"
                })
            
            return plan_steps

# 团队基类
class Team:
    def __init__(self, name: str, agents: List[Agent]):
        self.name = name
        self.agents = agents
        self.agent_map = {agent.name: agent for agent in agents}
        self.plan_agent = PlanAgent()
        self.current_task_id = None
    
    def create_task(self, goal: str, task_id: Optional[str] = None) -> str:
        """仅创建任务，不执行任何步骤"""
        print(f"团队 {self.name} 接到新任务：{goal}")
        
        # 查找是否有未完成的相同任务
        existing_task_id = TaskManager.find_incomplete_task(self.name, goal)
        if existing_task_id:
            print(f"发现未完成的相同任务，任务ID：{existing_task_id}")
            return existing_task_id
            
        # 制定计划
        steps = self.plan_agent.create_plan(goal, self.agents)
        
        # 如果计划仍然为空，创建一个默认步骤
        if not steps:
            steps = [
                {
                    "agent": self.agents[0].name,
                    "task": f"处理任务：{goal}"
                }
            ]
            
        print(f"制定的计划：{json.dumps(steps, indent=2)}")
        
        # 保存任务状态
        if task_id:
            # 使用指定的任务ID
            task_id = TaskManager.save_task_with_id(
                task_id=task_id,
                team_name=self.name,
                goal=goal,
                current_step=0,
                steps=steps,
                results=[]
            )
        else:
            # 生成新的任务ID
            task_id = TaskManager.save_task(
                team_name=self.name,
                goal=goal,
                current_step=0,
                steps=steps,
                results=[]
            )
        
        self.current_task_id = task_id
        return task_id
    
    def execute_task(self, goal: str, task_id: Optional[str] = None, reuse_existing: bool = True) -> str:
        """执行团队任务，可以选择加载已保存的任务状态"""
        # 查找是否有未完成的相同任务
        if reuse_existing and not task_id:
            existing_task_id = TaskManager.find_incomplete_task(self.name, goal)
            if existing_task_id:
                print(f"发现未完成的相同任务，任务ID：{existing_task_id}")
                task_id = existing_task_id
        
        if task_id:
            # 加载已保存的任务
            task_state = TaskManager.load_task(task_id)
            
            if "error" in task_state:
                return f"加载任务失败：{task_state['error']}"
                
            current_step = task_state.get("current_step", 0)
            steps = task_state.get("steps", [])
            results = task_state.get("results", [])
            print(f"加载任务 {task_id}，从步骤 {current_step+1}/{len(steps)} 继续")
            self.current_task_id = task_id
        else:
            # 创建新任务
            print(f"团队 {self.name} 接到新任务：{goal}")
            
            # 制定计划
            steps = self.plan_agent.create_plan(goal, self.agents)
            
            # 如果计划仍然为空，创建一个默认步骤
            if not steps:
                steps = [
                    {
                        "agent": self.agents[0].name,
                        "task": f"尝试处理任务：{goal}"
                    }
                ]
            
            print(f"制定的计划：{json.dumps(steps, indent=2)}")
            
            current_step = 0
            results = []
            self.current_task_id = None
        
        # 执行剩余步骤
        if not steps:
            return "任务计划为空，无法执行"
            
        for i in range(current_step, len(steps)):
            step = steps[i]
            agent_name = step.get("agent")
            task = step.get("task")
            
            # 执行任务前保存状态
            if not self.current_task_id:
                self.current_task_id = TaskManager.save_task(
                    team_name=self.name,
                    goal=goal,
                    current_step=i,
                    steps=steps,
                    results=results
                )
            else:
                TaskManager.save_task(
                    team_name=self.name,
                    goal=goal,
                    current_step=i,
                    steps=steps,
                    results=results
                )
            
            if not self.current_task_id:
                return "任务保存失败，无法继续执行"
                
            if agent_name in self.agent_map:
                agent = self.agent_map[agent_name]
                print(f"由 {agent_name} 执行步骤 {i+1}/{len(steps)}：{task}")
                result = agent.run(task)
                results.append({
                    "agent": agent_name,
                    "task": task,
                    "result": result
                })
                print(f"步骤 {i+1}/{len(steps)} 完成")
            else:
                results.append({
                    "agent": agent_name,
                    "task": task,
                    "result": f"错误：找不到名为 {agent_name} 的Agent"
                })
                print(f"步骤 {i+1}/{len(steps)} 失败")
        
        # 任务完成后再次保存状态
        final_task_id = TaskManager.save_task(
            team_name=self.name,
            goal=goal,
            current_step=len(steps),
            steps=steps,
            results=results
        )
        
        self.current_task_id = final_task_id
        
        # 汇总结果
        final_result = "\n\n".join([
            f"{result['agent']} 完成任务：{result['task']}\n结果：{result['result']}"
            for result in results
        ])
        
        final_result += f"\n\n任务已完成！任务ID：{final_task_id}"
        return final_result

# RobinGroup团队
class RobinGroup(Team):
    def __init__(self, name: str, agents: List[Agent]):
        super().__init__(name, agents)

# SelectGroup团队 - 旅行计划助手
class SelectGroup(Team):
    def __init__(self):
        # 创建团队成员
        travel_planner = Agent(
            name="旅行规划师",
            system_message=(
                "你是一个专业的旅行规划师，喜欢帮助小朋友们规划有趣的旅行！✈️"
                "你会根据小朋友的兴趣和预算，推荐合适的旅行地点和活动。"
                "你喜欢用旅行相关的表情符号，比如🗺️、🏖️、🚂、🌄。"
            ),
            tools=[
                Tools.search_kids_info,
                Tools.get_weather
            ]
        )
        
        budget_calculator = Agent(
            name="预算小管家",
            system_message=(
                "你是一个聪明的预算小管家，擅长帮助小朋友们管理旅行预算！💰"
                "你会用简单的数学计算，告诉小朋友们旅行需要花多少钱，怎么合理分配。"
                "你喜欢用金钱相关的表情符号，比如💵、💴、💶、💷。"
            ),
            tools=[
                Tools.calculate
            ]
        )
        
        story_teller = Agent(
            name="旅行故事家",
            system_message=(
                "你是一个富有想象力的旅行故事家，擅长根据旅行经历创作有趣的故事！📚"
                "你会用小朋友们喜欢的语言，把旅行中的点点滴滴变成精彩的故事。"
                "你喜欢用冒险相关的表情符号，比如🌍、🚀、🏕️、🌟。"
            ),
            tools=[
                Tools.generate_story
            ]
        )
        
        super().__init__(
            name="旅行小助手",
            agents=[travel_planner, budget_calculator, story_teller]
        )

# 创建一个专注于儿童学习的RobinGroup团队
learning_team = RobinGroup(
    name="超级学习小队",
    agents=[
        little_girl_agent,
        weather_agent,
        math_agent
    ]
)

# 创建旅行计划助手团队
travel_team = SelectGroup()

# 主交互界面
def main():
    print("\n欢迎来到儿童AI乐园！🎡")
    print("=" * 50)
    
    # 可用的Agents和Teams
    agents_and_teams = {
        "小花": little_girl_agent,
        "天气小精灵": weather_agent,
        "数学小博士": math_agent,
        "故事魔法师": story_agent,
        "时间小管家": time_agent,
        "超级学习小队": learning_team,
        "旅行小助手": travel_team
    }
    
    # 团队名称列表
    team_names = ["超级学习小队", "旅行小助手"]
    
    while True:
        print("\n你想进行什么操作呢？")
        print("1. 与Agent/Team聊天")
        print("2. 创建新任务（仅生成ID）")
        print("3. 执行已有任务")
        print("4. 列出所有保存的任务")
        print("0. 离开儿童AI乐园")
        
        main_choice = input("\n请选择一个编号：")
        
        if main_choice == "0":
            print("再见啦！希望你今天过得开心！✨")
            break
            
        elif main_choice == "1":
            print("\n你想和谁聊天呢？")
            for i, name in enumerate(agents_and_teams.keys(), 1):
                print(f"{i}. {name}")
            print("0. 返回主菜单")
            
            choice = input("\n请选择一个编号：")
            
            if choice == "0":
                continue
                
            if choice.isdigit() and 1 <= int(choice) <= len(agents_and_teams):
                name = list(agents_and_teams.keys())[int(choice) - 1]
                agent_or_team = agents_and_teams[name]
                
                print(f"\n=== 开始和 {name} 聊天啦！===")
                
                # 根据是否是团队来显示不同的提示
                if name in team_names:
                    print("输入 '再见' 结束聊天")
                    print("输入 '保存任务' 保存当前任务状态")
                    
                    goal = input(f"\n请告诉 {name} 你想完成的任务：")
                    task_id = None
                    
                    while True:
                        if goal.lower() == "再见":
                            print(f"{name} 说：再见啦！下次再一起玩哦！👋")
                            break
                        
                        if goal.lower() == "保存任务":
                            if hasattr(agent_or_team, 'current_task_id') and agent_or_team.current_task_id:
                                print(f"任务已保存，任务ID：{agent_or_team.current_task_id}")
                            else:
                                print("当前没有可保存的任务")
                            goal = input(f"\n请告诉 {name} 你想完成的任务：")
                            continue
                        
                        result = agent_or_team.execute_task(goal)
                        print(f"\n{name} 的回复：")
                        print(result)
                        
                        # 从结果中提取任务ID
                        lines = result.split('\n')
                        for line in reversed(lines):
                            if "任务ID" in line:
                                task_id = line.split("：")[-1].strip()
                                break
                        
                        goal = input(f"\n请告诉 {name} 你想完成的任务（或输入'再见'结束）：")
                else:
                    print("输入 '再见' 结束聊天")
                    
                    while True:
                        user_input = input(f"\n你对 {name} 说：")
                        
                        if user_input.lower() == "再见":
                            print(f"{name} 说：再见啦！下次再一起玩哦！👋")
                            break
                        
                        response = agent_or_team.run(user_input)
                        print(f"\n{name} 说：{response}")
            else:
                print("请输入正确的编号哦！")
                
        elif main_choice == "2":
            print("\n你想让哪个团队创建任务？")
            for i, name in enumerate(team_names, 1):
                print(f"{i}. {name}")
            print("0. 返回主菜单")
            
            team_choice = input("\n请选择一个编号：")
            
            if team_choice == "0":
                continue
                
            if team_choice.isdigit() and 1 <= int(team_choice) <= len(team_names):
                team_name = team_names[int(team_choice) - 1]
                team = agents_and_teams[team_name]
                
                goal = input(f"\n请输入任务目标：")
                
                # 可选：指定任务ID
                use_custom_id = input("是否使用自定义任务ID？(y/n)：").lower()
                if use_custom_id == "y":
                    task_id = input("请输入任务ID：")
                    task_id = team.create_task(goal, task_id)
                else:
                    task_id = team.create_task(goal)
                
                if task_id:
                    print(f"任务已成功创建，任务ID：{task_id}")
                else:
                    print("任务创建失败")
            else:
                print("请输入正确的编号哦！")
                
        elif main_choice == "3":
            task_id = input("\n请输入任务ID：")
            if not task_id:
                print("任务ID不能为空！")
                continue
                
            # 尝试获取任务信息
            task_state = TaskManager.load_task(task_id)
            if "error" in task_state:
                print(f"加载任务失败：{task_state['error']}")
                continue
                
            team_name = task_state.get("team_name")
            goal = task_state.get("goal")
            
            if team_name not in agents_and_teams:
                print(f"找不到团队：{team_name}")
                continue
                
            team = agents_and_teams[team_name]
            
            print(f"\n=== 加载任务 ===")
            print(f"团队：{team_name}")
            print(f"任务目标：{goal}")
            print(f"任务ID：{task_id}")
            
            result = team.execute_task(goal, task_id)
            print(f"\n{team_name} 的回复：")
            print(result)
            
        elif main_choice == "4":
            print("\n所有保存的任务：")
            task_ids = TaskManager.list_tasks()
            if not task_ids:
                print("没有找到保存的任务")
                continue
                
            for i, task_id in enumerate(task_ids, 1):
                task_state = TaskManager.load_task(task_id)
                if "error" in task_state:
                    print(f"{i}. {task_id} (加载失败)")
                else:
                    team_name = task_state.get("team_name", "未知团队")
                    goal = task_state.get("goal", "未知目标")
                    status = "已完成" if task_state.get("current_step", 0) >= len(task_state.get("steps", [])) else "进行中"
                    print(f"{i}. {task_id} - {team_name} - {goal} ({status})")
        else:
            print("请输入正确的编号哦！")

if __name__ == "__main__":
    main()