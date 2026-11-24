# ═══════════════════════════════════════════════════════════════════════════
#  main.py — Entry Point & Menu  (AUTO-REPEAT MATCH EDITION)
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
║  SINGH EDITION — All Regions Support                         ║
║                                                              ║
║  Owner      : {_OWNER_NAME:<46}║
║  Telegram   : {_TG_ID:<46}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

# ═══════════════ MENU ═══════════════
def main_menu():
    _show_banner()

    while True:
        print()
        print("  ╔══════════════════════════════════════════╗")
        print("  ║         MAIN MENU  BY AVI CODEX          ║")
        print("  ╠══════════════════════════════════════════╣")
        print("  ║  1. Gen Accounts (all regions)           ║")
        print("  ║  2. Join Guild                           ║")
        print("  ║  3. Start Match (all regions)            ║")
        print("  ║  4. Exit                                 ║")
        print("  ╚══════════════════════════════════════════╝")
        print()
        try:
            choice = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "1":
            try:
                from core import generate_accounts_interactive
                generate_accounts_interactive()
            except Exception as e:
                print(f"\n  X ERROR in Gen Accounts: {e}")
                print("  ─── FULL TRACEBACK ───")
                traceback.print_exc()

        elif choice == "2":
            try:
                from core import join_clan_interactive
                asyncio.run(join_clan_interactive())
            except KeyboardInterrupt:
                print("\n  Join Guild stopped by user.")
            except Exception as e:
                print(f"\n  X ERROR in Join Guild: {e}")
                print("  ─── FULL TRACEBACK ───")
                traceback.print_exc()

        elif choice == "3":
            try:
                from match import start_match_interactive
                asyncio.run(start_match_interactive())
            except KeyboardInterrupt:
                print("\n  Match loop stopped by user.")
            except Exception as e:
                print(f"\n  X ERROR in Start Match: {e}")
                print("  ─── FULL TRACEBACK ───")
                traceback.print_exc()

        elif choice == "4":
            print("  Exiting...")
            break
        else:
            print(f"  ! Invalid choice, try again.")

        print()
        try:
            input("  Press Enter to continue...")
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n  interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Fatal error in main.py: {e}")
        print("  ─── FULL TRACEBACK ───")
        traceback.print_exc()
        sys.exit(1)