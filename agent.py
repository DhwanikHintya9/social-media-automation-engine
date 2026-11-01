import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from anthropic import Anthropic
import requests

def load_env_file():
    env_path = Path(__file__).with_name(".env")
    if not env_path.is_file():
        return

    for line_number, line in enumerate(env_path.read_text(encoding="utf-8").splitlines(), start=1):
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue

        key, separator, value = entry.partition("=")
        key = key.strip()
        if not separator or not key:
            raise ValueError(f"Invalid .env entry on line {line_number}.")

        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        os.environ.setdefault(key, value)


load_env_file()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise RuntimeError("Set ANTHROPIC_API_KEY in .env or the environment.")

client = Anthropic(api_key=api_key)

class InstagramStructuredBulkAgent:
    def __init__(self, niche: str, target_audience: str):
        self.niche = niche
        self.target_audience = target_audience

    def _extract_text_safely(self, message) -> str:
        """Isolates raw text across SDK streaming block formats."""
        if hasattr(message, 'content') and isinstance(message.content, list):
            text_pieces = []
            for block in message.content:
                if hasattr(block, 'text'):
                    text_pieces.append(block.text)
                elif isinstance(block, dict) and 'text' in block:
                    text_pieces.append(block['text'])
            return "".join(text_pieces)
        return str(message)

    def skill_brainstorm_topics(self, num_topics: int = 5) -> list:
        """Brainstorms unique topics using a strict list extraction prompt."""
        prompt = f"""Niche: {self.niche}
Audience: {self.target_audience}
Generate a list of {num_topics} unique viral Instagram Reel topics targeting major bottlenecks.
Output format: Return ONLY a plain text list with one topic per line. Do not number them or add symbols."""
        
        message = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = self._extract_text_safely(message).strip()
        # Split text lines safely into a clean Python array list
        return [line.strip() for line in raw_text.split('\n') if line.strip()]

    def skill_generate_complete_post(self, topic: str) -> dict:
        """Generates full post package using strict object delimiter isolation."""
        prompt = f"""Act as an Instagram Growth Expert.
Niche: {self.niche}
Audience: {self.target_audience}
Topic: {topic}

Build a comprehensive Instagram content pack. You must structure your output using these exact delimiter tags below. 
Do not include any other conversational filler text or markdown wrappers.

[HOOKS]
Provide 3 distinct hook options, one per line.
[BODY]
Provide a highly readable, bulleted caption body with clean line breaks.
[CTA]
Provide a single strong call-to-action line.
[HASHTAGS]
Provide 5-7 space-separated hashtags.
[STORYBOARD]
Provide 5 sequential frames. Use this exact format for each frame line:
Frame X: [Text Overlay] -> Visual Action Scene Description (Audio direction)"""

        message = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        return self._parse_delimited_output(self._extract_text_safely(message))

    def _parse_delimited_output(self, text: str) -> dict:
        """Parses custom delimiter blocks safely without JSON string decoding vulnerabilities."""
        sections = {"hooks": "", "body": "", "cta": "", "hashtags": "", "storyboard": ""}
        current_key = None
        
        lines = text.split('\n')
        for line in lines:
            cleaned = line.strip()
            if cleaned == "[HOOKS]": current_key = "hooks"
            elif cleaned == "[BODY]": current_key = "body"
            elif cleaned == "[CTA]": current_key = "cta"
            elif cleaned == "[HASHTAGS]": current_key = "hashtags"
            elif cleaned == "[STORYBOARD]": current_key = "storyboard"
            elif current_key:
                if sections[current_key]:
                    sections[current_key] += "\n" + line
                else:
                    sections[current_key] = line
                    
        # Structure payload strings matching original pipeline expectation
        hooks_formatted = "\n".join([f"🪝 {h.strip()}" for h in sections["hooks"].split('\n') if h.strip()])
        final_caption = f"{hooks_formatted}\n\n{sections['body'].strip()}\n\n{sections['cta'].strip()}\n\n{sections['hashtags'].strip()}"
        
        return {
            "final_caption": final_caption,
            "storyboard_notes": sections["storyboard"].strip()
        }

    def execute_dynamic_pipeline(self, num_posts: int, starting_days_out: int, webhook_url: str):
        topics = self.skill_brainstorm_topics(num_topics=num_posts)
        print(f"🧠 Generated {len(topics)} Unique Topics dynamically.")

        print(f"🚀 Processing Token-Optimized Delimiter Pipeline...\n")
        for index, topic in enumerate(topics):
            if index >= num_posts: break
            scheduled_date = (datetime.now() + timedelta(days=starting_days_out + index)).strftime("%Y-%m-%d 10:00:00")
            print(f"🎬 Building Post {index + 1}/{len(topics)}: '{topic}'")
            
            try:
                # Executes cleanly without JSON vulnerabilities
                post_data = self.skill_generate_complete_post(topic)
                
                payload = {
                    "scheduled_time": scheduled_date,
                    "topic": topic,
                    "final_caption": post_data["final_caption"],
                    "storyboard_notes": post_data["storyboard_notes"]
                }
                
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 200:
                    print(f"   ✅ Row added to Google Sheets!")
                else:
                    print(f"   ❌ Webhook Failed: {response.status_code}")
                
            except Exception as e:
                print(f"   ❌ Execution error: {str(e)}")
            
            time.sleep(2.0)
        print("\n🏆 Production run complete! Open your Google Sheets Content Bank to see the new batch.")

# --- System Run Configuration ---
if __name__ == "__main__":
    agent = InstagramStructuredBulkAgent(
        niche="AI Tools & Productivity for Solopreneurs", 
        target_audience="Busy founders looking to automate repetitive tasks"
    )
    
    MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")
    if not MAKE_WEBHOOK_URL:
        raise RuntimeError("Set MAKE_WEBHOOK_URL in .env or the environment.")
    
    agent.execute_dynamic_pipeline(
        num_posts=5,
        starting_days_out=2,
        webhook_url=MAKE_WEBHOOK_URL
    )
