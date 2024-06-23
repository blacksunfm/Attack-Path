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
# 3 WebSurferAgent所需环境变量（可不设置，要体验此Agent相关功能时会报错）
export BING_API_KEY=<bing_api_key>
```

## 单个agent测试

实际操作浏览器的agent, 这个需要额外安装一些依赖

```shell
pip install -r package_source/webarena/requirements.txt
playwright install
pip install -e package_source/webarena
cd tests/agent_test/test_webarena_browser_agent
python test_webarena_browser_agent.py
```

其他agent都是进入该测试目录直接执行就行<br/>
例如代码执行agent

```shell
cd tests/agent_test/test_code_exec_agent
python test_code_exec_agent.py
```

(由于版本更新，rag_assistant似乎不能用了，所有用到rag的agent都收到影响，正在重构中)

## benchmark测试

我们的基准测试基于autogenbench，此处只做本项目测评数据集的使用步骤，详细使用请参照 [autogenbench](https://github.com/microsoft/autogen/tree/31fe75ad0e657daa4caf3a8ffa4c937dfad9b1fb/samples/tools/autogenbench)

1. 安装相关库, 下面两条命令任选一个执行

   a. 安装官方最新版本，此版本构建的docker预装库较少，运行任务会根据agent框架的requirements.txt再去下载相关依赖
   ```shell
   pip install autogenbench==0.0.3
   ```
   b. 安装0.0.2a3版本，此版本构建的docker比较大，已安装好相关依赖
   ```shell
   pip install autogenbench==0.0.2a3
   ```

2. **如果是Windows系统，请确保"docker+WSL环境"已安装**（linux系统可跳过这一步），安装参考 https://www.docker.com/products/docker-desktop/ 

3. 进入要测试的数据集文件夹

   ```shell
   cd tests/benchmark_test/CTFAIA
   ```

4. 运行初始化脚本 init_tasks.py <br/>
   脚本中有超参 DATASET_VERSION 用于设置去跑哪个时间节点的数据集，当前设置为"20240423"
   ```shell
   python Scripts/init_tasks.py
   ```

5. 运行一个任务，此处以**使用BasicTwoAgents测试20240423数据集test集合level1难度**的任务为例

   a. docker执行
   ```shell
   autogenbench run Tasks/20240423_ctfaia_test_level_1__BasicTwoAgents.jsonl
   ```
   b. 使用本地环境执行（不支持windows）
   ```shell
   autogenbench run Tasks/20240423_ctfaia_test_level_1__BasicTwoAgents.jsonl --native
   ```

6. 本地输出任务的执行情况，并将结果输出到目标任务目录下的result.jsonl文件中，
result.json可以被提交到 [**[LeaderBoard]**](https://huggingface.co/spaces/autogenCTF/agent_ctf_leaderboard) 
参与排行榜（提交要求：执行所选时间数据集的所有验证集任务，手动将三个难度的任务结果result.jsonl放在同一个jsonl文件中提交）

   ```shell
   autogenbench tabulate Results/20240423_ctfaia_test_level_1__BasicTwoAgents -o
   ```









