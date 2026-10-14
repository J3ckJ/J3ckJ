"""Обновляет версию и звёзды в карточках assets/card-*.svg из GitHub API."""
import json, os, re, urllib.request

OWNER = "J3ckJ"
CARDS = {"AppRestore": "card-apprestore.svg", "CleanTools": "card-cleantools.svg",
         "EL-Workspace": "card-el-workspace.svg", "FlyDrop": "card-flydrop.svg"}

def api(path):
    req = urllib.request.Request(f"https://api.github.com/repos/{OWNER}/{path}",
                                 headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)

for repo, card in CARDS.items():
    path = os.path.join("assets", card)
    if not os.path.exists(path):
        continue
    svg = open(path, encoding="utf-8").read()
    tag = api(f"{repo}/releases/latest")["tag_name"]
    stars = api(repo)["stargazers_count"]
    svg = re.sub(r'(text-anchor="middle">)[^<]*(</text>)', rf"\g<1>{tag}\g<2>", svg)
    svg = re.sub(r"★ \d+", f"★ {stars}", svg)
    open(path, "w", encoding="utf-8").write(svg)
    print(repo, tag, stars)
