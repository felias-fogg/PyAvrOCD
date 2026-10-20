"""
Run sigstress.py unguarded and guarded for every attached EDBG-based probe and print
the results. A run that hangs (a blocking HID read that never returns) is killed after
the timeout and reported as such.

    python tests/stress/sigstress_all.py [rounds] [timeout]
"""
import os
import subprocess
import sys

from pyedbglib.hidtransport.hidtransportfactory import hid_transport


def main() -> int:
    """Run both modes on every probe found"""
    rounds = sys.argv[1] if len(sys.argv) > 1 else "100"
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sigstress.py")
    tools = [(d.product_string, d.serial_number) for d in hid_transport().devices]
    print(f"{len(tools)} probe(s): " + ", ".join(f"{p} ({s})" for p, s in tools))
    for product, serial in tools:
        for mode in ("unguarded", "guarded"):
            try:
                r = subprocess.run([sys.executable, script, serial, mode, rounds],
                                   capture_output=True, text=True, timeout=timeout, check=False)
                lines = [line for line in (r.stdout + r.stderr).splitlines() if line.strip()]
                print(f"--- {product} {mode} (exit {r.returncode})")
                for line in lines[-2:]:
                    print("   ", line)
            except subprocess.TimeoutExpired:
                print(f"--- {product} {mode}: HUNG, killed after {timeout} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
