import sys
import os
import json
import time
import random
import getpass
import http.client

CONFIG_FILE = "config.json"
MESSAGES_FILE = "messages.txt"
TOKEN_ENV_VAR = "DISCORD_TOKEN"
ENV_FILE = ".env"

# Windows consoles often default to cp1252, which cannot encode emoji or
#unicode names and would crash output mid-run (even misreporting sends as
# failures). Force UTF-8 with replacement on both streams.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def load_env_file(path=ENV_FILE):
    """Load KEY=VALUE pairs from a .env file into os.environ.
    Existing environment variables are never overridden. Lines starting
    with # are comments. Values may be quoted with single or double quotes."""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except FileNotFoundError:
        pass

def resolve_token(config):
    """Resolve the token: environment variable first, stored config as fallback.
    Avoids keeping the secret in a plaintext file when DISCORD_TOKEN is set."""
    env_token = os.environ.get(TOKEN_ENV_VAR, "").strip()
    if env_token:
        return env_token
    return config.get("token", "")

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def configure_settings(mode="all"):
    config = load_config()
    print(f"\n--- Configuration Setup [{mode.upper()}] ---")
    
    if mode in ["all", "auth"]:
        print(f"(Tip: set the {TOKEN_ENV_VAR} environment variable instead of storing it in {CONFIG_FILE})")
        entered = getpass.getpass("Discord Token [Press Enter to keep current]: ").strip()
        if entered:
            config["token"] = entered
        config["user_agent"] = input("User Agent [Press Enter for default]: ").strip() or config.get(
            "user_agent", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

    if mode in ["all", "channel"]:
        config["channel_id"] = input("Discord Channel ID: ").strip() or config.get("channel_id", "")
        config["channel_url"] = input("Discord Channel URL (Referer): ").strip() or config.get("channel_url", "")

    save_config(config)
    print("Configuration updated successfully!\n")

def get_message_list():
    try:
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                return lines
    except FileNotFoundError:
        pass

    openers = [
        "yo", "gm", "wait lowkey", "ngl", "real talk", "no way", "i swear",
        "honest reaction:", "quick question", "bro", "ok but", "bruh", "fun fact:",
        "chat is this real", "hear me out", "on god", "nah cause why", "not to be dramatic but",
        "deadass", "lowkey though", "wait hold up", "no cap", "i'm not gonna lie",
        "okay hear me out", "literally", "bruh moment:", "highkey", "can we talk about how",
        "wait a second", "valid question:", "bro think about it", "not gonna lie chat",
        "fr though", "wait actually", "side note:"
    ]

    thoughts = [
        "this update goes crazy hard",
        "the dev team is actually cooking right now",
        "we are so back",
        "this build is pure aura no cap",
        "i'm fully locked in today",
        "the repo is looking absolutely mental",
        "who let them cook because this is straight fire",
        "caffeine kicked in and now i'm in flow state",
        "just pushed a flawless fix to my branch",
        "the performance optimization is wild",
        "the UI redesign feels buttery smooth",
        "this feature is peak software engineering",
        "we really bypassed all bugs today",
        "the architecture on this project is insane",
        "my code compiled first try without errors",
        "this refactor saved the entire codebase",
        "the latency dropped so much it's crazy",
        "this logic is insanely clean",
        "typing code at lightspeed rn",
        "everything is running smooth as butter",
        "this implementation is unmatched",
        "the response time is ridiculously fast",
        "we solved the biggest bottleneck today",
        "the code quality here is next level",
        "this hotfix fixed literally everything"
    ]

    reactions = [
        "fr fr 💯", "i'm dead 💀", "w dev team 🔥", "huge W", 
        "i'm crying 😭", "valid asf", "say less 🙏", "let's gooo 🚀",
        "speechless ngl", "absolute cinema 🎬", "10/10 no notes", "zero miss",
        "pure talent", "unreal stuff", "top tier", "legendary behavior",
        "blessed my timeline", "w in the chat", "mind blown 🤯", "aura unmatched ✨",
        "chef kiss 🤌", "sending vibes", "pure gold"
    ]

    # Generates 300 unique randomized Gen-Z combinations
    dynamic_messages = [
        f"{random.choice(openers)} {random.choice(thoughts)} {random.choice(reactions)}"
        for _ in range(300)
    ]

    static_messages = [
        "real and true 💯",
        "big W for the squad honestly",
        "bro is actually cooking 🧑‍🍳",
        "we're making it out of the debug terminal with this one 🚀",
        "i'm so locked in rn",
        "valid point ngl",
        "lowkey best update so far",
        "never let them know your next commit 🤫",
        "anyone else testing the new build?",
        "catching up on chat, pure vibes",
        "brb getting more caffeine ☕",
        "looks clean to me 👍",
        "same here honestly",
        "fair enough",
        "it's giving main character energy",
        "bro got infinite aura for this fix",
        "this is peak content right here",
        "absolute masterclass",
        "w mentality honestly",
        "living for this feature update",
        "certified hood classic",
        "bro understood the assignment 🫡",
        "no fluff just pure efficiency",
        "we take those Ws",
        "seamless execution as always",
        "hard work paying off fr"
    ]

    return list(set(dynamic_messages + static_messages))

def add_human_variance(text):
    """Applies subtle natural human behavior adjustments."""
    rand = random.random()
    if rand < 0.12:
        return text.lower()
    elif rand < 0.20:
        return text.rstrip(".!?")
    elif rand < 0.25 and len(text) > 8: # Subtle character repetition (e.g., "sooo")
        words = text.split()
        idx = random.randint(0, len(words) - 1)
        if len(words[idx]) > 3:
            words[idx] = words[idx][:-1] + (words[idx][-1] * random.randint(2, 3))
        return " ".join(words)
    return text

def trigger_typing_indicator(conn, headers, channel_id):
    """Triggers the typing status on Discord."""
    try:
        conn.request("POST", f"/api/v10/channels/{channel_id}/typing", "{}", headers)
        resp = conn.getresponse()
        resp.read() # Flush response body
    except Exception:
        pass

def send_message(conn, headers, channel_id, message_text):
    payload = json.dumps({"content": message_text, "tts": False})
    
    try:
        conn.request("POST", f"/api/v10/channels/{channel_id}/messages", payload, headers)
        resp = conn.getresponse()
        resp_data = resp.read().decode('utf-8')

        if 200 <= resp.status < 300:
            print(f"[SUCCESS] Sent: \"{message_text}\"")
            return True, conn
        elif resp.status == 429:
            try:
                rate_data = json.loads(resp_data)
                retry_after = float(rate_data.get("retry_after", 5.0))
            except (json.JSONDecodeError, ValueError):
                retry_after = 5.0
            print(f"[RATE LIMITED] Pausing execution for {retry_after:.2f}s...")
            time.sleep(retry_after)
            return send_message(conn, headers, channel_id, message_text)
        else:
            print(f"[HTTP ERROR {resp.status}] {resp.reason}: {resp_data}")
            return False, conn
    except (http.client.RemoteDisconnected, BrokenPipeError, ConnectionResetError):
        print("[NETWORK WARNING] Connection dropped. Re-establishing socket...")
        new_conn = http.client.HTTPSConnection("discord.com", 443)
        return send_message(new_conn, headers, channel_id, message_text)
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return False, conn

def build_headers(config, token):
    return {
        "Content-Type": "application/json",
        "User-Agent": config.get("user_agent", "Mozilla/5.0"),
        "Authorization": token,
        "Host": "discord.com",
        "Referer": config.get("channel_url", "")
    }

def show_help():
    print("Usage: python bot.py [subcommand]")
    print("Subcommands:")
    print("  (none)           Run the bot interactively.")
    print("  --config         Configure all settings (token hidden as you type).")
    print("  --setauth        Update token and user agent only.")
    print("  --setchannel     Update channel ID and URL only.")
    print("  --check          Validate the token and target channel (GET-only, sends nothing).")
    print("  --peek           Show the latest channel messages, read-only (sends nothing).")
    print("  --dry-run        Preview generated messages without any network request.")
    print("  --help           Show this help.")

def check_setup(config):
    """GET-only validation of the token and target channel. Sends nothing."""
    token = resolve_token(config)
    if not token:
        print(f"[FAIL] No token found. Set {TOKEN_ENV_VAR} or run `python bot.py --setauth`.")
        return False
    headers = build_headers(config, token)
    ok = True
    conn = http.client.HTTPSConnection("discord.com", 443)
    try:
        conn.request("GET", "/api/v10/users/@me", None, headers)
        resp = conn.getresponse()
        body = resp.read().decode("utf-8", "replace")
        if resp.status == 200:
            user = json.loads(body)
            print(f"[OK] Token valid - authenticated as '{user.get('username')}' (id {user.get('id')})")
        else:
            ok = False
            print(f"[FAIL] Token check: HTTP {resp.status} {resp.reason}. Token may be invalid or expired.")

        channel_id = config.get("channel_id", "")
        if not channel_id:
            print("[WARN] No channel_id configured.")
            ok = False
        else:
            conn.request("GET", f"/api/v10/channels/{channel_id}", None, headers)
            resp = conn.getresponse()
            body = resp.read().decode("utf-8", "replace")
            if resp.status == 200:
                ch = json.loads(body)
                print(f"[OK] Channel reachable - #{ch.get('name')} (type {ch.get('type')}, guild {ch.get('guild_id')})")
            else:
                ok = False
                print(f"[FAIL] Channel check: HTTP {resp.status} {resp.reason}.")
    finally:
        conn.close()
    return ok

def peek_channel(config, limit=20):
    """Read-only listing of the latest channel messages. Sends nothing."""
    token = resolve_token(config)
    if not token:
        print(f"[FAIL] No token found. Set {TOKEN_ENV_VAR} or run `python bot.py --setauth`.")
        return
    channel_id = config.get("channel_id", "")
    if not channel_id:
        print("[FAIL] No channel_id configured. Run `python bot.py --setchannel` first.")
        return
    headers = build_headers(config, token)
    conn = http.client.HTTPSConnection("discord.com", 443)
    try:
        conn.request("GET", f"/api/v10/channels/{channel_id}/messages?limit={limit}", None, headers)
        resp = conn.getresponse()
        body = resp.read().decode("utf-8", "replace")
        if resp.status != 200:
            print(f"[FAIL] HTTP {resp.status} {resp.reason}: {body[:200]}")
            return
        rows = json.loads(body)
        print(f"--- Latest {len(rows)} message(s), read-only view ---")
        for m in reversed(rows):
            author = (m.get("author") or {}).get("username", "?")
            stamp = (m.get("timestamp") or "").replace("T", " ")[:19]
            content = (m.get("content") or "").replace("\n", " ")
            if len(content) > 80:
                content = content[:77] + "..."
            print(f"{stamp}  @{author}: {content}")
        print(f"--- End of view. Nothing was sent. ---")
    finally:
        conn.close()

def dry_run():
    """Preview what would be sent - performs no network requests at all."""
    messages = get_message_list()
    try:
        entered = input("How many messages to preview [default 10]: ").strip()
        num = int(entered) if entered else 10
    except ValueError:
        num = 10
    num = max(1, min(num, len(messages), 50))
    print(f"--- DRY RUN: previewing {num} message(s). Nothing will be sent. ---")
    for i, raw in enumerate(random.sample(messages, num), 1):
        print(f"[{i}] {add_human_variance(raw)}")
    print("--- Preview complete. No messages were sent. ---")

def main():
    load_env_file()

    if len(sys.argv) > 1:
        flag = sys.argv[1].lower()
        if flag == "--config":
            configure_settings("all")
            sys.exit()
        elif flag == "--setchannel":
            configure_settings("channel")
            sys.exit()
        elif flag == "--setauth":
            configure_settings("auth")
            sys.exit()
        elif flag in ("--help", "-h"):
            show_help()
            sys.exit()
        elif flag == "--check":
            print("Running check (GET-only, sends nothing)...")
            sys.exit(0 if check_setup(load_config()) else 1)
        elif flag == "--peek":
            peek_channel(load_config())
            sys.exit()
        elif flag == "--dry-run":
            dry_run()
            sys.exit()

    config = load_config()

    if not resolve_token(config) or not config.get("channel_id"):
        print("Missing required configuration settings.")
        configure_settings("all")
        config = load_config()

    token = resolve_token(config)
    if not token:
        print(f"No token found. Set the {TOKEN_ENV_VAR} environment variable or run `python bot.py --setauth`.")
        sys.exit(1)

    headers = build_headers(config, token)

    print("=================================")
    print(f"Target Channel ID: {config['channel_id']}")
    print("=================================\n")

    print("Select Message Mode:")
    print("  1. Single Custom Message (Repeats)")
    print("  2. Random Message Selection")
    print("  3. Sequential Message Selection")
    mode = input("Choice (1/2/3): ").strip()

    if mode == "1":
        messages = [input("Enter the message text: ")]
    else:
        messages = get_message_list()
        print(f"Loaded {len(messages)} template message(s).")

    num_messages = int(input("Total number of messages to send: "))
    main_wait = float(input("Base delay between messages (seconds, e.g., 2.5): "))
    human_margin = float(input("Random variance delay (seconds, e.g., 0.5): "))
    enable_typing = input("Simulate typing indicator before sending? (y/n): ").strip().lower() == "y"

    if main_wait < 0.5:
        print("[STOP] A sub-half-second delay between messages is the fastest route to rate limits and account flags.")
        if input("Proceed anyway? (y/n): ").strip().lower() != "y":
            print("Cancelled. Raise the base delay and run again.")
            sys.exit(0)

    print()

    conn = http.client.HTTPSConnection("discord.com", 443)
    sent_indices = set()

    try:
        for i in range(1, num_messages + 1):
            if mode == "1":
                raw_msg = messages[0]
            elif mode == "3":
                raw_msg = messages[(i - 1) % len(messages)]
            else:
                if len(sent_indices) >= len(messages):
                    sent_indices.clear()
                available = [m for idx, m in enumerate(messages) if idx not in sent_indices]
                raw_msg = random.choice(available)
                sent_indices.add(messages.index(raw_msg))

            msg_to_send = add_human_variance(raw_msg)

            if enable_typing:
                trigger_typing_indicator(conn, headers, config["channel_id"])
                time.sleep(random.uniform(0.8, 1.8)) # Typing duration delay

            print(f"[{i}/{num_messages}] Sending...")
            success, conn = send_message(conn, headers, config["channel_id"], msg_to_send)

            if i < num_messages:
                delay = main_wait + (random.random() * human_margin)
                print(f"Waiting {delay:.2f}s...\n")
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Script execution stopped by user.")
    finally:
        conn.close()

    print(f"\nExecution finished. {num_messages} message attempt(s) processed.")

if __name__ == "__main__":
    main()