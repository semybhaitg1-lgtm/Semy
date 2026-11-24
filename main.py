

# ═══════════════ OWNER DETAILS ═══════════════
# ═══════════════════════════════════════════════════════════════════════════
#  main.py — FULL AUTO MODE  (no menu, no input, no command)
#  Owner: AVI CODEX  | Telegram: @AVI_CODEXX
# ═══════════════════════════════════════════════════════════════════════════
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import sys
import asyncio
import traceback

# ═══════════════ OWNER DETAILS ═══════════════
_OWNER_NAME = "AVI CODEX"
_TG_ID = "@AVI_CODEXX"

# ═══════════════ AUTO CONFIG ═══════════════
_AUTO_REGION   = "IND"     # 👈 yahan region change kar sakte ho (IND / BD / ME / SG / ID / TH / VN / PK / US / BR)
_AUTO_GAP_SEC  = 5         # match end ke baad gap (seconds)


# ═══════════════ BANNER ═══════════════
def _show_banner():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   █████╗ ███╗   ██╗██╗   ██╗██████╗  █████╗  ██████╗         ║
║  ██╔══██╗████╗  ██║██║   ██║██╔══██╗██╔══██╗██╔════╝         ║
║  ███████║██╔██╗ ██║██║   ██║██████╔╝███████║██║  ███╗        ║
║  ██╔══██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║██║   ██║        ║
║  ██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║  ██║╚██████╔╝        ║
║  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝         ║
║                                                              ║
║  SINGH EDITION — AUTO MODE (No Command Needed)               ║
║                                                              ║
║  Owner      : {_OWNER_NAME:<46}║
║  Telegram   : {_TG_ID:<46}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


# ═══════════════ AUTO RUNNER ═══════════════
def _auto_run_match_loop():
    """
    Koi menu nahi, koi input nahi.
    Seedha Start Match + IND region + infinite repeat.
    """
    from match import run_squad_game
    from core import load_squad_accounts, load_accounts, REGION_LIST

    # ── Accounts load ──
    accounts = load_squad_accounts()
    print(f"  [AUTO] squad_accounts loaded: {len(accounts)}")
    if len(accounts) < 2:
        accounts = load_accounts()
        print(f"  [AUTO] accs.txt loaded: {len(accounts)}")
    if len(accounts) < 2:
        print(f"  X Need at least 2 accounts (found {len(accounts)})")
        return

    # ── Region fix ──
    region_hint = _AUTO_REGION
    if region_hint not in REGION_LIST:
        print(f"  ! Region '{region_hint}' invalid, fallback to IND")
        region_hint = "IND"

    print(f"\n  ══════════ AUTO MODE STARTED ══════════")
    print(f"  Region  : {region_hint}")
    print(f"  Gap     : {_AUTO_GAP_SEC}s between matches")
    print(f"  Stop    : Ctrl+C")
    print(f"  ═══════════════════════════════════════\n")

    # ── Infinite match loop ──
    match_no = 1
    while True:
        print(f"\n  ══════════ MATCH #{match_no} STARTING ══════════\n")
        try:
            ok = asyncio.run(run_squad_game(accounts, region_hint=region_hint))
        except KeyboardInterrupt:
            print("\n  [AUTO] stopped by user (Ctrl+C)")
            return
        except Exception as e:
            print(f"  X Match #{match_no} crashed: {e}")
            print("  ─── FULL TRACEBACK ───")
            traceback.print_exc()
            ok = False

        status = "OK" if ok else "FAILED"
        print(f"\n  ────────── MATCH #{match_no} ENDED [{status}] ──────────")
        match_no += 1

        # ── Gap ──
        print(f"  [AUTO] waiting {_AUTO_GAP_SEC}s before next match...")
        try:
            import time
            time.sleep(_AUTO_GAP_SEC)
        except KeyboardInterrupt:
            print("\n  [AUTO] stopped by user (Ctrl+C)")
            return


# ═══════════════ ENTRY POINT ═══════════════
if __name__ == "__main__":
    try:
        _show_banner()
        _auto_run_match_loop()
    except KeyboardInterrupt:
        print("\n  interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Fatal error in main.py: {e}")
        print("  ─── FULL TRACEBACK ───")
        traceback.print_exc()
        sys.exit(1)
