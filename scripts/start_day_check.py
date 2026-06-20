from pathlib import Path
import getpass
import subprocess
import sys

print("ScrollGuard daily start check")
print(f"user={getpass.getuser()}")
print(f"cwd={Path.cwd()}")

if getpass.getuser() != "siri":
    raise SystemExit("ERROR: You are not user 'siri'. Exit and open Ubuntu as siri.")

required = [
    Path("README.md"),
    Path("src/scrollguard/data_access.py"),
    Path("scripts/month2_smoke_test.py"),
    Path("outputs/metadata_index.csv"),
    Path("data_cache/crops/Scroll1_z1000_y3520_3584_x4256_4320.npy"),
]

missing = [str(p) for p in required if not p.exists()]
if missing:
    raise SystemExit("ERROR: Missing required files:\n" + "\n".join(missing))

result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
if result.returncode != 0:
    raise SystemExit("ERROR: git status failed:\n" + result.stderr)

if result.stdout.strip():
    print("WARNING: Git has uncommitted changes:")
    print(result.stdout)
else:
    print("OK git working tree clean")

print("OK ready for ScrollGuard work")
print("Next: continue Month 2 or run: python scripts/month2_smoke_test.py")
