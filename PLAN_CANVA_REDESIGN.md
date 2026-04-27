# Canva 风格重构方案

> 参考 awesome-claude-design 中 Canva（Playful）的 DESIGN.md
> 将现有 UI 统一为 Canva 风格：单紫色主色+渐变背景装饰+友好大圆角

---

## 风格对照

| 维度 | 当前（DESIGN.md） | 新风格（Canva） | 差异 |
|------|-------------------|-----------------|------|
| 主色 | `#667eea` 紫蓝 | `#8b3dff` 紫色（Canva Purple） | 色相偏紫 |
| 浅色底 | `#667eea15` 透明 | `--accent-soft: #f0ecff` 不透明浅紫 | 更明显、更干净 |
| 背景渐变 | `#e8f0fe → #f5f0ff → #fff` | `linear-gradient(180deg, #f0ecff 0%, #ffffff 100%)` | 更浅、更紫 |
| 卡片阴影 | `0 2px 12px rgba(0,0,0,.06)` | `0 4px 16px rgba(15,16,21,0.08)` | 更柔和、hover时加深 |
| hover阴影 | 无 | `0 8px 24px rgba(139, 61, 255, 0.12)` | 新增交互反馈 |
| 标签样式 | 细边框圆角20px | 同风格但用 `--accent-soft` 做浅底 | 不变 |
| 字体 | 系统字体栈 | 同（Canva Sans 不可用，保留系统字体） | 不变 |
| 按钮半径 | 12px | 12px → 14px | 更圆润 |
| 卡片半径 | 16px | 16px → 18px | 更圆润 |

---

## 任务拆分

### Task 1：更新色板 —— 品牌色迁移

**文件：** `DESIGN.md`

**改动：**
- `--accent: #667eea` → `--accent: #8b3dff`（Canva Purple）
- `--accent-hover: #5a6fd6` → `--accent-hover: #7929e6`
- `--accent-soft: #667eea15` → `--accent-soft: #f0ecff`
- `--bg-gradient: linear-gradient(180deg, #e8f0fe 0%, #f5f0ff 50%, #fff 100%)` → `linear-gradient(180deg, #f0ecff 0%, #ffffff 100%)`
- `--shadow-card: 0 2px 12px rgba(0,0,0,.06)` → `0 4px 16px rgba(15,16,21,0.08)`
- `--shadow-hover: 0 8px 24px rgba(139,61,255,0.12)`（新增）
- 卡片 `border-radius: 16px` → `18px`
- 按钮 `border-radius: 12px` → `14px`

---

### Task 2：更新全局样式（App.vue）

**文件：** `frontend/src/App.vue`

**改动：**
- 导航栏选中态颜色：`#667eea` → `#8b3dff`
- `a` 链接颜色：`#667eea` → `#8b3dff`
- `body` 背景色保留无色，由各页面控制

---

### Task 3：更新所有页面背景渐变 + 主色

**文件：** 所有 6 个 views 文件 + App.vue

**每个页面需要改动：**
1. 背景渐变字符串替换
2. `#667eea` → `#8b3dff`（所有出现的位置）
3. `#f0f2ff`（图标浅底）→ `#f0ecff`
4. `#f0f4ff`（悬停浅底）→ `#f0ecff`
5. `#f8f9ff`（精灵头像浅底）→ `#f5f2ff`
6. 卡片 `border-radius: 16px` → `18px`
7. 按钮 `border-radius: 12px` → `14px`
8. 卡片 shadow 值更新

---

### Task 4：添加卡片 hover 阴影交互

**文件：** 所有包含卡片的页面

**改动：**
- 在 `.card` 或 `.xxx__card` 上添加 hover 规则：
```css
.card:hover {
  box-shadow: 0 8px 24px rgba(139, 61, 255, 0.12);
}
```

---

### Task 5：更新 DESIGN.md

**文件：** `DESIGN.md`

**改动：**
- 完整重写色板、阴影、圆角值
- Do's/Don'ts 更新

---

## 执行方式

直接用 `delegate_task` 切子任务并行执行：
1. Task 1: 更新色板定义文件（DESIGN.md）
2. Task 2-4: 用 sed/patch 批量替换所有页面中的颜色值和圆角值
3. Task 5: 构建验证

由于这是大规模批量替换（6个页面 × 10+处替换），建议写一个 Python 脚本统一处理，避免漏改。
