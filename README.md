# Autonomous Multi-Topic Instagram Content Engine

An enterprise-grade, token-optimized, two-tier automation framework that connects a localized Python AI agent network to cloud databases and Meta's official API publishing grid. This system dynamically brainstorms viral content, builds structured multi-format copy blueprints, and handles conditional human-in-the-loop auto-publishing completely on autopilot.

---

## 1. System Architecture Blueprint

The ecosystem operates across two completely independent, non-blocking asynchronous data pipelines mediated by a centralized cloud relational content bank:

[ Local Execution Layer ]
│ (Executes agent.py)
▼
[ Claude Engine (claude-sonnet-5-5) ] ──> Dynamic Ideation & Copy Generation
│
│ (Structured Delimiter Payload via HTTP POST)
▼
[ Make.com Pipeline #1 ] ───> Custom Webhook Integration
│
▼
[ Google Sheets Content Bank ] <── [ Human-In-The-Loop Review Layer ]
│                                  (Drop Media URL & Flip Status to "Approved")
│ (Decoupled Hourly Scan Loop)
▼
[ Make.com Pipeline #2 ] ───> Conditional Filter Matching (Status == "Approved")
│
├───> [ Meta Graph API Platform ] ───> Direct Live Instagram Post
│
└───> [ Google Sheets Closure ] ───> Flips Row Status to "Published"


---

## 2. Full Project Implementation History (Step-by-Step Diary)

### Step 1: Initial Local Architecture Blueprint
- **Objective:** Establish a local AI script utilizing the official `anthropic` SDK to generate content frameworks (Hooks, Body, CTA, Hashtags, Visual Storyboards).
- **Hurdles & Bug Fixes:**
  - *TypeError:* Passing the `temperature` parameter inside `client.messages.create()` triggered structural errors due to local SDK version environments. Attempts to isolate it via `extra_body` threw `Extra inputs are not permitted` from server validation. 
  - *Resolution:* Completely removed the `temperature` configuration parameter. Claude automatically defaulted to a well-balanced text generation profile, rendering the script version-proof.

### Step 2: Authentication & Billing Tier Verification
- **Objective:** Validate connection to the Anthropic server API endpoints.
- **Hurdles & Bug Fixes:**
  - *TypeError (Authentication):* The script threw credential runtime flags because the local Windows system environment variable (`ANTHROPIC_API_KEY`) was missing.
  - *Resolution:* Switched from terminal variables to explicit instantiation in the code: `client = Anthropic(api_key="YOUR_ACTUAL_API_KEY")`.
  - *Current implementation update:* The explicit in-code key was an interim historical solution. The current `agent.py` reads `ANTHROPIC_API_KEY` from a local `.env` file or the process environment; see **Current Local Setup** below. Do not put a real API key in source code.
  - *BadRequestError (Error Code 400):* The server blocked requests with a balance warning: `Your credit balance is too low`.
  - *Resolution:* Added a $5 prepaid credit tier balance inside the online Anthropic Developer Console billing dashboard.

### Step 3: Model Alignment & SDK Token Extraction
- **Objective:** Target the high-performance Claude 3.5 Sonnet engine for advanced content generation.
- **Hurdles & Bug Fixes:**
  - *NotFoundError (Error Code 404):* Standard version naming conventions like `claude-3-5-sonnet-20241022` and `claude-3-5-sonnet-latest` returned not found exceptions due to unique workspace routing.
  - *Resolution:* Aligned the model parameters exactly to the verified billing tier point string: `"claude-sonnet-5-5"`.
  - *AttributeError:* The system crashed on text parsing because `message.content` returned a raw Python list array block instead of an accessible text field object.
  - *Resolution:* Implemented a deep block validator (`_extract_text_safely`) to securely map the internal data streams.

### Step 4: Eradicating JSON String Vulnerabilities
- **Objective:** Parse AI text natively into programmatic fields to send across webhooks.
- **Hurdles & Bug Fixes:**
  - *JSONDecodeError (Unterminated String):* Claude repeatedly injected standard multiline formatting breaks inside its text output strings. This instantly crashed `json.loads()`.
  - *Resolution:* Completely abandoned JSON formatting prompts for the heavy content blocks. Rebuilt the engine around an explicit, custom text-delimiter system (`[HOOKS]`, `[BODY]`, etc.) handled by a robust Python scanner (`_parse_delimited_output`).

### Step 5: Setting Up the Cloud Google Sheet
- **Objective:** Construct a centralized online relational content bank database.
- **Action Taken:** Created a spreadsheet named `Instagram Content Bank` directly inside Google Drive using the same Google profile authenticated in Make.com. Set up columns for `Topic`, `Scheduled Time`, `Final Caption`, `Storyboard Notes`, `Status`, and `Media URL`. Configured Column B under *Format > Number > Date time* to clean up raw serial calculation metrics.

### Step 6: Developing and Splitting the Make.com Pipelines
- **Objective:** Establish the cloud publishing execution pipelines.
- **Hurdles & Bug Fixes:**
  - *The Mega-Scenario Bug:* Initially tried linking Webhooks, Sheets, and Instagram into a single unified flowchart. This caused the system to hang infinitely because it tried posting to Instagram before a human could ever review the text or add an image URL.
  - *Resolution:* Permanently split the execution into two separate, independent scenarios:
    1. **Scenario 1:** Listens for the Python webhook and immediately logs drafts using `Google Sheets: Add a Row`.
    2. **Scenario 2:** Scans the sheet independently using `Search Rows` to process rows only when the status changes to `Approved`.

---

## 3. Technical Stack & Credentials

- **Execution Runtime:** Python 3.15+ (Local Machine Environment)
- **Core AI Engine:** Anthropic Messaging Protocol API (`claude-sonnet-5-5`)
- **Cloud Middleware Platform:** Make.com Visual Scenarios
- **Relational Data Tier:** Google Sheets API Cloud Ecosystem
- **Target Social Layer:** Meta Business Graph API Architecture (Instagram Business Profile verified via Facebook Page Administration)

---

## 4. Local Execution Engine (`agent.py`)

> **Historical code sample:** The listing below preserves an earlier implementation for project context. It does not reflect the current credential-loading setup and should not be copied as the current `agent.py`. For the current setup, follow **Current Local Setup** below.

```python
import os
import json
import time
from datetime import datetime, timedelta
from anthropic import Anthropic
import requests

# Initialize Claude natively
client = Anthropic(api_key="YOUR_ACTUAL_API_KEY_HERE")

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
        """Skill 1: Brainstorms unique topics using a strict list extraction prompt."""
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
        return [line.strip() for line in raw_text.split('\n') if line.strip()]

    def skill_generate_complete_post(self, topic: str) -> dict:
        """Skill 2 & 3: Unified Execution - Generates full post package using strict object delimiter isolation."""
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
if name == "main":
agent = InstagramStructuredBulkAgent(
niche="AI Tools & Productivity for Solopreneurs",
target_audience="Busy founders looking to automate repetitive tasks"
)
MAKE_WEBHOOK_URL = "PASTE_YOUR_COPIED_MAKE_WEBHOOK_URL_HERE"
agent.execute_dynamic_pipeline(
num_posts=5,
starting_days_out=2,
webhook_url=MAKE_WEBHOOK_URL
)
```


## 5. Cloud Automation Scenarios (Make.com)


Scenario 1: Local Ingestion Pipeline

• Topology: Custom Webhook ➔ Google Sheets: Add a Row
• Settings: Active 24/7. Maps incoming text properties (topic, scheduled_time, final_caption, storyboard_notes) directly into empty rows.

Scenario 2: Decoupled Auto-Publishing Queue

• Topology: Google Sheets: Search Rows ➔ Instagram Business: Create a Photo Post ➔ Google Sheets: Update a Row
• Settings: Set to run automatically on an hourly timer.
	• Search Rows Filter: Matches rows where Status is exactly equal to Approved, limited to 1 row at a time.
	• Instagram Post: Pulls the image asset file location path directly out of the user-filled Media URL column.
	• Update a Row Closure: Automatically updates that row's status to Published so it never repeats.

## 6. Current Local Setup

The current `agent.py` reads the Anthropic API key and Make.com webhook URL from a `.env` file located beside `agent.py`. It also accepts these values from process environment variables; an environment variable already set in the process takes precedence over the matching `.env` value.

1. Install Python and the project dependencies:

   ```powershell
   python -m pip install anthropic requests
   ```

2. Create a file named `.env` in the project folder, next to `agent.py`, with these entries:

   ```dotenv
   ANTHROPIC_API_KEY=your_anthropic_api_key
   MAKE_WEBHOOK_URL=https://hook.example.com/your-webhook
   ```

   Replace both example values with your own credentials. Do not add quotes unless they are part of the value. Treat the webhook URL as a secret as well.

3. Confirm `.gitignore` contains `.env`. This project ignores the local `.env` file so its credentials are not included in normal Git commits. Keep actual credentials out of tracked files and never commit or share the real `.env`.

4. Run the agent from the project folder:

   ```powershell
   python agent.py
   ```

The script generates topics and post content with Anthropic, then sends each post to the Make.com webhook. The Make.com scenarios and Google Sheet must be configured separately for ingestion, human review, and any Instagram publishing. If either required setting is missing, the script reports which variable needs to be configured.

If an API key was previously placed in source code or otherwise exposed, revoke it and create a replacement before running the agent.

***

<FollowUp>
This file gives any AI engine **full historical context** of your setup. Let me know if you would like me to show you how to **schedule the Python file to run automatically using Windows Task Scheduler** so you don't even have to open your terminal!
</FollowUp>