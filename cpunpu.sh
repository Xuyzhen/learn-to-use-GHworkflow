#!/bin/bash

echo "========== CPU Info =========="
lscpu

echo ""
echo "========== NPU Info =========="
npu-smi info
