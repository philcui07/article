#!/usr/bin/env python3
"""
Article 站点 · API 方式部署脚本（git 协议不通时的备选）
---------------------------------------------------------------
用法：  GITHUB_TOKEN=ghp_xxxxxxxx  python3 deploy_api.py

与 deploy.sh 的区别：
  deploy.sh    走 git 协议（需要能连 github.com:443），一次 push 一个 commit
  deploy_api.py 走 HTTPS API（只需能连 api.github.com），把整个工作区打包成一个 commit

企业网络 / 沙箱里 github.com 常被墙而 api.github.com 可用，这时就用本脚本。
注意：GitHub 的 Git Data API 不支持完全空的仓库，本脚本会先自动建初始 commit。
"""
import requests, base64, os, sys

TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("请先 export GITHUB_TOKEN=你的token")
OWNER, REPO, BRANCH = "philcui07", "article", "main"
H = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}
B = f"https://api.github.com/repos/{OWNER}/{REPO}"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 收集文件：排除 .git 目录本身，但保留 .gitignore 等点文件
files = {}
for root, dirs, fs in os.walk("."):
    dirs[:] = [d for d in dirs if d != ".git"]
    for f in fs:
        p = os.path.relpath(os.path.join(root, f), ".").replace(os.sep, "/")
        if p == ".git" or p.startswith(".git/"):
            continue
        files[p] = open(os.path.join(root, f), "rb").read()

print(f"待推送 {len(files)} 个文件:")
for p in sorted(files):
    print(f"   {p}  ({len(files[p])} B)")

# --- 步骤 0：空仓库时，Git Data API 不可用（409），先用 Contents API 建初始 commit ---
r = requests.get(f"{B}/contents/README.md", headers=H, timeout=30)
if r.status_code == 404:
    print("\n[0/4] 仓库为空 → 先用 Contents API 建立初始 commit")
    r = requests.put(f"{B}/contents/README.md", headers=H, timeout=60,
                     json={"message": "init: 初始化仓库",
                           "content": base64.b64encode(files["README.md"]).decode()})
    r.raise_for_status()
    print("      初始 commit 已建立")
else:
    print("\n[0/4] 仓库已有内容，跳过初始化")

# --- 1) blobs ---
tree = []
for p, content in files.items():
    r = requests.post(f"{B}/git/blobs", headers=H, timeout=60,
                      json={"content": base64.b64encode(content).decode(), "encoding": "base64"})
    r.raise_for_status()
    tree.append({"path": p, "mode": "100644", "type": "blob", "sha": r.json()["sha"]})
print(f"[1/4] blob 创建完成: {len(tree)}")

# --- 2) tree ---
r = requests.post(f"{B}/git/trees", headers=H, timeout=60, json={"tree": tree})
r.raise_for_status()
tree_sha = r.json()["sha"]
print(f"[2/4] tree: {tree_sha[:12]}")

# --- 3) commit：必须挂上父提交，否则更新 ref 会因非 fast-forward 报 422 ---
parent_sha = None
r = requests.get(f"{B}/git/ref/heads/{BRANCH}", headers=H, timeout=30)
if r.status_code == 200:
    parent_sha = r.json()["object"]["sha"]
    print(f"      父提交: {parent_sha[:12]}")

payload = {"message": "docs: 补充 API 部署脚本与说明",
           "tree": tree_sha,
           "parents": [parent_sha] if parent_sha else []}
r = requests.post(f"{B}/git/commits", headers=H, timeout=60, json=payload)
r.raise_for_status()
commit_sha = r.json()["sha"]
print(f"[3/4] commit: {commit_sha[:12]}")

# --- 4) ref ---
r = requests.get(f"{B}/git/ref/heads/{BRANCH}", headers=H, timeout=30)
if r.status_code == 200:
    requests.patch(f"{B}/git/refs/heads/{BRANCH}", headers=H, timeout=60,
                   json={"sha": commit_sha}).raise_for_status()
    print(f"[4/4] 已更新 {BRANCH}")
else:
    requests.post(f"{B}/git/refs", headers=H, timeout=60,
                  json={"ref": f"refs/heads/{BRANCH}", "sha": commit_sha}).raise_for_status()
    print(f"[4/4] 已创建 {BRANCH}")

requests.patch(B, headers=H, timeout=30, json={"default_branch": BRANCH})
print("默认分支已设为 main")
