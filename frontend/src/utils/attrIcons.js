// 属性图标映射 - 来源: wiki.biligame.com/rocom
const ATTR_ICONS = {
  '普通': '/attr-icons/普通.png',
  '草': '/attr-icons/草.png',
  '火': '/attr-icons/火.png',
  '水': '/attr-icons/水.png',
  '光': '/attr-icons/光.png',
  '地': '/attr-icons/地.png',
  '冰': '/attr-icons/冰.png',
  '龙': '/attr-icons/龙.png',
  '电': '/attr-icons/电.png',
  '毒': '/attr-icons/毒.png',
  '虫': '/attr-icons/虫.png',
  '武': '/attr-icons/武.png',
  '翼': '/attr-icons/翼.png',
  '萌': '/attr-icons/萌.png',
  '幽': '/attr-icons/幽.png',
  '恶': '/attr-icons/恶.png',
  '机械': '/attr-icons/机械.png',
  '幻': '/attr-icons/幻.png',
}

export function getAttrIcon(attr) {
  return ATTR_ICONS[attr] || null
}
