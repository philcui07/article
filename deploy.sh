#!/usr/bin/env bash
#
# Article 站点一键部署脚本
# 用法：  GITHUB_TOKEN=ghp_xxxxxxxxxxxx  ./deploy.sh
#
# 做三件事：
#   1. 若 GitHub 上还没有 philcui07/article 仓库则创建（公开）
#   2. 把当前目录推送到 main 分支
#   3. 启用 GitHub Pages（Source = main / root）
#
# 注意：token 只通过环境变量传入，不会写入任何文件。
#
set -euo pipefail

OWNER="philcui07"
REPO="article"
BRANCH="main"

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "错误：请先设置环境变量 GITHUB_TOKEN" >&2
  echo "用法：GITHUB_TOKEN=ghp_xxxxxxxxxxxx ./deploy.sh" >&2
  exit 1
fi

API="https://api.github.com"
AUTH_HDR=(-H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/vnd.github+json")

echo "==> 1/3 检查仓库 ${OWNER}/${REPO} 是否存在"
# 必须带认证头：未认证请求限流只有 60/小时，很容易被打满返回 403，
# 会被误判成"仓库不存在"。认证后限额 5000/小时。
code=$(curl -s -o /dev/null -w "%{http_code}" "${AUTH_HDR[@]}" "${API}/repos/${OWNER}/${REPO}")
if [[ "$code" == "200" ]]; then
  echo "    仓库已存在，跳过创建"
else
  echo "    创建新仓库（公开）...（探测状态码 ${code}）"
  create_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${API}/user/repos" \
    "${AUTH_HDR[@]}" \
    -d "{\"name\":\"${REPO}\",\"private\":false,\"auto_init\":false,\"description\":\"个人文章站\"}")
  if [[ "$create_code" == "201" ]]; then
    echo "    已创建"
  elif [[ "$create_code" == "422" ]]; then
    echo "    仓库其实已存在（422），继续推送"
  else
    echo "    创建失败，状态码 ${create_code}" >&2
    exit 1
  fi
fi

echo "==> 2/3 推送 ${BRANCH} 分支"
git branch -M "${BRANCH}" 2>/dev/null || true

# remote 只存干净 URL —— token 绝不写进 .git/config
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "https://github.com/${OWNER}/${REPO}.git"
else
  git remote add origin "https://github.com/${OWNER}/${REPO}.git"
fi

# 用临时 askpass 脚本注入凭证：token 只在本次进程内存活，用完即删
ASKPASS="$(mktemp)"
cat > "${ASKPASS}" <<'EOS'
#!/bin/sh
case "$1" in
  *Username*) echo "x-access-token" ;;
  *Password*) echo "$GITHUB_TOKEN" ;;
esac
EOS
chmod 700 "${ASKPASS}"

GIT_ASKPASS="${ASKPASS}" git push -u origin "${BRANCH}"
rm -f "${ASKPASS}"

echo "==> 3/3 启用 GitHub Pages（main / root）"
# 已启用则返回 409/204，均视为成功
code=$(curl -s -o /tmp/pages_resp -w "%{http_code}" -X POST "${API}/repos/${OWNER}/${REPO}/pages" \
  "${AUTH_HDR[@]}" \
  -d "{\"source\":{\"branch\":\"${BRANCH}\",\"path\":\"/\"}}")
if [[ "$code" == "201" || "$code" == "204" || "$code" == "409" ]]; then
  echo "    Pages 已启用"
else
  echo "    Pages 返回状态码 ${code}，响应："
  cat /tmp/pages_resp
  echo
  echo "    若失败，可手动到 Settings → Pages 把 Source 设为 main / (root)"
fi

echo
echo "完成。站点地址：https://${OWNER}.github.io/${REPO}/"
echo "（首次访问可能需要等 1-2 分钟让 Pages 构建）"
