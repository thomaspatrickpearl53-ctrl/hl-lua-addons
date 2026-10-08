"""Owner-only approved-folder publisher. Default mode is validation, never upload."""
import argparse
import hashlib
import json
import re
import shutil
import stat
import subprocess
import time
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REPO = "thomaspatrickpearl53-ctrl/hl-lua-addons"
MAX_BYTES = 200 * 1024 * 1024
ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.-]+)?\Z")
BLOCKED = {".exe", ".dll", ".com", ".bat", ".cmd", ".ps1", ".vbs", ".msi", ".scr", ".lnk", ".so", ".dylib"}


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()


def validate(path):
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("ZIP exceeds 200 MiB")
    with zipfile.ZipFile(path) as archive:
        files = archive.infolist()
        if len(files) > 10000 or sum(f.file_size for f in files) > MAX_BYTES:
            raise ValueError("Too many files or excessive uncompressed size")
        names = set()
        manifests = []
        for info in files:
            name = info.orig_filename
            parts = tuple(name.rstrip("/").split("/"))
            if any(not p or re.fullmatch(r"(?i:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?", p) for p in parts):
                raise ValueError("Unsafe Windows archive path: " + name)
            if not parts or name.startswith("/") or "\\" in name or ":" in name or any(p in (".", "..") or p.endswith((".", " ")) for p in parts):
                raise ValueError("Unsafe archive path: " + name)
            if any(ord(c) < 32 for c in name) or name.casefold() in names:
                raise ValueError("Duplicate or invalid archive path")
            names.add(name.casefold())
            if stat.S_ISLNK(info.external_attr >> 16) or info.flag_bits & 1:
                raise ValueError("Links and encrypted entries are not supported")
            if PurePosixPath(name).suffix.lower() in BLOCKED:
                raise ValueError("Executable/native payload refused: " + name)
            if len(parts) == 3 and parts[0] == "addons" and parts[2] == "addon.json":
                manifests.append(name)
        if len(manifests) != 1:
            raise ValueError("Exactly one addons/<id>/addon.json is required")
        manifest_name = manifests[0]
        addon_id = PurePosixPath(manifest_name).parts[1]
        if not ID.fullmatch(addon_id):
            raise ValueError("Invalid addon folder ID")
        if archive.getinfo(manifest_name).file_size > 65536:
            raise ValueError("Manifest too large")
        data = json.loads(archive.read(manifest_name).decode("utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("Manifest must be a JSON object")
        version = data.get("version", "")
        if not isinstance(version, str) or not VERSION.fullmatch(version):
            raise ValueError("Version must be a safe semantic version such as 1.0.0")
        for name in names:
            parts = PurePosixPath(name).parts
            if len(parts) == 1 and parts[0] in {"addons", "models", "sound", "sprites", "gfx", "resource"}:
                continue
            if len(parts) < 2 or parts[1] != addon_id or parts[0] not in {"addons", "models", "sound", "sprites", "gfx", "resource"}:
                raise ValueError("Files must be inside the addon or its namespaced asset folders: " + name)
        if f"addons/{addon_id}/license.txt" not in names:
            raise ValueError("Include addons/<id>/LICENSE.txt")
        dependencies = data.get("dependencies", [])
        if not isinstance(dependencies, list) or any(not isinstance(d, str) or not ID.fullmatch(d) for d in dependencies):
            raise ValueError("Dependencies must be a list of addon IDs")
        for key in ("title", "name", "author", "description"):
            if key in data and (not isinstance(data[key], str) or len(data[key]) > 4096):
                raise ValueError("Invalid metadata: " + key)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    tag = f"{addon_id}-v{version}"
    return {"id": addon_id, "name": data.get("title") or data.get("name") or addon_id,
            "author": data.get("author", ""), "description": data.get("description", ""),
            "version": version, "dependencies": dependencies,
            "download_url": f"https://github.com/{REPO}/releases/download/{tag}/{tag}.zip",
            "sha256": digest, "size_bytes": path.stat().st_size}


def publish(path, entry):
    run("gh", "auth", "status")
    if run("git", "branch", "--show-current") != "main" or run("git", "status", "--porcelain"):
        raise ValueError("Publishing requires a clean checkout on main")
    remote = run("git", "remote", "get-url", "origin")
    if remote not in (f"https://github.com/{REPO}.git", f"https://github.com/{REPO}", f"git@github.com:{REPO}.git"):
        raise ValueError("Unexpected origin repository")
    run("git", "pull", "--ff-only")
    catalog_path = ROOT / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    previous = next((e for e in catalog["addons"] if e["id"] == entry["id"]), None)
    if previous and previous["version"] == entry["version"] and previous["sha256"] != entry["sha256"]:
        raise ValueError("This version already has different bytes; bump the version")
    tag = f"{entry['id']}-v{entry['version']}"
    asset_name = tag + ".zip"
    stage = ROOT / ".owner" / "staging" / asset_name
    stage.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, stage)
    if hashlib.sha256(stage.read_bytes()).hexdigest() != entry["sha256"]:
        raise ValueError("ZIP changed before upload; source retained")
    try:
        release = run("gh", "api", f"repos/{REPO}/releases/tags/{tag}")
    except subprocess.CalledProcessError as error:
        if "404" not in error.stderr:
            raise
        run("gh", "release", "create", tag, str(stage), "--repo", REPO,
            "--title", f"{entry['name']} {entry['version']}", "--notes", "Owner-reviewed Half-Life: Lua addon.")
    else:
        assets = json.loads(release)["assets"]
        asset = next((a for a in assets if a["name"] == asset_name), None)
        if not asset or asset.get("digest") != "sha256:" + entry["sha256"]:
            raise ValueError("Existing release could not be verified; refusing replacement")
    catalog["addons"] = sorted([e for e in catalog["addons"] if e["id"] != entry["id"]] + [entry], key=lambda e: e["id"])
    new = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    if new != catalog_path.read_text(encoding="utf-8-sig"):
        catalog_path.write_text(new, encoding="utf-8")
        run("git", "add", "--", "catalog.json")
        run("git", "commit", "-m", f"Publish {entry['id']} {entry['version']}")
    run("git", "push", "origin", "main")
    destination = ROOT / ".owner" / "published" / (tag + "-" + entry["sha256"][:12] + ".zip")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise ValueError("Local archive destination already exists; source retained")
    path.rename(destination)
    print("Published:", entry["download_url"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Upload owner-approved packages and push catalog")
    parser.add_argument("--watch", action="store_true", help="Repeat until Ctrl+C")
    args = parser.parse_args()
    folder = ROOT / ".owner" / "approved"
    folder.mkdir(parents=True, exist_ok=True)
    seen = {}
    while True:
        for path in sorted(folder.glob("*.zip")):
            before = (path.stat().st_size, path.stat().st_mtime_ns)
            if time.time() - path.stat().st_mtime < 20 or seen.get(path) == before:
                continue
            entry = validate(path)
            after = (path.stat().st_size, path.stat().st_mtime_ns)
            if before != after:
                continue
            print(json.dumps(entry, indent=2))
            if args.publish:
                publish(path, entry)
            seen[path] = before
        if not args.watch:
            break
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped.")
    except (ValueError, OSError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print("Stopped:", error)
        raise SystemExit(1)

