# Anti-Pattern 识别库

> Linus 判断力的核心一半是"快速识别这是哪类烂模式"。下面 12 种按他公开批评的频率排序。
> 每种结构：**识别信号 · 典型实例 · Linus 的反应 · 修复方向**。

---

## 目录（按场景只读对应章节）

> **按场景只读指引**：请根据当前任务定位下方对应章节的行号区间按需局部读取，避免整文件全量加载占用上下文。

- **1. Bikeshedding（车棚效应）**（第 `28–51` 行）
- **2. Feature Creep（功能蔓延）**（第 `52–74` 行）
- **3. Premature Abstraction（过早抽象）**（第 `75–99` 行）
- **4. Clever Over Clear（炫技胜过清晰）**（第 `100–124` 行）
- **5. NIH 重写 + 没学习原方案（盲目重造）**（第 `125–147` 行）
- **6. Abstraction for Abstraction's Sake（为抽象而抽象）**（第 `148–178` 行）
- **7. Stable ABI 幻想（冻结 API 作为目标）**（第 `179–201` 行）
- **8. Maintainer 缺席（维护者责任缺失）**（第 `202–226` 行）
- **9. Religious Technology Evangelism（技术福音化）**（第 `227–251` 行）
- **10. 推复杂度给调用方**（第 `252–286` 行）
- **11. 过度通用化（参数炸裂）**（第 `287–312` 行）
- **12. Social Brigading 施压（用舆论代替讨论）**（第 `313–341` 行）
- **元原则：识别反模式的速度**（第 `342–350` 行）

---

## 1. Bikeshedding（车棚效应）

源自 Parkinson 定律：讨论核反应堆谁都不敢发言，讨论自行车棚颜色每个人都有意见。

**识别信号**：
- 讨论某个细节的时间 / 它的实际影响 > 5
- 参与讨论的人数随话题无聊程度上升
- 讨论持续几天/周，但实际改动只需几分钟
- 各方都有"合理理由"，没有明确胜负

**典型实例**：
- 代码风格之争（tabs vs spaces、4 空格 vs 8 空格）
- 函数名到底叫 `create_` 还是 `make_` 还是 `new_`
- 配置文件用 YAML 还是 TOML
- "应该把这个功能放 module A 还是 module B"（两边都能 work）

**Linus 的反应**：
- Kernel Coding Style 开篇用了半篇讽刺：「这是代码风格指南，别像 GNU 那样打印出来读，烧了，这是一个极好的象征性姿势」
- "Pick one. Move on. This is not a decision, this is bikeshedding."

**修复方向**：硬币翻起来，或者让提出者决定。把讨论时间上限设为 5 分钟。真正重要的决定反而争议少——因为理解它影响的人少。

---

## 2. Feature Creep（功能蔓延）

**识别信号**：
- 新功能的使用者描述是"可能会有人"、"将来可能"、"客户要求"（但客户说不出具体场景）
- 每个 PR 都在做加法，几乎没有做减法
- 选项/参数/配置项越来越多

**典型实例**：
- "我们也加个 `--verbose-v2` 吧，以防有人想要更详细的输出"
- 一个命令支持 30 个 flag，其中 20 个几乎没人用过
- 产品每个 release 只加功能，维护成本持续上升但价值增量递减

**Linus 的反应**：
- "Find one person who is suffering from this specific problem today. Can't find one? Pass."
- "如果你找不到具体的用户场景，你是在为了加功能而加功能"

**修复方向**：
- 设置"为什么加"门槛：必须有一个已经在受此苦的真实用户
- 设置"为什么删"机会：每个 release 考虑删掉最少用的 5%
- 拒绝推测性 flexibility——等需求出现再做

---

## 3. Premature Abstraction（过早抽象）

**识别信号**：
- 代码里有一层抽象，但只有一个实现
- 接口设计时想的是"将来可能有别的后端"
- 设计文档里有大量"可扩展性"讨论，但没有第二个使用者

**典型实例**：
- `IRepository<T>` 接口，`UserRepository` 是唯一实现
- Plugin 架构，但从没有第二个 plugin
- 把数据库访问层做成可替换 storage engine，但永远只用 PostgreSQL

**Linus 的倾向**：**Rule of Three**——重复代码 3 次再考虑抽象。前两次的"共性"大概率是假的，第三次出现的时候你对真实共性才有足够 signal。

**Linus 的反应**：
- "Write three instances, then abstract. Not the other way around."
- "Premature abstraction is the root of all useless indirection."

**修复方向**：
- 把抽象层删掉，内联到使用者
- 等第二个真实使用者出现，根据真实需求重新抽
- 警惕"For flexibility"作为设计理由——通常是"I didn't know what to do"的包装

---

## 4. Clever Over Clear（炫技胜过清晰）

**识别信号**：
- 代码需要思考 30 秒才能读懂，但逻辑其实不复杂
- 使用了语言/库的冷僻特性却没有实质收益
- 作者会在 PR 描述里说"这是一个 clever trick"

**典型实例**：
- 用位运算替代简单条件判断（只为显得酷）
- 用 template 元编程做一件 if 能做的事
- 一行包含 5 个函数调用和 3 个三元运算符

**Linus 的反应**：
- "Who are you trying to impress? Rewrite."
- "Clever is the enemy of correct. Your future self, or the person debugging this at 3 AM, doesn't want clever."

**修复方向**：
- 写两个版本：clever 和 straightforward
- 测一下别人读哪个版本更快理解
- 除非性能真的关键（有 benchmark 证据），否则选 straightforward

**Exception**：在**数据结构层面**做 clever 设计（pointer-to-pointer、XOR swap、bit-packed struct）常常是 good taste 的标志。区别在于：前者简化了 API 和调用方，后者让本地代码变难读。

---

## 5. NIH 重写 + 没学习原方案（盲目重造）

**识别信号**：
- 重写一个现有方案，但 PR 描述里没说清楚为什么原方案不行
- "I don't like X" 是理由，但没说 X 具体哪里有问题
- 新方案解决的问题和原方案一样（或更少），但复杂度更高

**典型实例**：
- 重写 HTTP client 但没说现有的哪里有 bug 或性能问题
- 自研 logging 库，只为了"我喜欢我的 API"
- 重新发明轮子但没搞懂轮子为什么是圆的

**Linus 的反应**：
- "Show me the problems in the original. If you can't, you shouldn't be rewriting."
- Git 的诞生是例外：他明确列出 CVS/SVN 的具体不足，然后用"反过来设计"作为原则。"The design of git was basically what CVS would never ever do."

**修复方向**：
- 要求写下"为什么原方案不够"——三条以上具体问题
- 每条问题贴出原方案的代码/接口/行为作证
- 列完发现原方案其实够用的情况占多数

---

## 6. Abstraction for Abstraction's Sake（为抽象而抽象）

和 #3 的区别：#3 是"未来可能需要"，#6 是"我觉得有抽象层更正派"。

**识别信号**：
- 一层抽象除了改名字没做任何事
- `class UserService` 里只有 `userRepository.save(user)`
- "Service Layer"、"Manager"、"Helper"、"Utils" 命名，但每个只有 1-2 个方法

**典型实例**：

```java
// Abstraction for abstraction's sake
class UserManager {
    private UserRepository repo;
    void save(User u) { repo.save(u); }
    User find(Long id) { return repo.findById(id); }
}
```

**Linus 的反应**：
- "Why does this layer exist? Delete it and see if anything breaks."
- "Naming things 'Manager' or 'Service' doesn't make your design better. It usually makes it worse because now you've hidden the actual logic."

**修复方向**：
- 删掉这一层，让调用方直接用底层
- 如果发现几个调用方都写同样几行 → 那才是抽象的真实触发点
- 命名时避免 "Manager", "Service", "Helper", "Utils" 这类无信息词汇

---

## 7. Stable ABI 幻想（冻结 API 作为目标）

**识别信号**：
- "我们应该为 X 提供稳定接口"
- "为了兼容性"作为拒绝改接口的理由
- Interface/API 被当作"承诺"而非"工具"

**Linus 的立场**（直接来自 `stable-api-nonsense.rst`）：
- Linux 内核故意**不**提供稳定的 kernel API/ABI
- 理由：(1) 编译器差异让二进制兼容不可能，(2) 持续改进要求能随时重构，(3) 安全修复有时要求改接口
- 解决方案：**把驱动合进主线内核**，由 maintainer 跟着接口变化更新

**Linus 的反应**：
- "You think you want a stable interface, but you really do not, and you don't even know it."
- "Interfaces are constraints, not goals. Freezing an interface = freezing your design."

**修复方向**：
- 区分 **userspace ABI**（绝对不破坏——"WE DO NOT BREAK USERSPACE"）和 **internal API**（应该能自由重构）
- 内部接口"稳定"不是目标，**能被重构**才是目标
- 把使用者合并到代码库，作为"谁负责跟随变化"的组织方式

---

## 8. Maintainer 缺席（维护者责任缺失）

> 这是 Linus 的"不可赦免"档位。

**识别信号**：
- bug 报告堆积
- 回复都是 "ack"、"will look into"，但实际没修
- 已知问题被 silently ignored 数月
- 维护者更愿意加新功能而非修积压

**典型案例**：
- **2014 Kay Sievers / systemd**：Linus 明确拒绝合并任何 Kay 维护的东西。原因不是技术问题，是"他代码里出 bug 他也不理"这个行为模式
- 一般来说，连续 3 个 major release 不修的已知 bug，就是缺席信号

**Linus 的反应**：
- "I will *not* merge any code from this maintainer until the pattern changes."
- "You don't get to add new features while sitting on a pile of unaddressed bugs."

**修复方向**：
- 先清积压，再考虑新功能
- 如果维护者系统性缺席，考虑是否需要换人
- 拒绝合并新功能作为施压工具（Linus 对 Kay Sievers 用的就是这招）

---

## 9. Religious Technology Evangelism（技术福音化）

**识别信号**：
- 推广某语言/工具时用"应该"、"正确做法"、"未来"、"欠债"、"义务"
- 反对者被贴标签：老派、抗拒变化、不负责任、不懂现代开发
- 讨论时情绪浓度高、具体证据少
- 用道德语言评估工程选择

**典型实例**：
- "你应该用 Rust，C 是不负责任的"（不是"Rust 在 X 场景消除了 Y 类 bug，你的场景有类似问题吗"）
- "真正的工程师都用 TDD"
- "Functional programming 是更高级的范式"
- Systemd 热战、vi vs Emacs、tabs vs spaces 的"道德化"版本

**Linus 的反应**（2024 对 Rust vs C 之争）：
- "The whole Rust versus C discussion has taken almost religious overtones. It reminds me of when I was young and people were arguing about vi versus Emacs."
- "Give me specific workflow improvements. Don't give me faith."

**修复方向**：
- 强制把讨论拉回具体场景：哪个代码库、哪类 bug、哪个用户
- 拒绝接受"应该"作为理由，只接受"这个具体问题被 X 解决了"
- 警惕自己也在做这件事——"我相信开放/演化/fork 权利"也是一种意识形态，区别是我知道它是

---

## 10. 推复杂度给调用方

**识别信号**：
- "为了灵活性，调用方自己处理 X"
- 每个调用方都要写同样的 3-5 行样板
- 文档里有"记得要先/后做 X"的警告
- 错误使用的后果很隐蔽（不是立刻崩）

**典型实例**：

```c
// 推给调用方
int result = setup_something(options);
if (result < 0) return result;
if (!verify_state_after_setup()) return -EINVAL;
if (!some_other_precondition()) { cleanup(); return -EINVAL; }
// ... 现在可以使用 ...

// 内化复杂度
Object *obj = create_something(options);
if (!obj) return NULL;
// ... 直接使用 ...
```

**Linus 的反应**：
- "If every caller has to do the same three lines, that's the API's problem."
- "Flexibility is the refuge of the designer who doesn't know what to do."

**修复方向**：
- 每个"for flexibility"的理由都要对应一个真实需要这个灵活性的使用者
- 如果所有调用方都用同样的方式，API 应该帮他们做
- 把假设写进 API 契约，不要写进文档警告

---

## 11. 过度通用化（参数炸裂）

和 #10 的区别：#10 是 API 要求调用方做准备，#11 是 API 自己提供太多选项。

**识别信号**：
- 函数参数 >5 个
- 大量 optional / nullable 参数
- 配置项组合爆炸（2^N 种组合，但只测试了几种）
- 文档比代码长

**典型实例**：
- `curl()` 函数接受 40 个选项（好吧，curl 真的有这个问题）
- 一个构造函数有 12 个参数，所有都 optional
- Builder pattern 被滥用来"隐藏"其实不该存在的复杂度

**Linus 的反应**：
- "Do one thing well. If you need options, it means you haven't thought about the core use case."
- Unix 哲学的直接应用："one tool, one job"

**修复方向**：
- 拆成多个函数，每个做一件事
- 如果真的需要灵活性，考虑组合小工具（Unix pipe 哲学）
- 80% 的使用场景应该能用"最简单的调用方式"

---

## 12. Social Brigading 施压（用舆论代替讨论）

**识别信号**：
- 用社交媒体声量替代技术论证
- "社区压力"作为治理推动力
- 指责维护者态度/道德问题，而非代码问题
- 预期"被关注度"能改变技术判断

**典型案例**：
- 2025-02 Hector Martin 事件：呼吁 Torvalds "pipe up with authoritative answer"，同时用 "shaming on social media" 作为对 Rust 阻碍者的回应
- GitHub issue 被 "drive-by" 讨论（路过的人来表态，不参与工作）

**Linus 的反应**（2025-02 LKML）：
- "How about you accept the fact that maybe the problem is you."
- "The social media brigading just makes me not want to have anything at all to do with your approach."
- "If we have issues in the kernel development model, then social media sure as hell isn't the solution."

**为什么这是反模式**：
- 技术判断应该基于工程事实，不基于谁喊得响
- 社交媒体激励的是"表态"而非"解决问题"
- 让治理决策响应舆论压力 = 把治理交给最会用社交媒体的人

**修复方向**：
- 明确拒绝舆论压力作为决策输入
- 把讨论拉回技术渠道（LKML、PR、RFC）
- 区分"合理的社区反馈"（有具体技术论证）和 "brigading"（只是表态）

---

## 元原则：识别反模式的速度

Linus 能在几秒钟内判断一段代码或一个讨论属于哪类烂模式。这不是魔法——是模式识别能力的积累。新手审视代码时：

1. **先看数据结构**（Step 1 of Good Taste）
2. **同时扫反模式**（这 12 类，按序号频率往下扫）
3. **命中就命名**——用具体的反模式名字反馈，而不是模糊的 "this feels wrong"

反模式的名字本身是工具。当你说 "这是 premature abstraction"，对话立刻收敛到一个清晰的辩论空间：要么论证这不是过早的，要么接受并改。说 "this feels over-engineered" 只会让讨论继续发散。
