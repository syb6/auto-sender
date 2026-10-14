# Discord Self-Bot Setup Guide

A concise guide to configuring and running the self-bot in `bot.py`.

> **Important** — This tool automates a *user account* token. Automating user
> accounts violates [Discord's Terms of Service](https://discord.com/terms) and
> can result in the account being suspended or banned. Use at your own risk.

---

## Prerequisites

| Requirement                                       | Reason                                          |
| ------------------------------------------------- | ----------------------------------------------- |
| **Python 3.8 or newer**                           | `bot.py` is written for modern Python versions. |
| **Discord Account** (Developer Mode recommended)  | Needed to fetch IDs and tokens.                 |
| **No third-party libraries**                      | Uses Python's standard library only.            |

> **Tip**  Enable *Developer Mode* in Discord (Settings ▸ Advanced) to make copying IDs easier.

---

## 1. Quick Configuration

Run the setup command and answer the prompts:

```bash
python bot.py --config
```

| Field           | Where to find it                 | Steps                                                                                                                                                                                                                      |
| --------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **User Token**  | Browser Dev Tools ▸ Network      | 1. Open Discord in a browser and log in. 2. Press **F12** (or right-click ▸ *Inspect*). 3. Open the **Network** tab. 4. Send *any* message. 5. Select the request and copy the `authorization` header value.                                  |
| **Channel ID**  | Right-click channel ▸ *Copy ID*  | Developer Mode must be enabled first.                                                                                                                                                                                                      |
| **Channel URL** | Browser address bar              | Open the target channel and copy the full URL.                                                                                                                                                                                             |

Subcommands:

| Command                      | Purpose                                        |
| ---------------------------- | ---------------------------------------------- |
| `python bot.py --config`     | Configure all settings.                        |
| `python bot.py --setauth`    | Update the token and user agent only.          |
| `python bot.py --setchannel` | Update the channel ID and URL only.            |
| `python bot.py --check`      | Validate the token and target channel (GET-only, sends nothing). |
| `python bot.py --peek`       | Show the latest channel messages (read-only).  |
| `python bot.py --dry-run`    | Preview generated messages (no network access).|
| `python bot.py --help`       | Show help.                                     |

> **Good practice:** run `python bot.py --check` first. It verifies the token
> and channel with read-only requests before anything is sent. Delays under
> half a second trigger a confirmation warning because they are the fastest
> route to rate limits and account flags.

---

## 2. Storing the Token in `.env` (recommended)

The token is a secret — it should not sit in `config.json`. Put it in a `.env`
file in the project root instead:

```bash
cp .env.example .env
# then edit .env and set:  DISCORD_TOKEN=your-token-here
```

`bot.py` loads `.env` automatically. Precedence: an environment variable set in
your shell always wins over the `.env` file, which wins over `config.json`.

`.env` and `config.json` are both listed in `.gitignore` — never commit them.

---

## 3. Running the Bot

```bash
python bot.py
```

The bot connects with the stored credentials and sends the messages chosen in
the interactive menu (single repeating message, random selection, or sequential
selection), with configurable delays between sends.

---

## 4. Custom Messages

Create a `messages.txt` file in the project root, one message per line:

```
First message here
Second message here
```

If `messages.txt` does not exist, the bot generates a rotating set of default
messages instead.

---

## 5. Troubleshooting

| Symptom                | Possible Cause                 | Fix                                                          |
| ---------------------- | ------------------------------ | ------------------------------------------------------------ |
| HTTP 401: Unauthorized | Wrong or expired *User Token*. | Re-capture the token via Dev Tools and update `.env`.        |
| HTTP 403               | Missing channel permissions.   | Make sure the account can post in that channel.              |
| Bot exits immediately  | Incorrect **Channel ID/URL**   | Verify both values; they must refer to the same channel.     |
| "No token found"       | No `DISCORD_TOKEN` configured. | Fill in `.env` or run `python bot.py --setauth`.             |

---

## 6. Useful Links

- [Discord Developer Portal](https://discord.com/developers/docs/intro)
- [Discord API Terms](https://discord.com/developers/docs/legal)

---

© 2025 — Happy coding!
