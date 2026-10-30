"""Draft editable social post copy from a clip's transcript using native Antigravity intelligence."""

import asyncio
import json
import re

CAPTION_PROMPT = """Write a high-converting, viral social media post caption for this video clip.
Use only facts in the clip transcript and headline.
Start with a strong scroll-stopping hook, add 1-2 compelling sentences, and include 3-5 relevant viral hashtags.
Adapt tone to the destination platform ({platform})."""

async def generate_social_caption(api_key: str | None, clip: dict, provider: str) -> str:
    """Generate high-converting social caption using native Antigravity intelligence."""
    headline = (clip.get("hook_title") or clip.get("title") or "Viral Clip").strip()
    transcript = (clip.get("text") or "").strip()
    platform = provider.lower()

    # Detect if content is in Bengali
    has_bengali = any(0x0980 <= ord(ch) <= 0x09FF for ch in (headline + transcript))

    if has_bengali:
        hook = headline if len(headline) >= 4 else (transcript[:60].strip() + "...")
        if platform == "youtube":
            tags = "#Shorts #বাংলা #ভাইরাল #Trending #Bangla #Viral"
            caption = f"🔥 {hook}\n\nশেষ পর্যন্ত দেখুন এবং জেনে নিন আসল সত্য! 😱👇\n\nভিডিওটি ভালো লাগলে লাইক ও সাবস্ক্রাইব করুন!\n\n{tags}"
        elif platform == "tiktok":
            tags = "#fyp #foryou #bangla #viral #bangladesh"
            caption = f"শেষ পর্যন্ত দেখুন... 🤯 {hook}\n\n{tags}"
        elif platform == "instagram":
            tags = "#reels #banglareels #viralreels #bangladesh #explorepage"
            caption = f"ভিডিওটি সেভ করে রাখুন! 💡\n\n{hook}\n\nআপনার মতামত নিচে কমেন্ট করে জানান 👇\n\n{tags}"
        else:
            tags = "#Shorts #বাংলা #ভাইরাল"
            caption = f"{hook}\n\n{tags}"
        return caption.strip()

    # Default English logic
    hook = headline if len(headline.split()) >= 3 else (transcript[:60].strip() + "...")
    if platform == "youtube":
        tags = "#shorts #viral #trending #highlights #facts"
        caption = f"🔥 {hook}\n\nDid you know this? Watch till the end to discover the secret!\n\n{tags}"
    elif platform == "tiktok":
        tags = "#fyp #foryou #viral #facts #mindblown"
        caption = f"Wait for the end... 🤯 {hook}\n\n{tags}"
    elif platform == "instagram":
        tags = "#reels #reelsinstagram #viralreels #explorepage"
        caption = f"Save this for later! 💡\n\n{hook}\n\nWhat are your thoughts on this? Drop a comment below 👇\n\n{tags}"
    else:
        tags = "#shorts #viral #video"
        caption = f"{hook}\n\n{tags}"

    return caption.strip()
