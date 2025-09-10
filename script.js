console.log("hello");

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const SUPABASE_URL = 'https://vuftbtsbjzzoovmajyjn.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1ZnRidHNianp6b292bWFqeWpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc0Nzc4NTAsImV4cCI6MjA3MzA1Mzg1MH0.XWhNltdhYqYVQCWfzNsXJ1HVzDmZ3BqVPOCtkI4yKYQ';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
const status = (text) => document.getElementById('status').textContent = text

// 注册
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault()
    const email = e.target.email.value
    const password = e.target.password.value
    status('正在注册...')
    const { data, error } = await supabase.auth.signUp({ email, password })
    if (error) return status('注册失败: ' + error.message)
    status('注册成功，请在邮箱里点击验证\n' + JSON.stringify(data))
})

// 登录
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault()
    const email = e.target.email.value
    const password = e.target.password.value
    status('正在登录...')
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) return status('登录失败: ' + error.message)
    status('登录成功！\n当前用户:\n' + JSON.stringify(data.user))
})

// 登出
document.getElementById('logoutBtn').addEventListener('click', async () => {
    await supabase.auth.signOut()
    status('已登出')
})

// 页面加载时检查当前 session
(async () => {
    const { data } = await supabase.auth.getSession()
    if (data.session) {
    status('当前已登录用户:\n' + JSON.stringify(data.session.user))
    } else {
    status('当前没有用户登录')
    }
})