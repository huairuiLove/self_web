#!/usr/bin/env bash
# Download and import GLM-4-32B-0414 IQ3_XXS (~12.8GB) for 16GB RAM systems.
set -euo pipefail

MODEL_REPO="bartowski/THUDM_GLM-4-32B-0414-GGUF"
MODEL_FILE="THUDM_GLM-4-32B-0414-IQ3_XXS.gguf"
DOWNLOAD_DIR="${HOME}/.lmstudio/downloads/THUDM_GLM-4-32B-0414-GGUF"
TARGET_FILE="${DOWNLOAD_DIR}/${MODEL_FILE}"

echo "==> Function Search · LM Studio 模型安装"
echo "    推荐量化: IQ3_XXS (~12.8GB)"
echo "    适用环境: 16GB 内存 Mac，推理质量在 ~12GB 档最佳"
echo

if ! command -v lms >/dev/null 2>&1; then
  echo "错误: 未找到 lms CLI，请先安装 LM Studio 并启用命令行工具" >&2
  exit 1
fi

if ! command -v huggingface-cli >/dev/null 2>&1 && ! command -v hf >/dev/null 2>&1; then
  echo "==> 安装 huggingface_hub CLI"
  python3 -m pip install -U "huggingface_hub[cli]"
fi

HF_CLI="hf"
if command -v huggingface-cli >/dev/null 2>&1; then
  HF_CLI="huggingface-cli"
fi

mkdir -p "${DOWNLOAD_DIR}"

if [[ -f "${TARGET_FILE}" ]]; then
  echo "==> 模型文件已存在: ${TARGET_FILE}"
else
  echo "==> 开始下载 ${MODEL_REPO}/${MODEL_FILE}"
  "${HF_CLI}" download "${MODEL_REPO}" "${MODEL_FILE}" --local-dir "${DOWNLOAD_DIR}"
fi

echo "==> 导入到 LM Studio"
lms import "${TARGET_FILE}" --user-repo "bartowski/glm-4-32b-0414-gguf" -y

echo
echo "==> 后续步骤"
echo "1. 在 LM Studio 中加载模型: lms load glm-4-32b-0414 -c 4096 -y"
echo "2. 启动本地 API 服务: lms server start"
echo "3. 测试问答: function-search ask '如何用 json 序列化 dict？'"
echo
echo "配置文件: ~/Library/Application Support/FunctionSearch/config.json"
