# UI 风格一致性统一方案

> 基于 DESIGN.md 对照现有代码，找出所有不一致并修复
> 执行顺序：先推送 git，再逐个修复

---

## 前置：推送当前版本到 git

```bash
# 暂存所有变更 + DESIGN.md，推一个统一commit
git add -A
git commit -m "feat: UI统一+家园炼金+蛋组配对+DESIGN.md设计规范"
git push
```

---

## 任务计划

### Task 1：清理废弃文件

**问题：** `theme.css` 是旧的 Airtable 风格主题，与 DESIGN.md 完全不匹配，且无页面引用。
**操作：** 删除 `frontend/src/styles/theme.css`

---

### Task 2：删除废弃的旧 index.html 和杂项

**问题：** `index.html.legacy` 是旧的备份，`venv/` 是无用目录，很多旧 static assets 已经被构建产物覆盖。
**操作：**
- 删除 `index.html.legacy`
- `git rm` 已删除的旧 static assets（`D` 状态的已删除文件不用管）
- `.gitignore` 添加 `venv/`

---

### Task 3：全局字体复位（App.vue）

**问题：** 目前项目**没有**全局字体和 reset 样式，部分页面用系统字体，部分没有显式设置。SpiritDetail.vue 等页面依赖 scoped style。
**操作：** 在 App.vue 的 `<style>` 中添加全局 reset（无 scoped）：

```css
/* Global reset */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
  color: #1a1a2e;
  line-height: 1.5;
}
a { color: #667eea; text-decoration: none; }
a:hover { text-decoration: none; }
img { max-width: 100%; display: block; }
```

**验证：** 构建后打开页面，确认字体和基线一致。

---

### Task 4：移除 EggQuery.vue 中的旧 CSS 变量引用

**问题：** EggQuery.vue 里用了 `.eq-` 前缀，部分来自旧 Phase 1 的风格，但样式值已和 DESIGN.md 一致。只需确认无引用无用的旧变量即可。
**操作：** 检查代码，确认无引用废弃变量，无需修改。

---

### Task 5：Garden.vue 的弹窗组件样式统一

**问题：** Garden.vue 用了渐变色按钮（已修复），但还没有弹窗组件（Modal）样式。
**操作：** 如果需要弹窗功能，按 DESIGN.md 4.11 规范添加。

---

### Task 6：统一输入框 placeholder 颜色

**问题：** 各个输入框的 placeholder 颜色不一致，有些用默认灰色，有些未设置。
**定义规范：** `::placeholder { color: #bbb; }`
**验证：** 统一采用 #bbb。

---

### Task 7：SpiritDetail.vue 中导航栏按钮样式统一

**问题：** `detail__btn` 和 `detail__shiny-toggle` 的按钮样式虽然功能特殊，但颜色值需要确认和 DESIGN.md 一致。

当前状态：已自查一致 ✅

---

### Task 8：所有页面底部 footer 统一

**问题：** 各页面的 footer 间距一致（`padding: 24px 0 16px`），已在前一轮修复。

当前状态：已自查一致 ✅

---

## 总结

主要工作是：
1. ✅ **推送 git**
2. ✅ **清理废弃文件**（theme.css、index.html.legacy、.gitignore）
3. ✅ **App.vue 添加全局 reset+字体**

实际需要改的不多，因为前一轮已经做了大部分统一工作。
