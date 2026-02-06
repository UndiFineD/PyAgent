# Extracted from: C:\DEV\PyAgent\.external\skills\skills\ty-teo\patent-assistant\scripts\patent_search.py
#!/usr/bin/env python3
"""
专利检索工具 - 使用 Google Patents 进行专利检索
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from typing import Optional


def search_google_patents(
    query: str, limit: int = 20, country: str = "CN"
) -> list[dict]:
    """
    使用 Google Patents 搜索专利

    Args:
        query: 搜索关键词
        limit: 返回结果数量
        country: 国家代码 (CN=中国, US=美国, EP=欧洲)

    Returns:
        专利列表
    """
    # 构建搜索 URL
    encoded_query = urllib.parse.quote(f"{query} country:{country}")
    url = (
        f"https://patents.google.com/xhr/query?url=q%3D{encoded_query}&num={limit}&exp="
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        results = []
        if "results" in data and "cluster" in data["results"]:
            for cluster in data["results"]["cluster"]:
                if "result" in cluster:
                    for result in cluster["result"]:
                        patent = result.get("patent", {})
                        results.append(
                            {
                                "patent_number": patent.get("publication_number", ""),
                                "title": patent.get("title", ""),
                                "abstract": (
                                    patent.get("abstract", "")[:500]
                                    if patent.get("abstract")
                                    else ""
                                ),
                                "assignee": patent.get("assignee", ""),
                                "filing_date": patent.get("filing_date", ""),
                                "url": f"https://patents.google.com/patent/{patent.get('publication_number', '')}",
                            }
                        )
        return results[:limit]

    except Exception as e:
        print(f"Google Patents 搜索失败: {e}", file=sys.stderr)
        return []


def search_cnipa_web(query: str, limit: int = 20) -> list[dict]:
    """
    搜索国知局专利（通过网页接口）

    注意：国知局官方 API 需要申请，这里使用公开网页接口
    """
    # 国知局公开检索接口
    encoded_query = urllib.parse.quote(query)
    url = f"https://pss-system.cponline.cnipa.gov.cn/conventionalSearch/portal/search?searchType=1&searchWord={encoded_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            # 国知局需要登录，这里返回提示
            return [
                {
                    "note": "国知局检索需要登录账号",
                    "url": url,
                    "suggestion": "请手动访问上述链接进行检索，或使用 Google Patents",
                }
            ]
    except Exception as e:
        return [
            {
                "note": f"国知局检索失败: {e}",
                "url": url,
                "suggestion": "请手动访问链接或使用 Google Patents",
            }
        ]


def analyze_similarity(query: str, patents: list[dict]) -> list[dict]:
    """
    简单的相似度分析（基于关键词匹配）
    """
    keywords = set(query.lower().split())

    for patent in patents:
        title = patent.get("title", "").lower()
        abstract = patent.get("abstract", "").lower()
        content = f"{title} {abstract}"

        # 计算关键词匹配度
        matched = sum(1 for kw in keywords if kw in content)
        patent["similarity_score"] = (
            round(matched / len(keywords) * 100, 1) if keywords else 0
        )

    # 按相似度排序
    return sorted(patents, key=lambda x: x.get("similarity_score", 0), reverse=True)


def format_output(patents: list[dict], format_type: str = "text") -> str:
    """格式化输出"""
    if format_type == "json":
        return json.dumps(patents, ensure_ascii=False, indent=2)

    if not patents:
        return "未找到相关专利"

    lines = ["## 专利检索结果\n"]

    for i, p in enumerate(patents, 1):
        if "note" in p:
            lines.append(f"**提示**: {p['note']}")
            lines.append(f"链接: {p.get('url', '')}")
            lines.append(f"建议: {p.get('suggestion', '')}")
            continue

        lines.append(f"### {i}. {p.get('title', '无标题')}")
        lines.append(f"- **专利号**: {p.get('patent_number', 'N/A')}")
        lines.append(f"- **申请人**: {p.get('assignee', 'N/A')}")
        lines.append(f"- **申请日**: {p.get('filing_date', 'N/A')}")
        if "similarity_score" in p:
            lines.append(f"- **相似度**: {p['similarity_score']}%")
        lines.append(f"- **链接**: {p.get('url', '')}")
        if p.get("abstract"):
            lines.append(f"- **摘要**: {p['abstract'][:200]}...")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="专利检索工具")
    parser.add_argument("query", help="检索关键词")
    parser.add_argument("--limit", "-n", type=int, default=20, help="返回结果数量")
    parser.add_argument(
        "--country", "-c", default="CN", help="国家代码 (CN/US/EP/JP/KR)"
    )
    parser.add_argument(
        "--source",
        "-s",
        choices=["google", "cnipa", "all"],
        default="google",
        help="数据源",
    )
    parser.add_argument(
        "--format", "-f", choices=["text", "json"], default="text", help="输出格式"
    )
    parser.add_argument("--analyze", "-a", action="store_true", help="进行相似度分析")

    args = parser.parse_args()

    all_results = []

    if args.source in ["google", "all"]:
        print(f"正在搜索 Google Patents: {args.query}", file=sys.stderr)
        results = search_google_patents(args.query, args.limit, args.country)
        all_results.extend(results)

    if args.source in ["cnipa", "all"]:
        print(f"正在搜索国知局: {args.query}", file=sys.stderr)
        results = search_cnipa_web(args.query, args.limit)
        all_results.extend(results)

    if args.analyze and all_results:
        all_results = analyze_similarity(args.query, all_results)

    print(format_output(all_results, args.format))


if __name__ == "__main__":
    main()
