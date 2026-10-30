"""Build the Kodi repository served from GitHub Pages.

    python tools/build_repo.py <output-dir>

Writes into <output-dir>:
    index.html                              file list Kodi can browse (add this URL as a source)
    repository.lioree.ktuvit.zip            the one-time install zip for the repository
    addons.xml, addons.xml.md5              catalogue Kodi polls for updates
    <id>/<id>-<version>.zip, <id>/icon.png  one folder per addon

Publish <output-dir> as the root of the gh-pages branch.
"""
import hashlib
import os
import re
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = os.path.join(ROOT, "icon.png")

# addon id -> (source dir, files/folders inside it that go into the zip)
ADDONS = {
    "service.subtitles.ktuvit": (
        ROOT,
        ["addon.xml", "icon.png", "LICENSE.txt", "changelog.txt", "service.py", "resources"],
    ),
    "repository.lioree.ktuvit": (
        os.path.join(ROOT, "repository.lioree.ktuvit"),
        ["addon.xml", "icon.png"],
    ),
}
REPO_ID = "repository.lioree.ktuvit"
SKIP = ("__pycache__", ".pyc")


def read_version(addon_xml):
    with open(addon_xml, encoding="utf-8") as f:
        return re.search(r'<addon[^>]*\sversion="([^"]+)"', f.read()).group(1)


def build_zip(zip_path, src, entries, addon_id):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(addon_id + "/", b"")
        for entry in entries:
            path = os.path.join(src, entry)
            if os.path.isfile(path):
                z.write(path, "%s/%s" % (addon_id, entry))
                continue
            for folder, dirs, files in os.walk(path):
                dirs[:] = sorted(d for d in dirs if not d.endswith(SKIP))
                rel = os.path.relpath(folder, src).replace(os.sep, "/")
                z.writestr("%s/%s/" % (addon_id, rel), b"")
                for name in sorted(files):
                    if not name.endswith(SKIP):
                        z.write(os.path.join(folder, name), "%s/%s/%s" % (addon_id, rel, name))


def main(out):
    if os.path.exists(out) and os.listdir(out):
        sys.exit("%s is not empty" % out)
    os.makedirs(out, exist_ok=True)

    manifests = []
    for addon_id, (src, entries) in ADDONS.items():
        manifest = os.path.join(src, "addon.xml")
        version = read_version(manifest)
        folder = os.path.join(out, addon_id)
        os.makedirs(folder)
        build_zip(os.path.join(folder, "%s-%s.zip" % (addon_id, version)), src, entries, addon_id)
        shutil.copy(ICON, os.path.join(folder, "icon.png"))
        with open(manifest, encoding="utf-8") as f:
            manifests.append(re.sub(r"^<\?xml[^>]*\?>\s*", "", f.read()).strip())
        print("built %s %s" % (addon_id, version))

    # the stable zip people install once; the repository then keeps the addon updated
    repo_src, repo_entries = ADDONS[REPO_ID]
    build_zip(os.path.join(out, REPO_ID + ".zip"), repo_src, repo_entries, REPO_ID)

    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n%s\n</addons>\n' % "\n".join(manifests)
    with open(os.path.join(out, "addons.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    with open(os.path.join(out, "addons.xml"), "rb") as f:
        digest = hashlib.md5(f.read()).hexdigest()
    with open(os.path.join(out, "addons.xml.md5"), "w", newline="\n") as f:
        f.write(digest)

    with open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(
            "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"><title>Ktuvit (lioree) Kodi repository</title></head>\n"
            "<body>\n<h1>Ktuvit (lioree) Kodi repository</h1>\n"
            "<p>In Kodi: Add-ons &gt; Install from zip file &gt; this source &gt; the zip below, "
            "then Install from repository.</p>\n"
            "<a href=\"%s.zip\">%s.zip</a>\n</body></html>\n" % (REPO_ID, REPO_ID)
        )
    print("addons.xml md5 %s" % digest)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
