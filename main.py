# ═══════════════════════════════════════════════════════════════════════════
#  main.py — SEMY EDITION (AUTO: IND + match start, no prompt)
#  Owner: SEMY | Telegram: @SEMY
# ═══════════════════════════════════════════════════════════════════════════
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
import sys
import asyncio
import time


_OWNER_NAME = "SEMY"
_TG_ID = "@SEMY"
DEFAULT_REGION = "IND"      # ← auto-selected region
COOLDOWN_AFTER_MATCH = 3.0  # cleanup grace


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
║  SINGH EDITION — AUTO MODE (IND + AUTO MATCH ∞)              ║
║                                                              ║
║  Owner      : {_OWNER_NAME:<46}║
║  Telegram   : {_TG_ID:<46}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def _close_leaked_aiohttp():
    try:
        from match import _aiohttp_session as _m_sess
        if _m_sess is not None and not _m_sess.closed:
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(_m_sess.close())
            finally:
                loop.close()
    except Exception:
        pass


async def _run_match_with_region(region: str):
    """Patch match.start_match_interactive to skip region prompt."""
    import match

    # Override input() inside start_match_interactive so it auto-picks region
    original_input = None
    try:
        original_input = match.__dict__.get('_orig_builtin_input')
    except Exception:
        pass

    # Simpler: monkeypatch builtins.input temporarily so region prompt
    # returns the numeric index of DEFAULT_REGION, and no further prompts block.
    import builtins
    orig_input = builtins.input

    region_idx = "1"
    try:
        from core import REGION_LIST as _REGIONS
        if region in _REGIONS:
            region_idx = str(_REGIONS.index(region) + 1)
    except Exception:
        pass

    _prompt_count = {"n": 0}
    def _auto_input(prompt=""):
        _prompt_count["n"] += 1
        # First call inside start_match_interactive = region choice
        if _prompt_count["n"] == 1:
            return region_idx
        # Any further input() calls → return empty string (no blocking)
        return ""

    builtins.input = _auto_input
    try:
        await match.start_match_interactive()
    finally:
        builtins.input = orig_input


def run_auto_loop():
    """Auto: pick IND + start match ∞ — no prompts, no menu."""
    from match import start_match_interactive

    round_n = 0
    while True:
        round_n += 1
        print()
        print("  ╔══════════════════════════════════════════╗")
        print(f"  ║       AUTO MATCH ROUND #{round_n:<3}              ║")
        print(f"  ║       Region: {DEFAULT_REGION:<27}║")
        print("  ╚══════════════════════════════════════════╝")
        print()

        try:
            # Patch input for region auto-select
            import builtins
            orig_input = builtins.input
            try:
                from core import REGION_LIST as _REGIONS
                region_idx = str(_REGIONS.index(DEFAULT_REGION) + 1) \
                    if DEFAULT_REGION in _REGIONS else "1"
            except Exception:
                region_idx = "1"

            _prompt_count = {"n": 0}
            def _auto_input(prompt=""):
                _prompt_count["n"] += 1
                if _prompt_count["n"] == 1:
                    return region_idx
                return ""

            builtins.input = _auto_input
            try:
                asyncio.run(start_match_interactive())
            finally:
                builtins.input = orig_input

            print()
            print("  ✅ Round complete — all connections closed.")
            print(f"  ⏳ Cooling down {COOLDOWN_AFTER_MATCH:.0f}s before next round...")
            time.sleep(COOLDOWN_AFTER_MATCH)

        except KeyboardInterrupt:
            print()
            print("  🛑 Ctrl+C — stopping auto loop.")
            raise
        except Exception as e:
            print()
            print(f"  X Round #{round_n} error: {e}")
            import traceback
            traceback.print_exc()
            print(f"  ⏳ Retrying in {COOLDOWN_AFTER_MATCH:.0f}s...")
            time.sleep(COOLDOWN_AFTER_MATCH)
        finally:
            _close_leaked_aiohttp()


def main():
    _show_banner()
    print()
    print(f"  🚀 AUTO MODE: Region={DEFAULT_REGION}, auto match ∞")
    print("  🛑 Press Ctrl+C anytime to stop")
    print()
    time.sleep(1.0)

    try:
        run_auto_loop()
    except KeyboardInterrupt:
        print()
        print("  👋 Stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
