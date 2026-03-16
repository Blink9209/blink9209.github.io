#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日技术博客自动生成脚本
功能：
1. AI 生成技术知识内容
2. 抓取技术 RSS 资讯
3. 生成 Markdown 博客文章
"""

import os
import json
import datetime
import subprocess
from pathlib import Path

# 获取项目根目录
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# 配置
CONFIG = {
    "rss_feeds": [
        "https://news.ycombinator.com/rss",
        "https://dev.to/feed",
    ],
    "ai_topics": [
        "Python 编程技巧",
        "JavaScript 最佳实践",
        "数据结构与算法",
        "系统设计",
        "AI/机器学习基础",
    ],
    "content_sources": {
        "ai": True,
        "rss": True,
        "notes": True
    }
}

def get_date():
    """获取当前日期"""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_datetime():
    """获取当前日期时间"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_ai_content():
    """生成 AI 内容 - 占位符，实际运行时会调用 OpenAI API"""
    topics = CONFIG["ai_topics"]
    import random
    topic = random.choice(topics)
    
    content = f"""## 🤖 今日技术知识

### {topic}

**概念解释：**
{topic} 是现代软件开发中非常重要的知识点。掌握这项技术可以提升你的编程能力和代码质量。

**实际应用：**
在实际项目中，{topic} 常常被用于解决复杂的业务问题。建议通过实践来加深理解。

**学习建议：**
1. 阅读官方文档
2. 查看开源项目源码
3. 动手实践小项目

> 💡 提示：持续学习是成为优秀开发者的关键！
"""
    return content

def fetch_rss_content():
    """抓取 RSS 内容 - 占位符"""
    content = """## 📰 热门技术资讯

### Hacker News 热门

1. **[技术趋势] AI 编程助手的最新发展**
   - 摘要：探讨 AI 编程工具如何改变开发者的工作方式
   - 来源：Hacker News

2. **[开源动态] 2024 年最受欢迎的开源项目**
   - 摘要：盘点过去一年开源社区的重要贡献
   - 来源：Dev.to

3. **[学习资源] 免费编程学习资源大全**
   - 摘要：整理全网优质的免费编程教程
   - 来源：Hacker News
"""
    return content

def generate_notes_content():
    """生成学习笔记内容"""
    content = """## 📝 今日学习笔记

### 今日总结

今天是充实的一天！继续深入学习技术知识，保持每日进步。

**今日收获：**
- 了解了更多技术细节
- 动手实践了代码示例
- 解决了实际问题

**明日计划：**
- 继续学习新技术
- 整理学习笔记
- 参与技术社区讨论
"""
    return content

def create_blog_post():
    """创建博客文章"""
    date = get_date()
    datetime_str = get_datetime()
    
    # 构建文章内容
    content = f"""---
layout: post
title: "每日技术简报 - {date}"
date: {datetime_str}
categories: [技术, 每日更新]
tags: [学习笔记, 技术分享, AI]
---

# 🚀 每日技术简报 - {date}

欢迎来到 Blink9209 的每日技术博客！每天为你带来精选的技术知识和资讯。

---

"""
    
    # 添加各个部分
    if CONFIG["content_sources"]["ai"]:
        content += generate_ai_content() + "\n\n"
    
    if CONFIG["content_sources"]["rss"]:
        content += fetch_rss_content() + "\n\n"
    
    if CONFIG["content_sources"]["notes"]:
        content += generate_notes_content() + "\n\n"
    
    # 添加页脚
    content += """---

## 📢 说明

- 🤖 AI 内容由自动化系统生成
- 📰 资讯来源于 RSS 订阅源
- 📝 笔记为每日学习总结

---
*由自动化系统发布*
"""
    
    return content

def save_post(content):
    """保存博客文章"""
    date = get_date()
    filename = f"_posts/{date}-daily-tech.md"
    filepath = PROJECT_ROOT / filename
    
    # 确保目录存在
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 博客文章已生成: {filepath}")
    return filename

def git_commit_push(filename):
    """提交并推送文章"""
    try:
        # 配置 Git 用户
        subprocess.run(['git', 'config', '--global', 'user.name', 'Blink9209'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'chenwj9209@163.com'], check=True)
        
        # 添加文件
        subprocess.run(['git', 'add', filename], check=True)
        
        # 检查是否有更改
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not result.stdout.strip():
            print("📝 没有新内容需要提交")
            return True
        
        # 提交
        commit_message = f"Auto-publish daily post: {get_date()}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        print("✅ 文章已提交到本地!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始生成每日技术博客...")
    
    # 创建博客内容
    content = create_blog_post()
    
    # 保存文章
    filename = save_post(content)
    
    # 提交推送
    git_commit_push(filename)
    
    print("✨ 每日技术博客发布完成!")

if __name__ == "__main__":
    main()
