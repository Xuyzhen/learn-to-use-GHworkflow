# learn-to-use-GHworkflow

## 流水线流程图

```
┌─────────────────────────────────────────────────┐
│                    e2e                           │
│                                                  │
│  ┌──────────┐            ┌──────────────────┐   │
│  │  build   │──output──→ │ failure analyze   │   │
│  │          │            │                  │   │
│  │ artifact │            │ 接收e2e output   │   │
│  │ ↑        │            │ 上传自身artifact │   │
│  └──────────┘            └──────────────────┘   │
│                                                  │
└──────────┬──────────────────────────┬───────────┘
           │ artifact                 │ workflow_run
           │ workflow_run             │
           ▼                          ▼
   ┌──────────────┐          ┌──────────────┐
   │  read e2e    │          │  upload obs  │
   │              │          │              │
   │ 下载e2e的   │          │ 下载failure  │
   │ artifact     │          │ analyze的    │
   │              │          │ artifact     │
   │ 追加自身     │          │              │
   │ 时间戳+秘钥  │          │ 追加自身     │
   └──────────────┘          │ 时间戳+秘钥  │
                             └──────────────┘

触发条件：e2e success → 下游全部执行
          e2e 失败/取消 → 下游全部跳过
```

## 工作流参数说明

### e2e

| 参数 | 类型 | 说明 |
|---|---|---|
| `secrets.TEST_KEY_A` | Secret | 仓库秘钥，用于验证秘钥是否可被读取 |
| `github.event.pull_request.number` | GitHub 上下文 | PR 号，仅 PR 触发时有值 |
| `github.event.pull_request.title` | GitHub 上下文 | PR 标题，仅 PR 触发时有值 |
| `result-one.md` | Artifact | build job 的输出文件，通过 artifact 上传，标注 `[Delivered via artifact]` |
| `result-two` | Output | build job 的输出，通过 `GITHUB_OUTPUT` 传递给 failure analyze，标注 `[Delivered via output]` |

**触发方式**：`workflow_dispatch`（手动）/ `pull_request`（PR）

**产出**：
- `timestamp-artifact`：包含 result-one.md（artifact 方式）
- `result-two` output：传递给 failure analyze（output 方式）

### read e2e

| 参数 | 类型 | 说明 |
|---|---|---|
| `secrets.TEST_KEY_A` | Secret | 仓库秘钥，与 e2e 读取同一个 |
| `secrets.GITHUB_TOKEN` | Secret | 自动提供的 token，用于下载跨工作流 artifact |
| `github.event.workflow_run.id` | GitHub 上下文 | e2e 的 run ID，用于下载 e2e 的 artifact |
| `github.event.workflow_run.conclusion` | GitHub 上下文 | e2e 的运行结果，仅 `success` 时执行 |

**触发方式**：`workflow_run`，e2e 完成后自动触发

**产出**：`timestamp-artifact-from-e2e`：包含 e2e 的 result-one.md + read e2e 自身的时间戳和秘钥状态

### failure analyze

| 参数 | 类型 | 说明 |
|---|---|---|
| `inputs.result-two` | Input | 从 e2e 通过 output 传入的结果 |
| `secrets.TEST_KEY_A` | Secret | 仓库秘钥，通过 `secrets: inherit` 继承自 e2e |

**触发方式**：`workflow_call`，由 e2e 内部调用

**产出**：`timestamp-artifact-fa`：包含 e2e 的 result-two + failure analyze 自身的时间戳和秘钥状态

### upload obs

| 参数 | 类型 | 说明 |
|---|---|---|
| `secrets.TEST_KEY_A` | Secret | 仓库秘钥，与 e2e 读取同一个 |
| `secrets.GITHUB_TOKEN` | Secret | 自动提供的 token，用于下载跨工作流 artifact |
| `github.event.workflow_run.id` | GitHub 上下文 | e2e 的 run ID，用于下载 failure analyze 的 artifact（因 FA 在 e2e 内部调用，artifact 归属于 e2e 的 run） |
| `github.event.workflow_run.conclusion` | GitHub 上下文 | e2e 的运行结果，仅 `success` 时执行 |

**触发方式**：`workflow_run`，e2e 完成后自动触发

**产出**：`timestamp-artifact-from-fa`：包含 failure analyze 的完整结果 + upload obs 自身的时间戳和秘钥状态

## Secrets 配置

在仓库 **Settings → Secrets and variables → Actions** 中添加：

| Secret 名称 | 说明 |
|---|---|
| `TEST_KEY_A` | 测试秘钥，所有工作流都会尝试读取并判断是否为空 |

> `GITHUB_TOKEN` 由 GitHub 自动提供，无需手动添加。

## 数据传递方式

| 方式 | 适用场景 | 本项目使用位置 |
|---|---|---|
| **Artifact** | 跨工作流传文件（workflow_run 触发的下游下载） | e2e → read e2e |
| **Output** | 同工作流内 job 间传值（workflow_call 传参） | e2e build → failure analyze |
| **Artifact（嵌套）** | reusable workflow 的 artifact 归属于调用者 run | failure analyze → upload obs（通过 e2e run ID 下载） |
