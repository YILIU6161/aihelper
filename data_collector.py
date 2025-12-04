"""
数据收集和存储模块
"""
import os
import json
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from config import Config
from dianping_api import DianpingAPI


class DataCollector:
    """数据收集器"""
    
    def __init__(self, api_client: DianpingAPI = None):
        """
        初始化数据收集器
        
        Args:
            api_client: API客户端实例
        """
        self.api = api_client or DianpingAPI()
        self.data_dir = Config.DATA_DIR
        self.output_format = Config.OUTPUT_FORMAT
        
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
    
    def collect_shops(self,
                     keyword: str = None,
                     city: str = None,
                     category: str = None,
                     region: str = None,
                     max_pages: int = 10,
                     page_size: int = 20) -> List[Dict[str, Any]]:
        """
        收集商户信息
        
        Args:
            keyword: 搜索关键词
            city: 城市名称
            category: 分类
            region: 区域
            max_pages: 最大收集页数
            page_size: 每页数量
            
        Returns:
            商户信息列表
        """
        all_shops = []
        
        for page in range(1, max_pages + 1):
            try:
                result = self.api.search_shops(
                    keyword=keyword,
                    city=city,
                    category=category,
                    region=region,
                    page=page,
                    page_size=page_size
                )
                
                # 根据实际API响应结构调整
                shops = result.get('data', {}).get('shops', [])
                if not shops:
                    break
                    
                all_shops.extend(shops)
                print(f"已收集第 {page} 页，共 {len(shops)} 个商户")
                
            except Exception as e:
                print(f"收集第 {page} 页时出错: {str(e)}")
                break
        
        return all_shops
    
    def collect_shop_details(self, shop_ids: List[str]) -> List[Dict[str, Any]]:
        """
        收集商户详情
        
        Args:
            shop_ids: 商户ID列表
            
        Returns:
            商户详情列表
        """
        details = []
        
        for shop_id in shop_ids:
            try:
                result = self.api.get_shop_detail(shop_id)
                detail = result.get('data', {})
                if detail:
                    details.append(detail)
                print(f"已收集商户 {shop_id} 的详情")
            except Exception as e:
                print(f"收集商户 {shop_id} 详情时出错: {str(e)}")
        
        return details
    
    def collect_shop_reviews(self,
                            shop_id: str,
                            max_pages: int = 5,
                            page_size: int = 20) -> List[Dict[str, Any]]:
        """
        收集商户评论
        
        Args:
            shop_id: 商户ID
            max_pages: 最大收集页数
            page_size: 每页数量
            
        Returns:
            评论列表
        """
        all_reviews = []
        
        for page in range(1, max_pages + 1):
            try:
                result = self.api.get_shop_reviews(
                    shop_id=shop_id,
                    page=page,
                    page_size=page_size
                )
                
                reviews = result.get('data', {}).get('reviews', [])
                if not reviews:
                    break
                    
                all_reviews.extend(reviews)
                print(f"已收集第 {page} 页评论，共 {len(reviews)} 条")
                
            except Exception as e:
                print(f"收集第 {page} 页评论时出错: {str(e)}")
                break
        
        return all_reviews
    
    def save_data(self, data: List[Dict[str, Any]], filename: str = None, data_type: str = 'shops'):
        """
        保存数据到文件
        
        Args:
            data: 要保存的数据
            filename: 文件名（可选）
            data_type: 数据类型（用于生成默认文件名）
        """
        if not data:
            print("没有数据需要保存")
            return
        
        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{data_type}_{timestamp}"
        
        filepath = os.path.join(self.data_dir, filename)
        
        # 根据格式保存
        if self.output_format == 'json':
            filepath += '.json'
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        elif self.output_format == 'csv':
            filepath += '.csv'
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        elif self.output_format == 'xlsx':
            filepath += '.xlsx'
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False, engine='openpyxl')
        
        print(f"数据已保存到: {filepath}")
        print(f"共保存 {len(data)} 条记录")
    
    def flatten_shop_data(self, shops: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        扁平化商户数据（便于导出到Excel/CSV）
        
        Args:
            shops: 商户数据列表
            
        Returns:
            扁平化后的数据列表
        """
        flattened = []
        
        for shop in shops:
            flat_shop = {
                'shop_id': shop.get('shop_id', ''),
                'name': shop.get('name', ''),
                'address': shop.get('address', ''),
                'phone': shop.get('phone', ''),
                'rating': shop.get('rating', ''),
                'review_count': shop.get('review_count', 0),
                'price': shop.get('price', ''),
                'category': shop.get('category', ''),
                'region': shop.get('region', ''),
                'latitude': shop.get('latitude', ''),
                'longitude': shop.get('longitude', ''),
                'open_time': shop.get('open_time', ''),
                'url': shop.get('url', ''),
            }
            flattened.append(flat_shop)
        
        return flattened

