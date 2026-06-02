import { ref } from 'vue'

/**
 * 统一 API 请求 composable
 * 消除各 view 中重复的 fetch + 超时 + 错误处理逻辑
 */
export function useApi() {
  const loading = ref(false)
  const error = ref('')

  async function fetchJson(url, { timeout = 15000 } = {}) {
    loading.value = true
    error.value = ''
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), timeout)
    try {
      const res = await fetch(url, { signal: controller.signal })
      clearTimeout(timer)
      if (!res.ok) {
        if (res.status === 404) throw new Error('接口不存在，请检查服务是否正常运行')
        if (res.status >= 500) throw new Error(`服务器错误(${res.status})，请稍后重试`)
        throw new Error(`请求失败(${res.status})`)
      }
      return await res.json()
    } catch (e) {
      if (e.name === 'AbortError') error.value = '请求超时，请检查网络后重试'
      else if (e.name === 'TypeError' && e.message.includes('Failed to fetch')) error.value = '网络连接失败'
      else error.value = e.message || '查询失败，请稍后重试'
      return null
    } finally {
      loading.value = false
    }
  }

  return { loading, error, fetchJson }
}
