"""
大众点评API调用模块
"""
import time
import hashlib
import hmac
import urllib.parse
import requests
from typing import Dict, List, Optional, Any
from config import Config


class DianpingAPI:
    """大众点评API客户端"""
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        """
        初始化API客户端
        
        Args:
            api_key: API密钥
            api_secret: API密钥
        """
        self.api_key = api_key or Config.API_KEY
        self.api_secret = api_secret or Config.API_SECRET
        self.base_url = Config.BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        生成API签名
        
        Args:
            params: 请求参数
            
        Returns:
            签名字符串
        """
        # 按参数名排序
        sorted_params = sorted(params.items())
        # 构建查询字符串
        query_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
        # 添加密钥
        sign_string = f"{query_string}&key={self.api_secret}"
        # 生成MD5签名
        signature = hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()
        return signature
    
    def _build_request_params(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建请求参数
        
        Args:
            method: API方法名
            params: 业务参数
            
        Returns:
            完整的请求参数
        """
        request_params = {
            'appkey': self.api_key,
            'method': method,
            'timestamp': str(int(time.time())),
            'format': 'json',
            'v': '1.0',
            **params
        }
        
        # 生成签名
        request_params['sign'] = self._generate_signature(request_params)
        return request_params
    
    def _make_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送API请求
        
        Args:
            method: API方法名
            params: 业务参数
            
        Returns:
            API响应数据
        """
        request_params = self._build_request_params(method, params)
        
        try:
            response = requests.post(
                self.base_url,
                data=request_params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def search_shops(self, 
                     keyword: str = None,
                     city: str = None,
                     category: str = None,
                     region: str = None,
                     page: int = 1,
                     page_size: int = 20) -> Dict[str, Any]:
        """
        搜索商户
        
        Args:
            keyword: 搜索关键词
            city: 城市名称
            category: 分类
            region: 区域
            page: 页码
            page_size: 每页数量
            
        Returns:
            商户列表数据
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        
        if keyword:
            params['keyword'] = keyword
        if city:
            params['city'] = city
        if category:
            params['category'] = category
        if region:
            params['region'] = region
            
        return self._make_request('shop.search', params)
    
    def get_shop_detail(self, shop_id: str) -> Dict[str, Any]:
        """
        获取商户详情
        
        Args:
            shop_id: 商户ID
            
        Returns:
            商户详情数据
        """
        params = {'shop_id': shop_id}
        return self._make_request('shop.getDetail', params)
    
    def get_shop_reviews(self, 
                        shop_id: str,
                        page: int = 1,
                        page_size: int = 20) -> Dict[str, Any]:
        """
        获取商户评论
        
        Args:
            shop_id: 商户ID
            page: 页码
            page_size: 每页数量
            
        Returns:
            评论列表数据
        """
        params = {
            'shop_id': shop_id,
            'page': page,
            'page_size': page_size
        }
        return self._make_request('review.getList', params)
    
    def search_deals(self,
                    city: str = None,
                    category: str = None,
                    page: int = 1,
                    page_size: int = 20) -> Dict[str, Any]:
        """
        搜索团购/优惠
        
        Args:
            city: 城市名称
            category: 分类
            page: 页码
            page_size: 每页数量
            
        Returns:
            团购列表数据
        """
        params = {
            'page': page,
            'page_size': page_size
        }
        
        if city:
            params['city'] = city
        if category:
            params['category'] = category
            
        return self._make_request('deal.search', params)
    
    def get_categories(self, city: str = None) -> Dict[str, Any]:
        """
        获取分类列表
        
        Args:
            city: 城市名称
            
        Returns:
            分类列表数据
        """
        params = {}
        if city:
            params['city'] = city
        return self._make_request('category.getList', params)

