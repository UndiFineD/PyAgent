# Extracted from: C:\DEV\PyAgent\.external\skills\skills\jacobzwj\bilibili-hot-monitor\generate_report.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站热门视频日报生成器

获取热门视频列表，调用 B站 AI 总结 API，通过 OpenRouter 调用第三方 LLM 生成点评。

使用方法：
    python generate_report.py --sessdata "xxx" --openrouter-key "xxx" --model "google/gemini-2.0-flash-001" --output report.md
"""

import argparse
import datetime
import io
import json
import sys
import time
from pathlib import Path

import requests

# 修复 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 导入本地模块
from bilibili_api import BilibiliAPI, format_duration, format_number, format_timestamp


def call_openrouter(api_key: str, model: str, prompt: str) -> str:
    """
    调用 OpenRouter API 生成内容

    Args:
        api_key: OpenRouter API Key
        model: 模型名称，如 "anthropic/claude-sonnet-4.5"
        prompt: 提示词

    Returns:
        生成的文本
    """
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
            },
            timeout=30,
        )

        if response.status_code != 200:
            print(f"  [WARNING] OpenRouter API 错误: {response.status_code}")
            return ""

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"  [WARNING] OpenRouter 调用失败: {e}")
        return ""


def generate_ai_comment(api_key: str, model: str, video_info: dict) -> tuple[str, str]:
    """
    使用 OpenRouter LLM 生成 AI 点评和运营爆款分析

    Args:
        api_key: OpenRouter API Key
        model: 模型名称
        video_info: 视频信息字典

    Returns:
        (ai_comment, viral_analysis) 元组
    """
    title = video_info["title"]
    stat = video_info["stat"]
    ai_summary = video_info.get("ai_summary", "")
    like_rate = video_info.get("like_rate", 0)

    prompt = f"""你是一位B站内容分析专家。请根据以下视频信息，生成两段简短的分析：

视频标题：{title}
播放量：{format_number(stat['view'])}
点赞数：{format_number(stat['like'])}
收藏数：{format_number(stat['favorite'])}
硬币数：{format_number(stat['coin'])}
弹幕数：{stat['danmaku']:,}
评论数：{stat['reply']:,}
分享数：{stat['share']:,}
点赞率：{like_rate:.1f}%
B站AI总结：{ai_summary if ai_summary else '暂无'}

请生成：
1. **AI点评**（1-2句话，分析视频为何受欢迎，内容特点，或值得关注的地方）
2. **运营爆款分析**（使用固定格式：**爆款因素**：xxx **数据亮点**：xxx **成功关键**：xxx）

要求：
- 语言简洁有力，像专业的内容运营分析
- 每个部分不超过50字
- 直接输出内容，不要加额外的标题或序号

输出格式（严格遵守）：
AI点评：[你的点评内容]
运营分析：**爆款因素**：[内容] **数据亮点**：[内容] **成功关键**：[内容]"""

    # 调用 OpenRouter API
    result = call_openrouter(api_key, model, prompt)

    if not result:
        return "", ""

    # 解析结果
    ai_comment = ""
    viral_analysis = ""

    lines = result.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 匹配 AI点评
        if "AI点评" in line:
            parts = line.split("：", 1) if "：" in line else line.split(":", 1)
            if len(parts) > 1:
                ai_comment = parts[1].strip()
        # 匹配运营分析
        elif "运营分析" in line or "**爆款因素**" in line:
            if "：" in line:
                parts = line.split("：", 1)
                viral_analysis = parts[1].strip() if len(parts) > 1 else line
            elif ":" in line:
                parts = line.split(":", 1)
                viral_analysis = parts[1].strip() if len(parts) > 1 else line
            else:
                viral_analysis = line.strip()

    # 如果解析失败，尝试直接使用整个返回作为点评
    if not ai_comment and not viral_analysis and result:
        ai_comment = result.split("\n")[0][:100] if result else ""

    return ai_comment, viral_analysis


def _generate_data_analysis(vd):
    """根据视频数据自动生成数据分析"""
    stat = vd["stat"]
    like_rate = vd.get("like_rate", 0)

    analysis = []

    # 播放量分析
    views = stat["view"]
    if views >= 1000000:
        analysis.append(f"播放量{views // 10000}万，现象级热度")
    elif views >= 500000:
        analysis.append(f"播放量{views // 10000}万+，热度极高")
    elif views >= 100000:
        analysis.append(f"播放量{views // 10000}万+")
    else:
        analysis.append(f"播放量{views:,}")

    # 点赞率分析
    if like_rate >= 20:
        analysis.append(f"点赞率{like_rate:.0f}%（极高）")
    elif like_rate >= 10:
        analysis.append(f"点赞率{like_rate:.0f}%（优秀）")
    elif like_rate >= 5:
        analysis.append(f"点赞率{like_rate:.0f}%")

    # 硬币点赞比
    coin_like_ratio = stat["coin"] / stat["like"] * 100 if stat["like"] > 0 else 0
    if coin_like_ratio >= 50:
        analysis.append(f"硬币点赞比{coin_like_ratio:.0f}%（高投币意愿）")

    # 互动数据
    if stat["reply"] >= 1000:
        analysis.append(f"评论{stat['reply']}条（热议）")
    if stat["danmaku"] >= 1000:
        analysis.append(f"弹幕{stat['danmaku']:,}条")

    return "；".join(analysis[:4])


def _get_video_tag(vd):
    """根据视频内容生成标签"""
    title = vd["title"].lower()
    duration = vd["duration"]

    if duration < 60:
        return "超短视频"
    elif duration > 30 * 60:
        return "长视频深度内容"
    elif "说唱" in title or "rap" in title:
        return "说唱音乐"
    elif "游戏" in title or "原神" in title or "鸣潮" in title:
        return "游戏相关"
    elif "舞" in title or "跳" in title:
        return "舞蹈"
    elif "吃" in title or "美食" in title:
        return "美食"
    elif "vlog" in title or "日常" in title:
        return "生活记录"
    else:
        return "热门内容"


def generate_report(
    api: BilibiliAPI,
    num_videos: int = 20,
    delay: float = 1.0,
    openrouter_key: str = "",
    model: str = "google/gemini-2.5-flash-preview",
) -> str:
    """
    生成热门视频报告
    """
    print(f"正在获取热门视频列表...")
    videos = api.get_popular_videos(page_size=num_videos)
    print(f"获取到 {len(videos)} 个热门视频")

    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    # 第一遍：收集所有数据并计算统计
    video_data_list = []
    total_views = 0
    max_views_idx, max_views = 0, 0
    max_likes_idx, max_likes = 0, 0
    max_coins_idx, max_coins = 0, 0
    max_shares_idx, max_shares = 0, 0

    for i, video in enumerate(videos, 1):
        bvid = video["bvid"]
        title = video["title"]
        owner = video["owner"]
        stat = video["stat"]
        desc = video.get("desc", "")
        duration = video.get("duration", 0)
        pubdate = video.get("pubdate", 0)

        print(f"[{i}/{len(videos)}] 处理: {title[:30]}...")

        # 统计
        total_views += stat["view"]
        if stat["view"] > max_views:
            max_views = stat["view"]
            max_views_idx = i
        if stat["like"] > max_likes:
            max_likes = stat["like"]
            max_likes_idx = i
        if stat["coin"] > max_coins:
            max_coins = stat["coin"]
            max_coins_idx = i
        if stat["share"] > max_shares:
            max_shares = stat["share"]
            max_shares_idx = i

        # 获取 AI 总结（增加延迟避免触发速率限制）
        ai_summary = None
        ai_outline = []
        try:
            time.sleep(1.0)  # AI 总结 API 请求前等待 1 秒
            summary_data = api.get_ai_summary(
                bvid=bvid, cid=video.get("cid", 0), up_mid=owner["mid"]
            )
            if summary_data:
                model_result = summary_data.get("model_result")
                result_type = (
                    model_result.get("result_type", -1) if model_result else -1
                )
                # result_type: 0=无AI总结, 1=有AI总结, 2=有AI总结（另一种格式）
                if model_result and result_type in [1, 2]:
                    ai_summary = model_result.get("summary", "")
                    ai_outline = model_result.get("outline", [])
        except Exception as e:
            print(f"  [WARNING] 获取 AI 总结失败: {e}")

        like_rate = stat["like"] / stat["view"] * 100 if stat["view"] > 0 else 0

        video_data_list.append(
            {
                "idx": i,
                "bvid": bvid,
                "title": title,
                "owner": owner,
                "stat": stat,
                "desc": desc,
                "duration": duration,
                "pubdate": pubdate,
                "ai_summary": ai_summary,
                "ai_outline": ai_outline,
                "like_rate": like_rate,
            }
        )

        if i < len(videos):
            time.sleep(delay)

    # 为最高数据添加亮点标签
    for vd in video_data_list:
        highlights = []
        if vd["idx"] == max_views_idx:
            highlights.append("🔥播放量最高")
        if vd["idx"] == max_likes_idx:
            highlights.append("🔥点赞最高")
        if vd["idx"] == max_coins_idx and max_coins_idx not in [
            max_views_idx,
            max_likes_idx,
        ]:
            highlights.append("🔥硬币最高")
        if vd["idx"] == max_shares_idx and max_shares_idx not in [
            max_views_idx,
            max_likes_idx,
        ]:
            highlights.append("🔥分享最高")
        if vd["like_rate"] > 15:
            highlights.append(f"点赞率{vd['like_rate']:.0f}%")
        vd["highlight"] = " ".join(highlights) if highlights else _get_video_tag(vd)

    # 生成 AI 点评（使用 OpenRouter）
    if openrouter_key:
        print(f"\n正在使用 {model} 生成 AI 点评...")
        for vd in video_data_list:
            print(
                f"  [{vd['idx']}/{len(video_data_list)}] 生成点评: {vd['title'][:20]}..."
            )
            ai_comment, viral_analysis = generate_ai_comment(openrouter_key, model, vd)
            vd["ai_comment"] = ai_comment
            vd["viral_analysis"] = viral_analysis
            time.sleep(0.5)  # 避免 API 限流

    # 生成报告
    report_lines = [
        "# B站热门视频日报",
        "",
        f"**生成时间**：{now.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        f"## 📋 本期热门视频（{today_str}）",
        "",
        "| 排名 | 视频标题 | 播放量 | 亮点 | 链接 |",
        "|------|----------|--------|------|------|",
    ]

    # 摘要表格（标题中的 | 需要转义，避免破坏表格结构）
    for vd in video_data_list:
        link = f"https://www.bilibili.com/video/{vd['bvid']}"
        safe_title = vd["title"].replace("|", "｜")  # 替换为全角竖线
        safe_highlight = vd["highlight"].replace("|", "｜")
        report_lines.append(
            f"| {vd['idx']} | {safe_title} | {format_number(vd['stat']['view'])} | {safe_highlight} | [打开视频]({link}) |"
        )

    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 本期亮点
    report_lines.append("## 🌟 本期亮点")
    report_lines.append("")
    max_views_video = video_data_list[max_views_idx - 1]
    max_likes_video = video_data_list[max_likes_idx - 1]
    max_coins_video = video_data_list[max_coins_idx - 1]
    max_shares_video = video_data_list[max_shares_idx - 1]

    report_lines.append(
        f"1. **播放量冠军**：《{max_views_video['title']}》{format_number(max_views_video['stat']['view'])}"
    )
    report_lines.append(
        f"2. **点赞数冠军**：《{max_likes_video['title']}》{format_number(max_likes_video['stat']['like'])}"
    )
    report_lines.append(
        f"3. **硬币数冠军**：《{max_coins_video['title']}》{format_number(max_coins_video['stat']['coin'])}"
    )
    report_lines.append(
        f"4. **分享数冠军**：《{max_shares_video['title']}》{max_shares_video['stat']['share']:,}"
    )
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 详细报告
    for vd in video_data_list:
        report_lines.append(f"## {vd['idx']}. {vd['title']}")
        report_lines.append("")

        # 基本信息
        report_lines.append(f"- **UP主**：{vd['owner']['name']}")
        report_lines.append(
            f"- **时长**：{format_duration(vd['duration'])} | **发布时间**：{format_timestamp(vd['pubdate'])}"
        )
        report_lines.append("")

        # 数据统计
        report_lines.append("**📊 数据统计**：")
        report_lines.append(
            f"> 播放 {format_number(vd['stat']['view'])} | 点赞 {format_number(vd['stat']['like'])} | 收藏 {format_number(vd['stat']['favorite'])} | 硬币 {format_number(vd['stat']['coin'])} | 弹幕 {vd['stat']['danmaku']:,} | 评论 {vd['stat']['reply']:,} | 分享 {vd['stat']['share']:,}"
        )
        report_lines.append("")

        # 数据分析（自动生成）
        data_analysis = _generate_data_analysis(vd)
        report_lines.append("**📈 数据分析**：")
        report_lines.append(f"> {data_analysis}")
        report_lines.append("")

        # 视频简介
        if vd["desc"] and vd["desc"].strip() and vd["desc"].strip() != "-":
            desc_clean = vd["desc"][:500].replace("\n", " ").replace("\r", " ")
            desc_clean = " ".join(desc_clean.split())
            report_lines.append("**📝 视频简介**：")
            report_lines.append(
                f"> {desc_clean}{'...' if len(vd['desc']) > 500 else ''}"
            )
            report_lines.append("")

        # B站官方 AI 总结
        if vd["ai_summary"]:
            report_lines.append("**🤖 B站官方AI总结**：")
            report_lines.append(f"> {vd['ai_summary']}")

            if vd["ai_outline"]:
                report_lines.append(">")
                report_lines.append("> **内容大纲**：")
                for item in vd["ai_outline"][:3]:
                    outline_title = item.get("title", "")
                    outline_content = item.get("part_outline", [])
                    if outline_title:
                        report_lines.append(f"> • **{outline_title}**")
                        for part in outline_content[:2]:
                            content = part.get("content", "")
                            if content:
                                report_lines.append(f">   - {content}")
            report_lines.append("")
        else:
            report_lines.append("**🤖 B站官方AI总结**：")
            report_lines.append("> （该视频暂无官方AI总结）")
            report_lines.append("")

        # AI 点评
        ai_comment = vd.get("ai_comment", "")
        report_lines.append("**💡 AI点评**：")
        if ai_comment:
            report_lines.append(f"> {ai_comment}")
        else:
            report_lines.append("> （需要提供 API Key 生成）")
        report_lines.append("")

        # 运营爆款分析
        viral_analysis = vd.get("viral_analysis", "")
        report_lines.append("**🚀 运营爆款分析**：")
        if viral_analysis:
            report_lines.append(f"> {viral_analysis}")
        else:
            report_lines.append("> （需要提供 API Key 生成）")
        report_lines.append("")

        # 视频链接
        report_lines.append(
            f"🔗 [点击观看视频](https://www.bilibili.com/video/{vd['bvid']})"
        )
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

    # 底部统计
    report_lines.append("## 📊 本期数据概览")
    report_lines.append("")
    report_lines.append("| 指标 | 数值 |")
    report_lines.append("|------|------|")
    report_lines.append(f"| 视频总数 | {len(videos)} |")
    report_lines.append(f"| 总播放量 | {format_number(total_views)} |")
    report_lines.append(
        f"| 最高播放 | 《{max_views_video['title'][:20].replace('|', '｜')}...》{format_number(max_views_video['stat']['view'])} |"
    )
    report_lines.append(
        f"| 最高点赞 | 《{max_likes_video['title'][:20].replace('|', '｜')}...》{format_number(max_likes_video['stat']['like'])} |"
    )
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("*报告由 B站 API + OpenRouter AI 自动生成*")

    return "\n".join(report_lines)


def parse_cookies(cookies_str: str) -> dict:
    """
    解析完整的 cookies 字符串
    格式：key1=value1; key2=value2; ...
    """
    result = {}
    for item in cookies_str.split(";"):
        item = item.strip()
        if "=" in item:
            key, value = item.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def load_config(config_path: str) -> dict:
    """加载 JSON 配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="B站热门视频日报生成器")

    # 配置文件（推荐）
    parser.add_argument("--config", "-c", help="配置文件路径（推荐，配置一次永久使用）")

    # 或者单独指定参数
    parser.add_argument("--cookies", help="完整的B站cookies字符串")
    parser.add_argument(
        "--sessdata", default="", help="SESSDATA cookie（如果不用--cookies）"
    )
    parser.add_argument("--bili-jct", default="", help="bili_jct cookie")
    parser.add_argument("--buvid3", default="", help="buvid3 cookie")
    parser.add_argument("--dedeuserid", default="", help="DedeUserID cookie")
    parser.add_argument("--num-videos", type=int, default=20, help="获取视频数量")
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="请求间隔（秒），建议 >= 1.0 避免触发B站速率限制",
    )
    parser.add_argument("--output", "-o", help="输出文件路径")

    # AI 点评相关参数
    parser.add_argument(
        "--openrouter-key", default="", help="OpenRouter API Key（用于生成 AI 点评）"
    )
    parser.add_argument(
        "--model",
        default="",
        help="OpenRouter 模型名称（默认从配置文件读取，或 google/gemini-2.5-flash-preview）",
    )

    args = parser.parse_args()

    # 从配置文件或命令行参数获取配置
    config = {}
    if args.config:
        print(f"正在读取配置文件: {args.config}")
        config = load_config(args.config)

    # 解析 cookies（优先使用配置文件）
    cookies_str = args.cookies or config.get("bilibili", {}).get("cookies", "")
    all_cookies = None
    if cookies_str:
        all_cookies = parse_cookies(cookies_str)
        sessdata = all_cookies.get("SESSDATA", "")
        bili_jct = all_cookies.get("bili_jct", "")
        buvid3 = all_cookies.get("buvid3", "")
        dedeuserid = all_cookies.get("DedeUserID", "")
    else:
        sessdata = args.sessdata
        bili_jct = args.bili_jct
        buvid3 = args.buvid3
        dedeuserid = args.dedeuserid

    if not sessdata:
        print("错误：必须提供 --config、--cookies 或 --sessdata 参数")
        sys.exit(1)

    # AI 配置（优先使用命令行参数，其次配置文件）
    ai_config = config.get("ai", {})
    openrouter_key = args.openrouter_key or ai_config.get("openrouter_key", "")
    model = args.model or ai_config.get("model", "google/gemini-2.5-flash-preview")

    # 创建 API 客户端（传入所有 cookies 以确保完整性）
    api = BilibiliAPI(
        sessdata=sessdata,
        bili_jct=bili_jct,
        buvid3=buvid3,
        dedeuserid=dedeuserid,
        all_cookies=all_cookies,
    )

    # 报告配置
    report_config = config.get("report", {})
    num_videos = args.num_videos or report_config.get("num_videos", 10)

    # 生成报告
    try:
        report = generate_report(
            api=api,
            num_videos=num_videos,
            delay=args.delay,
            openrouter_key=openrouter_key,
            model=model,
        )
    except Exception as e:
        print(f"[ERROR] 生成报告失败: {e}")
        sys.exit(1)

    # 输出
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"\n[SUCCESS] 报告已保存到: {output_path}")
    else:
        print("\n" + "=" * 50)
        print(report)


if __name__ == "__main__":
    main()
