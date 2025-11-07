import { useState, useEffect } from 'react';

// 自定义hook，用于在localStorage中存储和获取数据
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  // 读取localStorage中的值
  const readValue = (): T => {
    // 防止在服务器端渲染时出现错误
    if (typeof window === 'undefined') {
      return initialValue;
    }

    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  };

  // 状态管理
  const [storedValue, setStoredValue] = useState<T>(readValue);

  // 更新localStorage和状态
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      // 允许值是一个函数
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      
      // 保存到状态
      setStoredValue(valueToStore);
      
      // 保存到localStorage，处理配额超出错误
      if (typeof window !== 'undefined') {
        try {
          window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (storageError) {
          // 处理localStorage配额超出错误
          if (storageError instanceof Error && storageError.name === 'QuotaExceededError') {
            console.warn(`localStorage quota exceeded for key "${key}". Trying to clean up space...`);
            
            // 尝试清理一些可能不需要的大型数据
            try {
              // 只清理非关键数据，保留主题和认证状态
              const keysToPreserve = ['theme', 'isAuthenticated'];
              for (let i = 0; i < window.localStorage.length; i++) {
                const storageKey = window.localStorage.key(i);
                if (storageKey && !keysToPreserve.includes(storageKey)) {
                  window.localStorage.removeItem(storageKey);
                }
              }
              
              // 再次尝试保存
              window.localStorage.setItem(key, JSON.stringify(valueToStore));
            } catch (retryError) {
              console.warn(`Failed to save to localStorage even after cleanup. Using sessionStorage as fallback.`);
              // 如果仍然失败，使用sessionStorage作为备选
              window.sessionStorage.setItem(key, JSON.stringify(valueToStore));
            }
          } else {
            throw storageError;
          }
        }
      }
    } catch (error) {
      console.warn(`Error setting storage key "${key}":`, error);
    }
  };

  // 监听其他标签页的localStorage变化
  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key && event.newValue !== null) {
        setStoredValue(JSON.parse(event.newValue));
      }
    };

    // 添加事件监听器
    window.addEventListener('storage', handleStorageChange);
    
    // 清理函数
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key]);

  return [storedValue, setValue];
}