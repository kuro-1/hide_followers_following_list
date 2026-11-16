import base64
import json
import re
import threading
import tkinter as tk
from tkinter import messagebox
import urllib.error
import urllib.parse
import urllib.request


def hide_lists_api(sessionid: str) -> str:
    if not sessionid or any(ord(c) <= 32 or ord(c) >= 127 or c in ';,"\\' for c in sessionid):
        raise ValueError("Enter only the sessionid cookie value, without 'sessionid='.")
    match = re.fullmatch(r"([1-9][0-9]*)(?::|%3[aA]).+", sessionid)
    if not match:
        raise ValueError("Invalid sessionid format: expected a numeric user ID followed by ':' or '%3A'.")

    user_id = match.group(1)
    token = base64.b64encode(json.dumps({
        "ds_user_id": user_id,
        "sessionid": sessionid,
        "should_use_header_over_cookies": True,
    }, separators=(",", ":")).encode()).decode("ascii")

    authorization = "Bearer IGT:2:" + token
    name = "IGSettingsBooleanMutation"
    form = {
        "method": "post",
        "format": "json",
        "server_timestamps": "true",
        "locale": "user",
        "fb_api_req_friendly_name": name,
        "client_doc_id": "2669261950526978627082629536",
        "variables": json.dumps({
            "setting_id": "hide_followers_following_list",
            "allow_error_codes": True,
            "callsite": "account_privacy",
            "value": True,
        }),
    }

    request = urllib.request.Request(
        "https://i.instagram.com/graphql/query",
        data=urllib.parse.urlencode(form).encode(),
        headers={
            "Authorization": authorization,
            "Cookie": f"sessionid={sessionid}; ds_user_id={user_id}",
            "IG-INTENDED-USER-ID": user_id,
            "X-IG-App-ID": "124024574287414",
            "X-Auth-Type": "instagram",
            "User-Agent": "Instagram 453.0.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "identity",
            "X-GraphQL-Client-Library": "pando",
            "X-FB-Friendly-Name": name,
        },
        method="POST",
    )

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            raise RuntimeError("Redirect refused; credentials were not forwarded.")

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=15) as response:
            raw = response.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise RuntimeError("Response too large.")
            body = json.loads(raw)
    except urllib.error.HTTPError as error:
        code = error.code
        with error:
            raw = error.read(16385)
        details = {}
        try:
            err_body = json.loads(raw) if len(raw) <= 16384 else {}
            if isinstance(err_body, dict):
                for key in ("message", "error_type", "status", "code"):
                    if isinstance(err_body.get(key), (str, int, bool)):
                        details[key] = err_body[key]
        except (ValueError, UnicodeError):
            pass
        text = json.dumps(details) if details else "No selected JSON error details."
        secrets = {authorization, token, sessionid, urllib.parse.unquote(sessionid),
                   urllib.parse.quote(sessionid, safe="")}
        for secret in sorted(secrets, key=len, reverse=True):
            if secret:
                text = text.replace(secret, "<REDACTED>")
        raise RuntimeError(f"HTTP {code}: {text[:300]}") from None

    data = body.get("data") if isinstance(body, dict) else None
    root = "xdt_api__v1__settings__set_bool"
    matches = [val for k, val in data.items() if k == root or k.startswith(root + "(")] if isinstance(data, dict) else []
    result = matches[0] if len(matches) == 1 and isinstance(matches[0], dict) else {}

    if (not isinstance(body, dict) or body.get("errors") or body.get("error")
            or body.get("status") == "fail" or result.get("value") is not True
            or any(result.get(k) for k in ("error_name_value", "errorNameValue", "fallback_message", "fallbackMessage"))):
        raise RuntimeError("Instagram did not confirm enabling the setting.")

    return "Enabled: Instagram returned value=true."


def on_submit():
    sessionid = entry_session.get().strip()
    btn_run.config(state=tk.DISABLED)
    lbl_status.config(text="Sending request to Instagram...", fg="#38bdf8")

    def worker():
        try:
            msg = hide_lists_api(sessionid)
            root.after(0, lambda: lbl_status.config(text=msg, fg="#22c55e"))
        except Exception as exc:
            err_msg = str(exc)
            root.after(0, lambda: lbl_status.config(text=err_msg, fg="#ef4444"))
        finally:
            root.after(0, lambda: btn_run.config(state=tk.NORMAL))

    threading.Thread(target=worker, daemon=True).start()


# إعداد نافذة التطبيق
root = tk.Tk()
root.title("Instagram Hide Lists")
root.geometry("460x240")
root.resizable(False, False)
root.configure(bg="#0f172a")

tk.Label(root, text="Instagram Hide Followers & Following", font=("Segoe UI", 13, "bold"), bg="#0f172a", fg="#f8fafc").pack(pady=(18, 5))
tk.Label(root, text="Paste your raw Instagram sessionid cookie value:", font=("Segoe UI", 9), bg="#0f172a", fg="#94a3b8").pack(pady=(0, 10))

entry_session = tk.Entry(root, width=48, font=("Consolas", 10), show="*", bg="#1e293b", fg="#f8fafc", insertbackground="white", relief=tk.FLAT)
entry_session.pack(ipady=6, padx=20)

btn_run = tk.Button(root, text="Hide Lists Now", font=("Segoe UI", 10, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief=tk.FLAT, cursor="hand2", command=on_submit)
btn_run.pack(pady=15, ipadx=20, ipady=5)

lbl_status = tk.Label(root, text="Ready.", font=("Segoe UI", 9), bg="#0f172a", fg="#94a3b8", wraplength=420)
lbl_status.pack(pady=(0, 10))

root.mainloop()
