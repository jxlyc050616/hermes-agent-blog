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
    """将 Markdown 转为微信公众号兼容的移动端 HTML"""
    import re

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
    raw = markdown.markdown(md_content, extensions=extensions)

    # ── 微信公众平台移动端适配 ────────────────────
    # WeChat 会剥离 <style> 和外链 CSS，所以所有样式必须 inline
    # WeChat 移动端 WebView 对 overflow 支持不稳定，需要用 div 包裹

    # 容器：整体 padding + 字体基础（容器本身也要 overflow 兜底）
    wrap = '<section style="padding: 8px 14px; font-size: 17px; line-height: 1.75; color: #333; max-width: 100%; overflow: auto; word-wrap: break-word;">'

    # 处理标题：h1/h2/h3 + 内联样式
    raw = re.sub(
        r'<h(\d)([^>]*)>(.*?)</h\1>',
        lambda m: {
            1: f'<h1 style="font-size: 22px; font-weight: 700; color: #1a1a1a; margin: 24px 0 12px; padding: 0 0 8px; border-bottom: 2px solid #3866FF;">{m.group(3)}</h1>',
            2: f'<h2 style="font-size: 19px; font-weight: 700; color: #1a1a1a; margin: 20px 0 10px; padding-left: 10px; border-left: 3px solid #3866FF;">{m.group(3)}</h2>',
            3: f'<h3 style="font-size: 17px; font-weight: 700; color: #333; margin: 16px 0 8px;">{m.group(3)}</h3>',
        }.get(int(m.group(1)), m.group(0)),
        raw,
    )

    # 段落 + 内联样式
    raw = re.sub(
        r'<p>(.*?)</p>',
        r'<p style="margin: 10px 0; font-size: 17px; line-height: 1.75; color: #333;">\1</p>',
        raw,
        flags=re.DOTALL,
    )

    # ── 行内代码：先处理（独立 <code>，不在 <pre> 内的）────
    # 先用占位符保护 <pre> 内的 <code>
    PRE_MARKER = "║║║PREBLOCK║║║"
    pre_blocks = []
    
    def _save_pre(m):
        pre_blocks.append(m.group(0))
        return f"{PRE_MARKER}{len(pre_blocks)-1}{PRE_MARKER}"
    
    raw = re.sub(r'<pre>.*?</pre>', _save_pre, raw, flags=re.DOTALL)
    
    # 现在所有 <code> 都是行内代码
    raw = re.sub(
        r'<code>(.*?)</code>',
        r'<code style="background: #f0f2f5; color: #d63384; border-radius: 3px; padding: 2px 6px; font-size: 15px; font-family: Menlo, Consolas, monospace;">\1</code>',
        raw,
    )
    
    # ── 代码块：还原并加上双层可滚动结构 ────────
    # WeChat 移动版经常忽略 <pre> 上的 overflow-x，用外层 <div> 兜底
    for i, block in enumerate(pre_blocks):
        # 去掉 <pre> 和 </pre> 标签，取中间内容
        inner = re.sub(r'^<pre[^>]*>(.*)</pre>$', r'\1', block, flags=re.DOTALL)
        wrapped = (
            '<div style="overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch; '
            'margin: 12px 0; border-radius: 6px; max-width: 100%;">'
            '<pre style="background: #1e1e1e; color: #d4d4d4; padding: 14px; '
            'font-size: 13px; line-height: 1.45; white-space: pre; '
            'font-family: Menlo, Consolas, Courier, monospace; margin: 0; '
            'min-width: min-content;">'
            f'{inner}'
            '</pre>'
            '</div>'
        )
        raw = raw.replace(f"{PRE_MARKER}{i}{PRE_MARKER}", wrapped)

    # 表格：响应式 + 边线 + 斑马纹
    raw = re.sub(
        r'<table>',
        r'<div style="overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 12px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 15px; white-space: nowrap;">',
        raw,
    )
    raw = re.sub(r'</table>', r'</table></div>', raw)
    raw = re.sub(
        r'<th>',
        r'<th style="background: #3866FF; color: #fff; padding: 8px 10px; border: 1px solid #ddd; text-align: left; font-weight: 600;">',
        raw,
    )
    raw = re.sub(
        r'<td>',
        r'<td style="padding: 8px 10px; border: 1px solid #ddd;">',
        raw,
    )

    # 引用块：左侧蓝条
    raw = re.sub(
        r'<blockquote>(.*?)</blockquote>',
        r'<blockquote style="margin: 14px 0; padding: 12px 16px; background: #f5f7fa; border-left: 4px solid #3866FF; color: #555; font-size: 15px; line-height: 1.7; border-radius: 0 4px 4px 0;">\1</blockquote>',
        raw,
        flags=re.DOTALL,
    )

    # 无序/有序列表：WeChat 丢弃默认 list-style，必须显式声明
    raw = re.sub(
        r'<ul>',
        r'<ul style="margin: 8px 0; padding-left: 28px; font-size: 17px; line-height: 1.75; list-style-type: disc; list-style-position: outside;">',
        raw,
    )
    raw = re.sub(
        r'<ol>',
        r'<ol style="margin: 8px 0; padding-left: 30px; font-size: 17px; line-height: 1.75; list-style-type: decimal; list-style-position: outside;">',
        raw,
    )
    raw = re.sub(
        r'<li>(.*?)</li>',
        r'<li style="margin: 4px 0; color: #333;">\1</li>',
        raw,
    )

    # 粗体
    raw = re.sub(
        r'<strong>(.*?)</strong>',
        r'<strong style="font-weight: 700; color: #1a1a1a;">\1</strong>',
        raw,
    )

    # 图片：自适应 + 圆角
    raw = re.sub(
        r'<img([^>]*)>',
        r'<img\1 style="max-width: 100%; height: auto; border-radius: 6px; margin: 12px 0; display: block;">',
        raw,
    )

    # 水平线
    raw = re.sub(
        r'<hr\s*/>',
        r'<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">',
        raw,
    )

    return wrap + raw + "</section>"


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
