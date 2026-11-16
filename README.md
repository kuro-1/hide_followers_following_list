<div align="center">

# 🔒 Instagram Hide Followers & Following List

**A zero-dependency, security-hardened Python CLI tool to hide your Instagram followers and following lists via Instagram's internal GraphQL API.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)

</div>

---

## ✨ Key Features

- **Zero External Dependencies:** Built purely on Python's standard library (`urllib`, `json`, `base64`, `getpass`, `re`). No `pip install` required.
- **Security-First Architecture:**
  - 🙈 **Masked Input:** Uses `getpass` so your `sessionid` is never echoed on screen or saved in shell history.
  - 🛡️ **Credential Redaction:** Automatically strips tokens, headers, and `sessionid` values from HTTP error logs (`<REDACTED>`).
  - 🚫 **Redirect & Proxy Lock:** Blocks HTTP redirects (`NoRedirect`) and bypasses system proxies to prevent credential leakage.
  - 📦 **Memory Protection:** Caps server responses at 1 MB to prevent memory exhaustion.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/kuro-1/hide_followers_following_list.git
cd hide_followers_following_list

؛؛؛
```
## 💻 Windows GUI Download

You can download the standalone Windows executable (`InstagramHideLists.exe`) directly from the [Releases](https://github.com/kuro-1/hide_followers_following_list/releases) page—no Python installation required.

> **Note on Windows SmartScreen Warning:** Because this executable is unsigned, Windows Defender SmartScreen may display a *"Windows protected your PC"* prompt when you first run it. Click **More info** $\rightarrow$ **Run anyway** to launch the app, or inspect `gui_hide_lists.py` and build it yourself.
