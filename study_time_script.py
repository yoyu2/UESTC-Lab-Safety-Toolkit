# 导入 curl_cffi 的 requests 模块，而不是原始的 requests
from curl_cffi import requests 
import time
import json
from datetime import datetime

# ===============================================================
# API 的 URL
url = 'UM_distinctid=19836422886143d-02a6955f85525e8-4c657b58-144000-198364228871848; zg_did=%7B%22did%22%3A%20%2219899354b4959c-0160a58cb4d60e-4c657b58-144000-19899354b4a100e%22%7D; zg_=%7B%22sid%22%3A%201755915554611%2C%22updated%22%3A%201755915554615%2C%22info%22%3A%201755915554614%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22eportal.uestc.edu.cn%22%2C%22cuid%22%3A%20%222025090905026%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201755915554611%7D; show_vpn=0; show_fast=0; heartbeat=1; show_faq=0; wengine_vpn_ticketwebvpn_uestc_edu_cn=wrdvpn1-b9521ca22aca408ab963b22e825a0c7a; refresh=0'

# ★★★★★
# ★★★★★  每次运行前，请务必更新为一个全新的、有效的 Cookie ★★★★★
# ★★★★★
cookie_string = 'UM_distinctid=19836422886143d-02a6955f85525e8-4c657b58-144000-198364228871848; zg_did=%7B%22did%22%3A%20%2219899354b4959c-0160a58cb4d60e-4c657b58-144000-19899354b4a100e%22%7D; zg_=%7B%22sid%22%3A%201755915554611%2C%22updated%22%3A%201755915554615%2C%22info%22%3A%201755915554614%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22eportal.uestc.edu.cn%22%2C%22cuid%22%3A%20%222025090905026%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201755915554611%7D; show_vpn=0; show_fast=0; heartbeat=1; show_faq=0; wengine_vpn_ticketwebvpn_uestc_edu_cn=wrdvpn1-b9521ca22aca408ab963b22e825a0c7a; refresh=0'
# 请求头
# 我们依然提供一些必要的头信息，但 User-Agent 等指纹相关的头 curl_cffi 会自动处理
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://webvpn.uestc.edu.cn',
    'Referer': 'https://webvpn.uestc.edu.cn/https/77726476706e69737468656265737421fcf6438f26366d447b1b9de28d503021c5f4812c5427f8ff/redir.php?catalog_id=121&object_id=2737',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': cookie_string
}

# 请求体
data = {
    'cmd': 'xuexi_online'
}
# ===============================================================

# 发送请求的循环
count = 0
while True:
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_time}] 准备发送第 {count + 1} 次心跳请求 (使用 curl_cffi)...")
        
        # 发送 POST 请求
        # 关键！告诉 curl_cffi 模拟 Chrome 110 浏览器的底层指纹
        response = requests.post(url, headers=headers, data=data, timeout=20, impersonate="chrome110")
        
        # 检查响应状态码
        if response.status_code == 200:
            # 检查返回内容是否是预期的成功JSON
            if '"status":1' in response.text:
                count += 1
                print(f"[{current_time}] 请求成功! 状态码: {response.status_code}. 这是第 {count} 次成功。")
                try:
                    # 尝试美化输出JSON
                    response_json = response.json()
                    print("服务器响应内容:", json.dumps(response_json, indent=2, ensure_ascii=False))
                except json.JSONDecodeError:
                    print("服务器响应内容 (非预期的JSON):", response.text)
            else:
                # 状态码200，但内容是错误页面，说明被VPN网关拦截
                print(f"[{current_time}] 请求被拦截! 状态码: 200，但响应内容无效。")
                print("响应内容:", response.text[:200] + "...") # 打印部分错误内容
                print("!!! Cookie 可能已失效，或VPN安全策略增强。脚本停止。")
                break
        else:
            print(f"[{current_time}] 请求失败! 状态码: {response.status_code}")
            print("服务器响应内容:", response.text)
            break

    except requests.errors.RequestsError as e: # 注意这里是 requests.errors
        print(f"[{current_time}] 请求发生异常: {e}")
        print("可能是网络问题，脚本将在60秒后重试...")

    # 等待60秒
    print("\n-------------------- 等待 60 秒 --------------------\n")
    time.sleep(60)
