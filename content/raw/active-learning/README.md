# 主动学习论文资料

这组资料围绕“有限标注预算下，选择哪些样本最值得标注”组织。PDF 均保存在 `papers/`，论文库通过同源 `/papers/*.pdf` 提供站内阅读与划词翻译。

## 建议阅读顺序

### 1. 建立基础框架

| 文件 | 论文 | 关注点 |
| --- | --- | --- |
| `settles-2009.pdf` | Active Learning Literature Survey | 场景、查询策略与经典术语 |
| `1703.02910.pdf` | Deep Bayesian Active Learning with Image Data | Bayesian 不确定性与 BALD |
| `1708.00489.pdf` | Active Learning for CNNs: A Core-Set Approach | 批量代表性与 k-center 覆盖 |
| `1904.00370.pdf` | Variational Adversarial Active Learning | 任务无关的潜在空间采样 |
| `1905.03677.pdf` | Learning Loss for Active Learning | 学习样本难度代理 |
| `1906.03671.pdf` | Deep Batch Active Learning by Diverse, Uncertain Gradient Lower Bounds | BADGE 的梯度嵌入 |
| `cs.9603104.pdf` | Active Learning with Statistical Models | 预期误差与预测方差下降 |

### 2. 冷启动与少样本

| 文件 | 论文 | 关注点 |
| --- | --- | --- |
| `2010.09535.pdf` | Cold-start Active Learning through Self-supervised Language Modeling | ALPS 与无标签冷启动 |
| `2109.03764.pdf` | Active Learning by Acquiring Contrastive Examples | CAL 的局部边界选样 |
| `2210.10109.pdf` | A Survey of Active Learning for Natural Language Processing | NLP 标注单位、成本与停止条件 |

### 3. 基础模型、LLM 与近期评估

| 文件 | 论文 | 关注点 |
| --- | --- | --- |
| `2401.14555.pdf` | Revisiting Active Learning in the Era of Vision Foundation Models | DINOv2/OpenCLIP 下的低预算选样 |
| `2403.14800.pdf` | Deep Active Learning: A Reality Check | 强基线、预算协议与复现风险 |
| `2404.02261.pdf` | LLMs in the Loop | LLM 自动标注与低资源语言 |
| `2405.00334.pdf` | A Survey on Deep Active Learning | 深度主动学习的新综述与分类法 |
| `2405.10808.pdf` | ActiveLLM | LLM 参与文本 few-shot 选样 |
| `2502.11767.pdf` | From Selection to Generation | LLM 主动学习完整综述 |
| `2508.03441.pdf` | MedCAL-Bench | 医学基础模型冷启动基准 |
| `2601.15773.pdf` | Next Generation Active Learning: Mixture of LLMs in the Loop | 多个本地轻量 LLM 参与标注闭环 |

### 4. 医学主动学习补充

| 文件 | 论文 | 关注点 |
| --- | --- | --- |
| `1706.04737.pdf` | Suggestive Annotation | 生物医学分割的不确定性与代表性 |
| `1809.09287.pdf` | MedAL | 医学图像特征距离采样 |
| `1910.02923.pdf` | A Survey on Active Learning and Human-in-the-Loop Deep Learning for Medical Image Analysis | 医学人机闭环综述 |
| `2101.02323.pdf` | Diminishing Uncertainty Within the Training Pool | 医学分割迭代查询 |

## 文件校验

- PDF 数量：22
- 总体积：约 59MB
- 每个文件均通过 PDF 文件头与 `pdfinfo` 页数校验
- Settles 综述来自作者公开页面，其余文件来自 arXiv PDF 入口
