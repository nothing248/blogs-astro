import requests
import json
import pandas as pd

class CloudflareAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def get_zone_id(self, domain):
        """获取域名的zone_id"""
        url = f"{self.base_url}/zones"
        params = {"name": domain}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["success"] and len(data["result"]) > 0:
                return data["result"][0]["id"]
        return None

    def create_dns_record(self, zone_id, record_type, name, content, proxied=False, ttl=1):
        """创建DNS记录
        Args:
            zone_id: 域名zone ID
            record_type: 记录类型(A, AAAA, CNAME, TXT等)
            name: 记录名称
            content: 记录内容
            proxied: 是否开启CDN代理
            ttl: TTL值(1为自动)
        """
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        data = {
            "type": record_type,
            "name": name,
            "content": content,
            "proxied": proxied,
            "ttl": ttl
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def batch_create_dns_records(self, zone_id, records):
        """批量创建DNS记录
        Args:
            zone_id: 域名zone ID
            records: 记录列表，每条记录为一个字典，包含以下字段:
                    - record_type: 记录类型(A, AAAA, CNAME, TXT等)
                    - name: 记录名称
                    - content: 记录内容
                    - proxied: 是否开启CDN代理(可选，默认False)
                    - ttl: TTL值(可选，默认1)
        Returns:
            包含所有创建结果的列表
        """
        results = []
        for record in records:
            result = self.create_dns_record(
                zone_id=zone_id,
                record_type=record['record_type'],
                name=record['name'],
                content=record['content'],
                proxied=record.get('proxied', False),
                ttl=record.get('ttl', 1)
            )
            results.append(result)
        return results

    def update_dns_record(self, zone_id, record_id, record_type, name, content, proxied=False, ttl=1):
        """更新DNS记录"""
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}"
        data = {
            "type": record_type,
            "name": name,
            "content": content,
            "proxied": proxied,
            "ttl": ttl
        }
        
        response = requests.put(url, headers=self.headers, json=data)
        return response.json()

    def delete_dns_record(self, zone_id, record_id):
        """删除DNS记录"""
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}"
        response = requests.delete(url, headers=self.headers)
        return response.json()

    def list_dns_records(self, zone_id):
        """列出所有DNS记录"""
        url = f"{self.base_url}/zones/{zone_id}/dns_records"
        response = requests.get(url, headers=self.headers)
        return response.json()

# 使用示例
if __name__ == "__main__":
    # 初始化API客户端
    cf = CloudflareAPI("nbXHqu0OEcGv450aSTrmR67UnChTJFm-Kc_xexeo")
    
    # 获取域名的zone_id
    zone_id = cf.get_zone_id("sxyxy.top")
    
    if zone_id:
        # 读取Excel文件
        df = pd.read_excel('./scripts/sxyxy_top.xlsx')
        
        # 将DataFrame转换为records列表
        records = []
        for _, row in df.iterrows():
            record = {
                'record_type': row['记录类型'],
                'name': row['域名'], 
                'content': row['记录值']
            }
            
            # 可选字段
            if 'proxied' in row:
                record['proxied'] = bool(row['proxied'])
            if 'TTL值(秒)' in row:
                record['ttl'] = int(row['TTL值(秒)'])
                
            records.append(record)
        results = cf.batch_create_dns_records(zone_id, records)
        for result in results:
            print(json.dumps(result, indent=2))
