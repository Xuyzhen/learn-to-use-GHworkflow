#!/usr/bin/env python3
import sys

def test_import():
    print("[1/4] Testing vllm import...")
    import vllm
    print(f"  vllm version: {vllm.__version__}")

def test_ascend():
    print("[2/4] Testing vllm-ascend import...")
    import vllm_ascend
    print(f"  vllm-ascend OK")

def test_npu():
    print("[3/4] Testing NPU visibility...")
    import subprocess
    result = subprocess.run(["npu-smi", "info", "-l"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  NPU detected:\n{result.stdout[:200]}")
    else:
        print(f"  NPU check failed: {result.stderr}")
        return False
    return True

def test_torch_npu():
    print("[4/4] Testing torch + NPU...")
    import torch
    import torch_npu
    print(f"  torch version: {torch.__version__}")
    print(f"  torch_npu version: {torch_npu.__version__}")
    print(f"  NPU available: {torch.npu.is_available()}")
    if torch.npu.is_available():
        print(f"  NPU count: {torch.npu.device_count()}")
        print(f"  NPU name: {torch.npu.get_device_name(0)}")

if __name__ == "__main__":
    tests = [test_import, test_ascend, test_npu, test_torch_npu]
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"  FAILED: {e}")
    print("\nDone.")
