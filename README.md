## 项目介绍
本项目旨在探索Agent在网络安全领域的实操能力，部署多代理协同执行攻击路径规划任务，对某一IP或某一网段进行潜在漏洞检测。


**你可以根据下面的教程进行项目的初体验**

# 快速体验

## 下载项目

```shell
git clone https://github.com/blacksunfm/Attack-Path.git
cd Attack-Path
```

## 基础库安装

运行在python3.10环境（可使用conda新建环境避免未知冲突）, 执行以下代码安装基本的依赖库

```shell
pip install -r requirements.txt
```

## 环境变量

使用下面的命令设置环境变量(bash)<br/>
其中"<...>"需要更换成自己的。如果是使用官网的openai_api_key则不需要设置<base_url><br/>
OAI_CONFIG_LIST文件里的内容需要更新成自己的配置。如果是使用官网的openai_api_key，请删掉<base_url>那几行

```shell
# 设置环境变量
# 1 LLM相关环境变量（如果是使用官网的openai_api_key则不需要设置<base_url>）
export OPENAI_API_KEY=<openai_api_key>
export BASE_URL=<base_url>
# 2 autogen所需环境变量，OAI_CONFIG_LIST为根目录下的一个文件，替换其内容中的"<...>"，替换后执行以下代码（如果是使用官网的openai_api_key，请删掉<base_url>那几行）
export OAI_CONFIG_LIST=$(cat ./OAI_CONFIG_LIST)
```

## 单个agent测试

所有单agent都是进入该测试目录直接执行就行<br/>
例如代码执行agent

```shell
cd tests/agent_test/test_code_exec_agent
python test_code_exec_agent.py
```







