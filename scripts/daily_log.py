#!/usr/bin/env python3
"""
daily_log.py - Automated Daily Learning Logger for GitHub Contribution Streak.

Usage:
    python scripts/daily_log.py --topic "Multi-Agent Reflection Loops" --summary "Implemented custom critique node with LangGraph."
    python scripts/daily_log.py   (prompts interactively)
"""

import argparse
from datetime import datetime
from pathlib import Path

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "knowledge-hub" / "daily-journal"

def log_entry(topic: str, summary: str, tags: list[str] | None = None) -> Path:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now()
    year_month = today.strftime("%Y-%m")
    date_str = today.strftime("%Y-%m-%d")
    
    file_path = JOURNAL_DIR / f"{year_month}.md"
    
    tags_formatted = " ".join([f"`#{t.strip()}`" for t in (tags or ["AI", "Engineering", "DailyStreak"])])
    
    entry_content = f"""
### 📅 {date_str}: {topic}

- **Topic**: {topic}
- **Timestamp**: {today.strftime("%Y-%m-%d %H:%M:%S")}
- **Tags**: {tags_formatted}
- **Summary**:
  {summary.strip()}

---
"""
    
    if not file_path.exists():
        header = f"# 📖 Daily Learning Journal — {year_month}\n\nContinuous daily logs of AI breakthroughs, algorithms, and engineering notes.\n\n---\n"
        file_path.write_text(header + entry_content, encoding="utf-8")
    else:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry_content)
            
    print(f"✅ Successfully logged entry for {date_str} in {file_path}")
    return file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log daily learning entry.")
    parser.add_argument("--topic", type=str, help="Title of topic learned or implemented today")
    parser.add_argument("--summary", type=str, help="Bullet points or summary of the day's engineering work")
    parser.add_argument("--tags", type=str, help="Comma-separated tags (e.g. LLM,RAG,Python)")
    
    args = parser.parse_args()
    
    topic = args.topic or "Autonomous Multi-Agent Routing & Quantized Inference"
    summary = args.summary or "Explored StateGraph conditional transitions, evaluated QLoRA rank tradeoffs, and established daily open-source contribution workflow."
    tag_list = [t.strip() for t in args.tags.split(",")] if args.tags else ["GenerativeAI", "LangGraph", "QLoRA", "OpenSource"]
    
    log_entry(topic, summary, tag_list)
