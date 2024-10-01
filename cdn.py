import requests

# Cloudflare API凭据
API_TOKEN = 'cf_token'
ZONE_ID = '域名ID'
DOMAIN_NAME = 'your_domain'

def delete_cdn_records():
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    records = response.json().get('result', [])
    
    for record in records:
        if record['name'] == 'cdn.your_domain' and record['type'] == 'A':
            delete_url = f"{url}/{record['id']}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 200:
                print(f"成功删除记录: {record['content']}")
            else:
                print(f"删除记录失败: {delete_response.json()}")

def add_a_record(ip_address):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': 'cdn',
        'content': ip_address,
        'ttl': 1,  # 自动 TTL
        'proxied': False
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"成功添加记录: {ip_address}")
    else:
        print(f"添加记录失败: {response.json()}")

def main():
    delete_cdn_records()  # 删除现有 'cdn' A 记录
    with open('ip.txt', 'r') as file:
        for line in file:
            ip_address = line.strip()
            add_a_record(ip_address)

if __name__ == "__main__":
    main()

