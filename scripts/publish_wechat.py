#!/usr/bin/env python3
"""
WeChat Official Article Publisher
将 Markdown 文章发布到微信公众号（草稿箱 → 发布）

用法：
  python3 publish_wechat.py \
    --appid YOUR_APPID \
    --appsecret YOUR_APPSECRET \
    --file article.md \
    --cover /path/to/cover.jpg
"""

import sys
import json
import time
import argparse
import requests
import markdown

API_BASE = "https://api.weixin.qq.com/cgi-bin"


def get_access_token(appid: str, secret: str) -> str:
    """Step 1: 获取 Access Token"""
    resp = requests.get(f"{API_BASE}/token", params={
        "grant_type": "client_credential",
        "appid": appid,
        "secret": secret,
    })
    data = resp.json()
    if "access_token" not in data:
        raise RuntimeError(f"获取 Token 失败: {data}")
    print(f"✅ 获取 Access Token 成功（有效期 7200秒）")
    return data["access_token"]


def upload_image(token: str, image_path: str) -> str:
    """上传封面图片到素材库，返回 media_id"""
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{API_BASE}/material/add_material?access_token={token}&type=image",
            files={"media": (image_path, f, "image/jpeg")}
        )
    data = resp.json()
    if "media_id" not in data:
        raise RuntimeError(f"上传图片失败: {data}")
    print(f"✅ 上传封面图片成功: {data['media_id']}")
    return data["media_id"]


def md_to_wechat_html(md_path: str) -> str:
    """将 Markdown 转为微信公众号兼容的 HTML"""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # 去掉 YAML frontmatter
    if md_content.startswith("---"):
        parts = md_content.split("---", 2)
        if len(parts) >= 3:
            md_content = parts[2].strip()
    
    # 用 markdown 库转换
    extensions = [
        "markdown.extensions.fenced_code",
        "markdown.extensions.codehilite",
        "markdown.extensions.tables",
        "markdown.extensions.toc",
    ]
    html = markdown.markdown(md_content, extensions=extensions)
    
    # 微信公众平台 HTML 兼容性处理
    # - 代码块用 <pre><code>
    # - 表格用标准 table 标签
    # - 避免使用微信不支持的 CSS
    return html


def add_draft(token: str, title: str, author: str, digest: str, 
              html_content: str, thumb_media_id: str, 
              source_url: str = "") -> str:
    """Step 2: 添加草稿到草稿箱"""
    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": html_content,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    if source_url:
        article["content_source_url"] = source_url
    
    resp = requests.post(
        f"{API_BASE}/draft/add?access_token={token}",
        json={"articles": [article]}
    )
    data = resp.json()
    if "media_id" not in data:
        raise RuntimeError(f"新增草稿失败: {data}")
    print(f"✅ 草稿创建成功: {data['media_id']}")
    return data["media_id"]


def submit_publish(token: str, media_id: str) -> str:
    """Step 3: 提交发布草稿"""
    resp = requests.post(
        f"{API_BASE}/freepublish/submit?access_token={token}",
        json={"media_id": media_id}
    )
    data = resp.json()
    if data.get("errcode", 0) != 0:
        raise RuntimeError(f"提交发布失败: {data}")
    publish_id = data.get("publish_id", "")
    print(f"✅ 已提交发布，publish_id: {publish_id}")
    return publish_id


def check_publish_status(token: str, publish_id: str) -> dict:
    """查询发布状态（可选）"""
    resp = requests.post(
        f"{API_BASE}/freepublish/get?access_token={token}",
        json={"publish_id": publish_id}
    )
    return resp.json()


def parse_frontmatter(md_path: str) -> dict:
    """简易 frontmatter 解析"""
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    meta = {"title": "", "author": "小糊涂虫", "description": ""}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip().lower()
                    val = val.strip().strip('"').strip("'")
                    if key in ("title", "author", "description"):
                        meta[key] = val
    return meta


def main():
    parser = argparse.ArgumentParser(description="发布 Markdown 文章到微信公众号")
    parser.add_argument("--appid", required=True, help="公众号 AppID")
    parser.add_argument("--appsecret", required=True, help="公众号 AppSecret")
    parser.add_argument("--file", required=True, help="Markdown 文章路径")
    parser.add_argument("--cover", required=True, help="封面图片路径")
    parser.add_argument("--publish", action="store_true", 
                       help="直接发布（默认只创建草稿）")
    args = parser.parse_args()
    
    # 解析 frontmatter
    meta = parse_frontmatter(args.file)
    title = meta["title"] or input("请输入文章标题: ")
    author = meta["author"] or "小糊涂虫"
    digest = meta.get("description", "") or title[:120]
    
    print(f"📄 文章: {title}")
    print(f"✍️  作者: {author}")
    
    # 获取 Token
    token = get_access_token(args.appid, args.appsecret)
    
    # 上传封面
    thumb_id = upload_image(token, args.cover)
    
    # Markdown → HTML
    html = md_to_wechat_html(args.file)
    
    # 创建草稿
    media_id = add_draft(token, title, author, digest, html, thumb_id)
    
    # 可选：直接发布
    if args.publish:
        publish_id = submit_publish(token, media_id)
        print(f"\n📢 发布任务已提交！publish_id: {publish_id}")
        print("   发布通常需要几秒到几分钟，可通过 publish_id 查询状态")
    else:
        print(f"\n📝 草稿已创建，请登录公众号后台手动发布")
        print(f"   或加 --publish 参数直接自动发布")


if __name__ == "__main__":
    main()
