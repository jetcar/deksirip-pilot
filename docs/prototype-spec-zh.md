# 技术原型规格说明

状态：Draft 0.1。本文件是研究原型规格，不是可以直接用于国家治理的
信息系统。原型需要在小规模、自愿参加的试点中验证“资源—决定—行动—审计”
这条链条。

## 1. 范围

原型服务于一个地方试点和有限的资源集合，例如食品、闲置空间、生产工时
和储备。它不替代法定身份登记、会计、医疗或司法系统。外部系统通过可导出
记录和人工确认接入。

## 2. 核心实体

| 实体 | 记录内容 |
|---|---|
| `PersonCredential` | 参与权和基本服务权；个人数据单独保存 |
| `Asset` | 仓库、房间、设备、基础设施及责任范围 |
| `ResourceBatch` | 资源类型、数量、单位、质量、地点和有效期 |
| `Capacity` | 产能、可用工时、限制条件和证明材料 |
| `Request` | 请求人、用途、期限、数量、优先级和替代方案 |
| `Reservation` | 条件性分配、失效时间和取消条件 |
| `Project` | 目标、计划、投入、阶段、风险、指标和退出方案 |
| `Vote` | 问题、选项、资格规则、时间和计票验证方式 |
| `Decision` | 结果、少数意见、适用规则和有效期限 |
| `LedgerEvent` | 含作者、时间、链接和哈希的追加式事件 |
| `AuditFinding` | 检查、证据、违规、纠正措施和责任方 |
| `AIAnalysis` | 问题、来源、假设、模型、计算和不确定性 |

## 3. 不变量

只有满足以下条件，系统才算正确：

1. 每一次实体资源移动都必须有账本事件：来源、接收方、数量、时间、确认
   以及操作后的余额。
2. 数字余额不能超过已确认的实体余额。
3. 预约不是最终转移；它必须失效、取消，或通过单独事件变成已确认的交付。
4. 投票不会直接改变资源。投票产生决定，实际行动必须由单独操作检查权限、
   规则和可用余额后执行。
5. 每个人在每个问题中只能有一个有效选票；重复、撤回和过期选票必须可以
   被验证并排除。
6. 每个决定都要链接到规则、数据版本、计算过程和实体影响。
7. 不公开个人隐私数据。公开审计获得汇总数据和资格证明，而不是不必要的
   个人信息。
8. 紧急授权必须有期限、范围和强制性的事后审计。
9. 事件账本只能追加。更正必须作为新事件记录原因并链接原错误。

## 4. 允许的操作

所有操作都必须明确并写入日志：

```text
register_asset(asset, evidence)
publish_stock(batch, evidence)
publish_capacity(capacity, evidence)
submit_request(request)
reserve_resource(request, allocation, expiry)
record_delivery(reservation, physical_confirmation)
record_use(delivery, quantity, evidence)
propose_project(project)
open_vote(proposal, rules, closing_time)
cast_vote(vote, proof_of_eligibility)
close_vote(vote, tally_proof)
release_tranche(project, stage, resource_plan)
audit_event(event_range, auditor)
ask_ai(question, data_snapshot, model_version)
```

AI 没有 `cast_vote`、`close_vote`、`record_use`、`release_tranche`、
`edit_event` 或 `publish_decision` 权限。AI 只能读取经过授权的数据快照并
生成带签名的分析报告。

## 5. 流程状态

项目：`draft → reviewed → voted → active → paused/completed/cancelled`。

每一次状态转换都必须写明作者、规则、证据和后果。进入 `cancelled` 不得
删除历史，也不得追溯性地释放已经使用的资源。

投票：`draft → public_review → open → closed → challenged/confirmed`。
质疑会启动复核，但不能覆盖原始结果。

## 6. AI 助手契约

每一个 AI 答案必须包含：

- 使用的数据快照和日期；
- 原始记录及适用规则的链接；
- 假设、不确定性范围和已知数据缺口；
- 模型版本和简短的转换日志；
- 一个替代情景以及反对主要建议的论据。

对于影响基本服务的决定，AI 至少展示两个情景以及可能受损的群体。用户
必须能够打开来源数据、重复计算并请求人工复核。

## 7. 隐私与韧性

- 身份、投票资格、医疗数据和经济操作使用不同的数据域；
- 无记名投票使用与身份分离的资格证明，不公开身份与选择的对应关系；
- 纸质和现场渠道是同等的备用渠道；
- 离线事件先在本地签名，恢复连接后再处理冲突；
- 独立账本副本不能由同一个运营者控制；
- 关键导出文件必须不依赖专有软件也能读取。

## 8. 验收测试

只有独立审查员确认以下事项后，原型才算准备完成：

1. 不能凭空创造资源，也不能超出余额使用资源；
2. 不能重复投票，也不能看到其他参与者的选择；
3. 每个公开结果都能从保存的数据快照中复现；
4. AI 不能修改账本、投票或执行资源分配；
5. 更正仍然在历史记录中可见；
6. 网络中断时仍可按备用流程工作，重新同步时能发现冲突；
7. 参与者可以验证自己的资格、结果和相关资源，同时不能访问他人的个人
   数据；
8. 紧急授权会自动到期，并生成强制性的事后审计案件。

每项测试都要公开输入、操作、预期结果、实际结果和已知限制。
