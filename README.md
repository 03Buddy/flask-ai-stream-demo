Flask AI 流式问答Demo

基于Flask + DeepSeek API实现文本流式问答AI应用，线上可访问Demo



1\. 整体架构说明

三层极简架构：

1\. 前端层：原生HTML页面，提供输入框展示流式实时回复

2\. 服务层：Flask后端，提供页面路由 / 和流式接口 /stream

3\. AI调用层：请求DeepSeek大模型开放API，采用SSE服务端推送实现打字机效果

业务流程：用户输入文本 → POST提交至后端流式接口 → 后端封装请求调用LLM → 逐token流式返回前端渲染



2\. 关键Prompt与设计思路

基础Prompt



Vibe设计思路

轻量化文本处理工具，主打低延迟实时流式输出，无复杂RAG/多智能体，聚焦基础文本问答场景，快速验证大模型API调用流程，适合AI Agent入门演示。



3\. AI调用逻辑

1\. 传输方案：SSE(Server-Sent Events)流式传输，实时推送模型输出，避免等待完整响应

2\. API封装：统一请求头鉴权，固定模型参数temperature=0.7平衡创意与准确性

3\. 数据处理：迭代解析接口返回流，提取delta增量文本逐字下发前端

4\. 异常兼容：流结束标识\[DONE]自动终止连接，前端分段解析JSON避免报错

5\. 拓展预留：可快速新增Function Calling工具调用、多轮对话上下文缓存



4\. 完整部署步骤（含HTTPS、域名说明）

本地测试部署

1\. 安装依赖

bash

pip install -r requirements.txt

