#!/bin/bash
# Roda o SMO sem poder travar a GPU (e derrubar o Hyprland/terminal junto).
#   tools/run_safe.sh            -> lavapipe (Vulkan na CPU): lento, mas um shader ruim nunca dá "ring gfx timeout"
#   tools/run_safe.sh --gpu      -> GPU real, mas num unit systemd próprio (morre sozinho; um reset da GPU ainda afeta tudo)
# Argumentos extras vão para o binário. Log: build/smo-v141/logs/safe-*.log
cd "$(dirname "$0")/.." || exit 1
mode=cpu; [ "$1" = --gpu ] && { mode=gpu; shift; }
export TOTK_SHARED_FONTS=$PWD/build/substitute-fonts
# Saves e configurações fora do build/, para que apagar o build/ não leve o progresso.
export TOTK_PROFILE_DIR=${TOTK_PROFILE_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/smo-recomp/profile}
mkdir -p "$TOTK_PROFILE_DIR"
if [ $mode = cpu ]; then
  export VK_DRIVER_FILES=/usr/share/vulkan/icd.d/lvp_icd.json VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json
  export TOTK_GPU_NAME=llvmpipe MESA_SHADER_CACHE_DIR=$PWD/build/smo-v141/lvp-cache \
         TOTK_PIPELINE_CACHE=$PWD/build/smo-v141/lvp-cache/pipeline-cache.bin
fi
mkdir -p build/smo-v141/logs
log=build/smo-v141/logs/safe-$mode-$(date +%H%M%S).log
echo "modo $mode, log em $log"
exec systemd-run --user --scope --quiet --unit="smo-$mode-$$" --slice=background.slice \
  -p MemoryMax=10G build/smo-v141/smo "$@" > >(tee "$log") 2>&1
