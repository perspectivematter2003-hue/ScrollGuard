from pathlib import Path
import zipfile

package_dir = Path("outputs/demo_package/scrollguard_v0_demo")
zip_path = Path("outputs/demo_package/scrollguard_v0_demo.zip")

if not package_dir.exists():
    raise FileNotFoundError(f"Missing demo package directory: {package_dir}")

if zip_path.exists():
    zip_path.unlink()

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for path in sorted(package_dir.rglob("*")):
        if path.is_file():
            z.write(path, path.relative_to(package_dir.parent))

print("OK built demo ZIP")
print(f"zip_path={zip_path}")
print(f"size_bytes={zip_path.stat().st_size}")
