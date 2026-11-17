# ═══════════════════════════════════════════════════════════════════════════
#  core.py — Login core (squad match ke liye only)
#  Owner: AVI CODEX | Telegram: @AVI_CODEXX
# ═══════════════════════════════════════════════════════════════════════════

import os
import sys
import re
import ssl
import json
import time
import uuid
import hmac
import string
import base64
import random
import hashlib
import asyncio
import socket
import struct
import threading
import traceback
import math
import warnings
from datetime import datetime

import aiohttp
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# gen.py wali pb2 files — proven method
import MajorloginReqBuild_pb2
import PorTs_pb2
from MajorloginResp_pb2 import MajorLoginRes as MajorLoginResponse

try:
    from protobuf_decoder.protobuf_decoder import Parser
    HAS_PARSER = True
except ImportError:
    HAS_PARSER = False
    Parser = None

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════════════
#  REGION CONFIG
# ═══════════════════════════════════════════════════════════════════════════
REGION_LIST = ["IND", "ID", "TH", "ME", "EUROPE", "VN", "BD", "PK",
               "TW", "RU", "NA", "SAC", "BR", "SG", "US"]

REGION_LANG = {
    "ME": "ar", "IND": "hi", "ID": "id", "VN": "vi", "TH": "th",
    "BD": "bn", "PK": "ur", "TW": "zh", "EUROPE": "fr", "RU": "ru",
    "NA": "na", "SAC": "es", "BR": "pt", "SG": "ms", "US": "us",
}

REGION_GROUP = {
    "IND": "IND",
    "BR": "AMERICA", "US": "AMERICA", "NA": "AMERICA", "SAC": "AMERICA",
    "ID": "OTHERS", "TH": "OTHERS", "ME": "OTHERS", "EUROPE": "OTHERS",
    "VN": "OTHERS", "BD": "OTHERS", "PK": "OTHERS", "TW": "OTHERS",
    "RU": "OTHERS", "SG": "OTHERS",
}

REGION_URLS = {
    "IND": {"server": "https://loginbp.ppmainecoonghj.com/",
            "client": "https://client.ind.freefiremobile.com/"},
    "AMERICA": {"server": "https://loginbp.ppmainecoonghj.com/",
                "client": "https://client.us.freefiremobile.com/"},
    "OTHERS": {"server": "https://loginbp.ppmainecoonghj.com/",
               "client": "https://clientbp.ggpolarbear.com/"},
}


def region_byte(region):
    reg = str(region or "IND").upper()
    if reg == "IND":
        return 0x14
    if reg == "BD":
        return 0x19
    return 0x15


def region_prefix(region, kind="online"):
    reg = str(region or "IND").upper()
    if reg == "BD":
        return "7119" if kind == "online" else "9219"
    if reg == "IND":
        return "7114" if kind == "online" else "9214"
    return "7115" if kind == "online" else "9215"


# ═══════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════
APP_ID = 100067
CLIENT_TYPE = 2
SOURCE = 2
SECRET = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"

GARENA_BASE = "https://100067.connect.garena.com/api/v2/oauth"
GRANT_URL = f"{GARENA_BASE}/guest/token:grant"
DATADOME_URL = "https://datadome.garena.com/js/"
VER_URL_BASE = "https://version.ggwhitehawk.com/live/ver.php"
PLAYSTORE_URL = "https://play.google.com/store/apps/details?id=com.dts.freefireth&hl=en&gl=US"

REGISTER_BACKOFF_START = 10.0
REGISTER_BACKOFF_MAX = 60.0
DATADOME_MAX_RETRIES = 4
VER_MAX_ATTEMPTS = 3

USER_AGENT_MSDK = "GarenaMSDK/4.0.44(V2538 ;Android 16;en;US;app 1.132.1 2019121227;)"
USER_AGENT_UNITY = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"
USER_AGENT_WEB = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

_KEYSTREAM = bytes([
    0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
    0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30,
])

SESSION_HASH = "1ac4b80ecf0478a44203bf8fac6120f5"

# Sirf squad accounts
SQUAD_ACCOUNTS_FILE = "squad_accounts.json"

REGION = "IND"
LANG_CODE = "hi"

_PLAY_VERSION = "1.132.13"
_OB_VERSION = "OB55"

HARDCODED_CONFIG = {
    "latest_release_version": "OB55",
    "remote_version": "1.132.13",
    "cdn_url": "https://dl-bs.ggpolarbear.com/live/ABHotUpdates/",
    "abhotupdate_cdn_url": "https://core-bs.ggpolarbear.com/live/ABHotUpdates/",
    "client_ip": "103.200.36.133",
    "vercfg_sign": "1.f46ddde8bb35d74e",
    "region": REGION,
    "lang": LANG_CODE,
    "country_code": REGION,
    "server_url": "https://loginbp.ggpolarbear.com/",
    "client_url": "https://client.ind.freefiremobile.com/",
}

_print_lock = threading.Lock()
_file_lock = threading.Lock()
_dd_lock = threading.Lock()
_log_lock = threading.Lock()

_dd_session_cookie = None
_dd_expires_at = 0.0

# Movement constants (match.py use karta hai)
MOVE_HZ = 15.0
MOVE_INTERVAL = 1.0 / MOVE_HZ
DASH_VEL = 501
STEP_PER_TICK = DASH_VEL / (MOVE_HZ * 0.1)
STICK_DIST = 150.0
CHASE_Y_LERP = 0.5
POSE_STANDING = 0
POSE_DASHING = 2
CMD_PLAYER_STATE_UPLOAD = 2001
CHAT_FOLLOW_TRIGGERS = (1, 2)

JHUND_MAX_AGE = 10.0
JHUND_DASH_DIST = 6000.0
JHUND_SLOT_MIN = 120.0
JHUND_SLOT_MAX = 260.0
LEADER_DEADZONE = 220.0

SEND_HZ = 10.0
MOVE_INTERVAL_BD = 1.0 / SEND_HZ
WALK_SPEED = 5150.0
STEP_PER_TICK_BD = WALK_SPEED / SEND_HZ
ZONE_RADIUS_SCALE = 1000.0

CMD_PLAYER_JOIN = 101
CMD_MATCH_END = 103
CMD_DEAD = 107
CMD_SAFE_ZONE = 117
CMD_SERVER_TIME = 2000
CMD_MY_STATE = 2001
CMD_OTHER_STATES = 2012
CMD_QUICK_CHAT = 551
CMD_GRI_SYNC = 1901
PHASE_PREPARE = 1
PHASE_FIGHT = 3
QUICK_CHAT_FOLLOW = 1
QUICK_CHAT_HELP = 2


# ═══════════════════════════════════════════════════════════════════════════
#  BASIC HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def _log(line):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    with _log_lock:
        print(f"[{ts}] {line}", flush=True)


def gen_nickname(prefix="vai"):
    chars = string.ascii_lowercase + string.digits
    return f"{prefix}_{''.join(random.choices(chars, k=4))}"


def enc_aes(data):
    return AES.new(KEY, AES.MODE_CBC, IV).encrypt(pad(data, 16))


def dec_aes(data):
    try:
        return unpad(AES.new(KEY, AES.MODE_CBC, IV).decrypt(data), 16)
    except ValueError:
        return AES.new(KEY, AES.MODE_CBC, IV).decrypt(data)


def sign_body(body):
    return hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()


def encode_open_id(open_id):
    return bytes(ord(open_id[i]) ^ _KEYSTREAM[i % len(_KEYSTREAM)] for i in range(len(open_id)))


def decode_jwt_payload(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {}
        p2 = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(p2))
    except Exception:
        return {}


def _to_bytes(v):
    if isinstance(v, bytes):
        return v
    if isinstance(v, str):
        try:
            return bytes.fromhex(v)
        except ValueError:
            return v.encode()
    if v is None:
        raise ValueError("cannot convert None")
    return bytes(v)


def _normalize_uid(uid):
    s = str(uid).strip()
    return int(s) if s.isdigit() else s


# ═══════════════════════════════════════════════════════════════════════════
#  PROTOBUF HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def enc_varint(v):
    out = bytearray()
    while True:
        b = v & 0x7F
        v >>= 7
        out.append(b | (0x80 if v else 0))
        if not v:
            return bytes(out)


def read_varint(data, off):
    v, s = 0, 0
    while True:
        b = data[off]
        off += 1
        v |= (b & 0x7F) << s
        if not (b & 0x80):
            return v, off
        s += 7


def ptag(f, wt):
    return enc_varint((f << 3) | wt)


def f_vint(f, n):
    return ptag(f, 0) + enc_varint(n)


def f_bytes(f, b):
    return ptag(f, 2) + enc_varint(len(b)) + b


def f_str(f, s):
    b = s.encode("utf-8")
    return ptag(f, 2) + enc_varint(len(b)) + b


def parse_proto(data):
    fields = {}
    i = 0
    while i < len(data):
        try:
            key, i = read_varint(data, i)
        except Exception:
            break
        fn, wt = key >> 3, key & 7
        try:
            if wt == 0:
                v, i = read_varint(data, i)
                fields.setdefault(fn, []).append(("varint", v))
            elif wt == 1:
                v = int.from_bytes(data[i:i+8], "little")
                i += 8
                fields.setdefault(fn, []).append(("u64", v))
            elif wt == 2:
                ln, i = read_varint(data, i)
                raw = data[i:i+ln]
                i += ln
                s_ok = False
                try:
                    s = raw.decode("utf-8")
                    if s.isprintable():
                        fields.setdefault(fn, []).append(("string", s))
                        s_ok = True
                except UnicodeDecodeError:
                    pass
                if not s_ok:
                    fields.setdefault(fn, []).append(("bytes", raw.hex()))
            elif wt == 5:
                v = int.from_bytes(data[i:i+4], "little")
                i += 4
                fields.setdefault(fn, []).append(("u32", v))
            else:
                break
        except Exception:
            break
    return fields


def first_value(fields, field_num, want_kind=None):
    for kind, v in fields.get(field_num, []):
        if want_kind is None or kind == want_kind:
            return v
    return None


# ═══════════════════════════════════════════════════════════════════════════
#  SQUAD ACCOUNT STORAGE (sirf squad_accounts.json)
# ═══════════════════════════════════════════════════════════════════════════
def load_squad_accounts(path=SQUAD_ACCOUNTS_FILE):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        out = []
        for rec in data:
            if not isinstance(rec, dict):
                continue
            uid = rec.get("uid")
            pw = rec.get("pass") or rec.get("password")
            if not uid or not pw:
                continue
            out.append(rec)
        return out
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════════════════════
#  VERSION / DATADOME
# ═══════════════════════════════════════════════════════════════════════════
def get_play_store_version():
    headers = {"User-Agent": USER_AGENT_WEB, "Accept-Language": "en-US,en;q=0.9"}
    html = requests.get(PLAYSTORE_URL, headers=headers, timeout=15).text
    versions = re.findall(r"\b(1\.\d{1,3}\.\d{1,3})\b", html)
    if not versions:
        raise RuntimeError("no version on playstore page")
    real = [v for v in versions if v != "1.000.000"]
    return (real or versions)[-1]


def fetch_ver_config(initial_version, region=None, lang=None):
    region = region or REGION
    lang = lang or REGION_LANG.get(region, "en")
    version = initial_version
    last = None
    for attempt in range(1, VER_MAX_ATTEMPTS + 1):
        url = (
            f"{VER_URL_BASE}?version={version}"
            f"&lang={lang}&device=android&channel=3rd_party&appstore=thirdparty"
            f"&region={region}&whitelist_version=1.7.0&whitelist_sp_version=1.0.0"
            f"&device_name=vivo%20V2538"
            f"&device_CPU=ARM64%20FP%20ASIMD%20AES"
            f"&device_GPU=Adreno%20%28TM%29%20722"
            f"&device_mem=7282"
        )
        try:
            cfg = requests.get(url, timeout=15).json()
        except Exception as e:
            last = e
            time.sleep(1.0 * attempt)
            continue
        if cfg.get("code") == 0:
            grp = REGION_GROUP.get(region, "OTHERS")
            cfg["region"] = region
            cfg["lang"] = lang
            cfg["country_code"] = region
            cfg["server_url"] = REGION_URLS[grp]["server"]
            cfg["client_url"] = REGION_URLS[grp]["client"]
            return cfg
        if cfg.get("remote_version"):
            version = cfg["remote_version"]
        last = cfg
        time.sleep(1.0 * attempt)
    raise RuntimeError(f"ver.php failed: {last}")


def get_datadome(tag, force=False):
    global _dd_session_cookie, _dd_expires_at
    with _dd_lock:
        now = time.time()
        if not force and _dd_session_cookie and _dd_expires_at > now:
            return _dd_session_cookie
        headers = {
            "User-Agent": USER_AGENT_WEB,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://sso.garena.com/universal/register?locale=en-SG",
            "Origin": "https://sso.garena.com",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
        }
        payload = {
            "jsType": "le",
            "eventCounters": '{"mousemove":1,"click":1,"keydown":11}',
            "ddk": "AE3F04AD3F0D3A462481A337485081",
            "Referer": "https://sso.garena.com/universal/register?locale=en-SG",
            "request": "/universal/register?locale=en-SG",
            "responsePage": "origin",
            "ddv": "5.7.0",
        }
        last = None
        for attempt in range(1, DATADOME_MAX_RETRIES + 1):
            try:
                r = requests.post(DATADOME_URL, data=payload, headers=headers, timeout=15)
                r.raise_for_status()
                result = r.json()
            except Exception as e:
                last = e
                time.sleep(1.5 * attempt)
                continue
            if result.get("status") == 200 and result.get("cookie"):
                for part in result["cookie"].split(";"):
                    if "datadome=" in part:
                        dd = part.replace("datadome=", "").strip()
                        if dd:
                            _dd_session_cookie = dd
                            _dd_expires_at = now + 300.0
                            return dd
            last = result
            time.sleep(1.5 * attempt)
        raise RuntimeError(f"DataDome failed: {last}")


# ═══════════════════════════════════════════════════════════════════════════
#  MAJOR LOGIN + GET LOGIN DATA (pb2 method — proven)
# ═══════════════════════════════════════════════════════════════════════════
def _build_major_login_pb2(open_id, access_token, platform, client_version,
                           region="IND", country="IND", lang="en"):
    p = MajorloginReqBuild_pb2.MajorLogin()
    p.open_id = open_id
    p.access_token = access_token
    p.client_version = client_version
    p.event_time = str(int(time.time()))
    p.game_name = "free fire"
    p.platform_id = 1
    p.system_software = "Android OS 16 / API-36 (BP4A.251205.006/M066BXXS8CZI1)"
    p.system_hardware = "Handheld"
    p.telecom_operator = "WIFI"
    p.network_type = "WIFI"
    p.screen_width = 1600
    p.screen_height = 720
    p.screen_dpi = "300"
    p.processor_details = "ARM64 FP ASIMD AES | 2400 | 8"
    p.memory = 3507
    p.gpu_renderer = "Mali-G57 MC2"
    p.gpu_version = "OpenGL ES 3.2 v1.r38p1"
    p.unique_device_id = "Google|6acc6a56-b955-42d6-9920-7c3faa8992e3"
    p.client_ip = "122.174.21.31"
    p.language = lang
    p.open_id_type = "4"
    p.device_type = "Handheld"
    p.device_model = "samsung SM-S928B"
    p.country_code = country
    p.platform_sdk_id = 1
    p.network_operator_a = "WIFI"
    p.network_type_a = "WIFI"
    p.client_using_version = SESSION_HASH
    p.external_storage_total = 47195
    p.external_storage_available = 19418
    p.internal_storage_total = 5135
    p.internal_storage_available = 5135
    p.game_disk_storage_available = 19546
    p.game_disk_storage_total = 47195
    p.external_sdcard_avail_storage = 19546
    p.external_sdcard_total_storage = 47195
    p.field_70 = 4
    p.login_by = 3
    p.library_path = "/data/app/~~bsxEK2UVui2u9YoL_QKi_w==/com.garena.game.ffi-p7Uh_JDc-8hCjRgLvsaRqg==/lib/arm64"
    p.reg_avatar = 3
    p.library_token = ("dd9d4c174e0472d34b7fd34bd5924bc9|"
                       "/data/app/~~bsxEK2UVui2u9YoL_QKi_w==/com.garena.game.ffi-p7Uh_JDc-8hCjRgLvsaRqg==/base.apk")
    p.channel_type = 3
    p.cpu_type = 2
    p.cpu_architecture = "64"
    p.client_version_code = "2019121269"
    p.field_85 = 3
    p.graphics_api = "OpenGLES2"
    p.supported_astc_bitset = 8191
    p.login_open_id_type = 4
    p.loading_time = 13070
    p.release_channel = "android"
    p.extra_info = ("KqsHT3kf8XDT3vqFEnlSSQFMl5SRiWL2SxIxcx47LozWRI7AqvwWJ9eJ/"
                    "fXX0amawG9xA6DLOyWSJCij9Fp7M5o3bzp7/MjO1jDqX8PwDD8qq5vO")
    p.android_engine_init_flag = 111107
    p.field_96 = json.dumps({"cur_rate": [90, 60], "support_etc2": False},
                            separators=(",", ":"))
    p.if_push = 1
    p.is_vpn = 1
    p.origin_platform_type = "4"
    p.primary_platform_type = "4"
    p.field_102 = b""
    p.field_104 = 80395
    p.field_105 = 1
    p.field_106 = ("https://dl-tata.freefireind.in/live/ABHotUpdates/"
                   "|https://core-tata.freefireind.in/live/ABHotUpdates/"
                   "|dff941d41e6e3a9e76f05ed71fdc8d87")
    p.field_107 = "1.6168622e0868ddbd"
    return enc_aes(p.SerializeToString())


def major_login(tag, open_id, access_token, cfg, platform, region=None):
    url = cfg["server_url"].rstrip("/") + "/MajorLogin"
    plain = _build_major_login_pb2(
        open_id, access_token, platform,
        cfg["remote_version"],
        cfg.get("region", "IND"),
        cfg.get("country_code", "IND"),
        cfg.get("lang", "en"),
    )
    headers = {
        "User-Agent": USER_AGENT_UNITY,
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": "Bearer",
        "X-GA": "v1 1",
        "X-GA-SV": str(int(time.time())),
        "ReleaseVersion": cfg["latest_release_version"],
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.12f1",
    }
    r = requests.post(url, data=plain, headers=headers, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"MajorLogin HTTP {r.status_code}: {r.text[:200]}")
    body = r.content

    def _try(blob):
        if len(blob) < 10:
            return None
        try:
            m = MajorLoginResponse()
            m.ParseFromString(blob)
            if getattr(m, "token", "") and getattr(m, "account_id", 0):
                return m
        except Exception:
            return None

    cand = _try(body)
    if not cand and len(body) > 64:
        cand = _try(body[64:])
    if not cand:
        for off in range(1, min(128, len(body))):
            cand = _try(body[off:])
            if cand:
                break
    if not cand:
        raise RuntimeError(f"MajorLogin parse failed, raw: {body[:100].hex()}")
    return {
        "account_id": cand.account_id,
        "jwt": cand.token,
        "game_url": getattr(cand, "server_url", "") or cfg["server_url"],
        "region": getattr(cand, "lock_region", "") or cfg.get("region", "IND"),
        "aes_key": getattr(cand, "ak", b""),
        "aes_iv": getattr(cand, "aiv", b""),
        "server_time": getattr(cand, "kts", 0),
    }


def get_login_data(tag, open_id, access_token, cfg, platform, jwt):
    url = cfg["client_url"].rstrip("/") + "/GetLoginData"
    plain = _build_major_login_pb2(
        open_id, access_token, platform,
        cfg["remote_version"],
        cfg.get("region", "IND"),
        cfg.get("country_code", "IND"),
        cfg.get("lang", "en"),
    )
    headers = {
        "User-Agent": USER_AGENT_UNITY,
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": f"Bearer {jwt}",
        "X-GA": "v1 1",
        "X-GA-SV": str(int(time.time())),
        "ReleaseVersion": cfg["latest_release_version"],
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.12f1",
    }
    r = requests.post(url, data=plain, headers=headers, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"GetLoginData HTTP {r.status_code}: {r.text[:200]}")
    body = r.content

    def _try(blob):
        try:
            m = PorTs_pb2.GetLoginData()
            m.ParseFromString(blob)
            if getattr(m, "AccountUID", 0) or getattr(m, "Online_IP_Port", ""):
                return m
        except Exception:
            return None

    cand = _try(body)
    if not cand and len(body) > 64:
        cand = _try(body[64:])
    if not cand:
        for off in range(1, min(128, len(body))):
            cand = _try(body[off:])
            if cand:
                break
    if not cand:
        raise RuntimeError(f"GetLoginData parse failed, raw: {body[:100].hex()}")
    return {
        "account_id": getattr(cand, "AccountUID", 0),
        "region": getattr(cand, "Region", "") or cfg.get("region", "IND"),
        "nickname": getattr(cand, "Nickname", ""),
        "game_server": getattr(cand, "Online_IP_Port", ""),
        "chat_server": getattr(cand, "Chat_IP_Port", ""),
        "event_url": getattr(cand, "Event_URL", ""),
    }


# ═══════════════════════════════════════════════════════════════════════════
#  REGION CFG BUILDER
# ═══════════════════════════════════════════════════════════════════════════
def build_region_cfg(region):
    region = region.upper()
    grp = REGION_GROUP.get(region, "OTHERS")
    cfg = dict(HARDCODED_CONFIG)
    cfg["region"] = region
    cfg["lang"] = REGION_LANG.get(region, "en")
    cfg["country_code"] = region
    cfg["server_url"] = REGION_URLS[grp]["server"]
    cfg["client_url"] = REGION_URLS[grp]["client"]
    return cfg


# ═══════════════════════════════════════════════════════════════════════════
#  GUEST TOKEN (async — login ke liye)
# ═══════════════════════════════════════════════════════════════════════════
async def get_guest_token(uid, password, max_retries=6):
    """Async guest token grant — match login ke liye."""
    uid_val = _normalize_uid(uid)
    payload = {
        "client_id": APP_ID, "client_secret": SECRET, "client_type": CLIENT_TYPE,
        "device_id": "02-" + str(uuid.uuid4()),
        "password": password,
        "response_type": "token", "uid": uid_val,
    }
    body = json.dumps(payload, separators=(",", ":"))

    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            datadome = await asyncio.to_thread(get_datadome, "[login]", (attempt > 1))
        except Exception as e:
            last_err = f"DataDome failed: {e}"
            await asyncio.sleep(min(2.0 * attempt, 10.0))
            continue

        headers = {
            "User-Agent": USER_AGENT_MSDK,
            "Authorization": f"Signature {sign_body(body)}",
            "Cookie": f"datadome={datadome}",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(GRANT_URL, data=body, headers=headers, timeout=20) as r:
                    if r.status != 200:
                        last_err = f"HTTP {r.status}: {(await r.text())[:200]}"
                        await asyncio.sleep(min(2.0 * attempt, 10.0))
                        continue
                    data = await r.json()
                    code = data.get("code")
                    if code == 0:
                        d = data["data"]
                        return d["open_id"], d["access_token"], int(d.get("platform", 4) or 4)
                    if code in (1006, 1005):
                        wait = min(REGISTER_BACKOFF_START * (2 ** (attempt - 1)), REGISTER_BACKOFF_MAX)
                        last_err = data
                        await asyncio.sleep(wait)
                        continue
                    last_err = data
        except Exception as e:
            last_err = str(e)
        await asyncio.sleep(min(2.0 * attempt, 10.0))
    raise RuntimeError(f"guest token grant failed: {last_err}")