# Good Taste · 代码审视 7 步清单

> 这是 Linus "good taste" 工程判断的可操作 7 步拆解（入口见 [SKILL.md](../SKILL.md)）。
> 按需从数据结构往后逐项排查：核心数据结构若不成立，后续局部修补与命名打磨均无意义。

---

## 使用方法

收到一段代码后，按 1→7 顺序走。每步提出的问题如果**答得上**"为什么这样写是对的"，继续下一步。答不上就停在当前步，把问题抛回给作者。

**不要并行检查所有 7 步**。Linus 的审视方式是线性的：数据结构不对，后面几步都没意义。

---

## Step 1: 数据结构先行

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships." —— 2006

**要问的问题**：
- 核心数据结构是什么？（用一个名词回答）
- 谁是 first-class citizen，谁是派生数据？
- 数据结构的不变量（invariant）是什么？在哪里保证？
- 如果需求变了，数据结构需要变吗？
  - 如果答"是" → 数据结构抽象层不够高
  - 如果答"要改接口" → 数据结构抽错了

**坏信号**：
- 多个数据结构之间有重复字段，需要"同步"
- 需要 comment 解释"为什么 A 和 B 必须保持一致"
- 操作某个字段时总是要先 check 另一个字段
- 第一眼看不出核心结构，需要读完所有字段才能理解

**Linus 的经典案例**：
- Git 的 `commit / tree / blob / tag` 四个对象类型 = 数据结构先行的极致。一旦这 4 个定下来，所有 Git 操作都是"在这些结构上做什么"的自然推论。
- Linux 的 `struct file_operations` = 把每种文件系统/设备的差异内化到一个函数指针表，调用者永远用同一种方式。

---

## Step 2: 特殊情况能否消失

> "Sometimes you can see a problem in a different way and rewrite it so that a special case goes away and becomes the normal case, and that's good code." —— TED 2016

**要问的问题**：
- 代码里有多少个 `if` 是"special case"？（不是业务分支，是"边界特判"）
- 这些 special case 有没有一种数据结构改动可以让它们全部消失？

**Linus 的链表案例**（最具体）：

```c
// 坏 taste：需要特判头节点
void remove_entry(struct list *head, struct entry *target) {
    struct entry *prev = NULL;
    struct entry *curr = head->first;
    while (curr) {
        if (curr == target) {
            if (prev)
                prev->next = curr->next;
            else
                head->first = curr->next;   // 特殊情况
            return;
        }
        prev = curr;
        curr = curr->next;
    }
}

// 好 taste：用 pointer-to-pointer 消除了特殊情况
void remove_entry(struct list *head, struct entry *target) {
    struct entry **pp = &head->first;
    while (*pp) {
        if (*pp == target) {
            *pp = (*pp)->next;   // 对头节点和中间节点都成立
            return;
        }
        pp = &(*pp)->next;
    }
}
```

**关键洞察**：好 taste 不是"技巧"，是"把边界情况看作数据结构的不完整表达"。当你用 `list_item **` 而非 `list_item *` 来迭代，你把"head pointer"也纳入了数据结构，于是删除头节点和删除中间节点变成同一件事。

**判断方法**：
- 数一下 `if (first)` / `if (last)` / `if (empty)` / `if (single element)` 这类分支
- 如果 ≥2 个，很可能数据结构选错了
- 如果 0 个，且代码仍然清晰，可能已经 good taste

**局限**：不是所有 special case 都能消除。真实业务逻辑有真实的分支。关键是区分"业务分支"（不同流程）vs "实现分支"（同一流程的边界）。后者才是 taste 问题。

---

## Step 3: 缩进 ≤ 3 层

> "If you need more than 3 levels of indentation, you're screwed anyway, and should fix your program." —— Linux Kernel Coding Style

**这不是格式规则，是设计信号**。

**要问的问题**：
- 最深的缩进层级有多少？
- 深层缩进的原因是什么？
  - 嵌套循环 → 提取成函数
  - 嵌套条件 → 用 early return
  - 异常处理 → goto cleanup 模式
  - 状态机 → 考虑用 dispatch table

**典型修复**：

```c
// 坏：4 层缩进
void f() {
    if (a) {
        if (b) {
            for (int i = 0; i < n; i++) {
                if (c) {
                    do_work();
                }
            }
        }
    }
}

// 好：early return + 提取函数
void f() {
    if (!a || !b) return;
    for (int i = 0; i < n; i++)
        if (c) do_work();
}
```

**Linus 的倾向**：内核代码大量使用 early return 和 goto cleanup。不是因为"Linus 喜欢 goto"，是因为它们**让主路径保持扁平**。主路径扁平 = 读者立刻看懂正常情况。

---

## Step 4: 错误路径和正常路径的比例

**要问的问题**：
- 如果去掉错误处理代码，这个函数变短多少？
- 错误路径和正常路径混在一起吗，还是分离的？

**内核的标准模式**：

```c
int do_something(...) {
    resource_a = allocate_a();
    if (!resource_a)
        return -ENOMEM;

    resource_b = allocate_b();
    if (!resource_b) {
        err = -ENOMEM;
        goto free_a;
    }

    err = do_real_work(resource_a, resource_b);
    if (err)
        goto free_b;

    return 0;

free_b:
    free_b(resource_b);
free_a:
    free_a(resource_a);
    return err;
}
```

这不是"恶心的 C"——这是让**正常路径保持线性**的最清晰方式。Go 的 `defer` 和 C++ 的 RAII 是为同样目标用不同工具。共同原则：**错误处理不能让正常情况读起来像错误处理**。

**坏信号**：
- 函数 80% 的行数在处理各种错误
- 正常路径的变量要嵌套在多层 if 里才能使用
- "happy path" 需要努力才能在代码里找到

---

## Step 5: 内化复杂度 vs 推给调用方

> "为了灵活性，我让调用方自己处理" = 通常是"我没想清楚"

**要问的问题**：
- 我的 API 假设调用者知道什么？
- 这些假设合理吗？还是我在推卸责任？
- 如果调用方使用错误，是他的问题还是 API 设计问题？

**经典反例**：

```c
// 推给调用方：必须先初始化 + 必须检查返回值 + 必须释放
struct widget *w = malloc(sizeof(*w));
widget_init(w);
if (widget_setup(w) < 0) {
    widget_cleanup(w);
    free(w);
    return err;
}

// 内化复杂度：创建即可用，析构即完整清理
struct widget *w = widget_create();
if (!w) return err;
```

**内化的代价**：灵活性略有损失，但换来的是**每个调用方都少一堆 bug**。Linus 的判断通常偏向内化——除非灵活性有真实的消费者。

**Linus 的典型质疑**：
- "Why does the caller need to know about this detail?"
- "If every caller has to do the same three lines, that's the API's problem, not theirs."

---

## Step 6: 抽象层的必要性

**要问的问题**：
- 这层抽象有几个实际使用者？
  - 1 个 → 几乎肯定应该内联
  - 2 个 → 警惕，重复 2 次好过坏抽象
  - 3+ 个，且共性清晰 → 可能合理
- 删掉这层会怎样？（如果答"也还好"——那就删掉）
- 这层是在统一真实的共性，还是在假装有共性？

**Linus 对抽象的偏见**：**先重复代码，再抽象**。三个实例出来了再抽，抽出来的东西通常比"预先设计"的抽象层准确得多。

**坏抽象的信号**：
- 只有一个实现者
- 接口有大量 optional 参数（说明"共性"是假的）
- 使用者要读抽象层的实现才能正确使用它
- 抽象层本身几乎没逻辑，只是改个名字转发

**"stable API" 幻想**：这是另一种过度抽象。Linux 内核刻意不提供稳定的内核 API，因为"稳定"约束了"正确"。见 `stable-api-nonsense.rst`。

---

## Step 7: 命名是否暴露意图

**放最后不是因为不重要，是因为前 6 步没做对时改名字没用。**

**要问的问题**：
- 函数名能回答"为什么存在"，还是只回答"做什么"？
- 变量名的生命周期和它表达的意思匹配吗？
- 需不需要注释才能理解？（需要 → 名字没想好）

**命名的 Linus 倾向**：
- 短名字 > 长名字（内核代码的 `tsk`, `mm`, `vma`, `fd`，上下文里清晰就好）
- 但**全局函数必须长而具体**——`foo()` 作为全局函数是 "a shooting offense"（Kernel Coding Style）
- 类型前缀（Hungarian notation）= "brain damaged"
- 名字应该在代码里自解释：读代码不读注释也能懂

**判断方法**：
- 把所有注释删掉，代码还看得懂吗？
- 如果要写注释，注释是写"为什么这么做"还是"做了什么"？
  - 前者合理（WHY 注释）
  - 后者是命名失败（WHAT 注释补救不当命名）

---

## Full Review Template

当你用这个清单 review 代码时，给反馈用以下格式（模拟 Linus 的 LKML 回复风格）：

```
[整体判断一句话：ok / needs work / broken / horrible]

数据结构：[一句话评估]
特殊情况：[有没有消除空间]
缩进/主路径清晰度：[具体问题]
错误处理：[格式和主路径的关系]
API 边界：[谁在承担复杂度]
抽象层：[有没有过度或不足]
命名：[最弱的 2-3 个名字]

[如果 overall 不 ok]：具体到某一行的建议 —— 但优先级在前面几步。命名层面的问题等数据结构对了再说。
```

---

## 局限性

这个清单偏向 C 和系统编程的 taste。对以下范式需要谨慎适配：

- **函数式**：immutability 和纯度改变了"内化复杂度"的权衡
- **声明式/DSL**：抽象层的"必要性"判断不同
- **前端 UI**：状态机和渲染逻辑比数据结构更核心
- **ML 代码**：数据流图的 good taste 是另一套标准

Linus 本人也说过：这是我的品味，深深打着 C 的烙印。别的范式有别的 taste，不要硬套。
