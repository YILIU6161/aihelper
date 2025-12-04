"""
使用示例脚本
演示如何使用大众点评API收集数据
"""
from config import Config
from dianping_api import DianpingAPI
from data_collector import DataCollector


def example_search_shops():
    """示例：搜索商户"""
    print("=" * 50)
    print("示例1: 搜索商户")
    print("=" * 50)
    
    try:
        Config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        print("请先配置 .env 文件")
        return
    
    api = DianpingAPI()
    collector = DataCollector(api)
    
    # 搜索商户
    shops = collector.collect_shops(
        keyword="火锅",
        city="北京",
        max_pages=2,
        page_size=20
    )
    
    print(f"\n共找到 {len(shops)} 个商户")
    
    # 保存数据
    if shops:
        flattened = collector.flatten_shop_data(shops)
        collector.save_data(flattened, filename="example_shops", data_type='shops')
    
    return shops


def example_get_shop_detail():
    """示例：获取商户详情"""
    print("\n" + "=" * 50)
    print("示例2: 获取商户详情")
    print("=" * 50)
    
    try:
        Config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        return
    
    api = DianpingAPI()
    collector = DataCollector(api)
    
    # 假设有一个商户ID
    shop_id = "12345678"  # 替换为实际的商户ID
    
    try:
        result = api.get_shop_detail(shop_id)
        detail = result.get('data', {})
        
        if detail:
            print(f"商户名称: {detail.get('name', '')}")
            print(f"地址: {detail.get('address', '')}")
            print(f"评分: {detail.get('rating', '')}")
            
            # 保存数据
            collector.save_data([detail], filename="example_shop_detail", data_type='shop_detail')
        else:
            print("未找到商户详情")
    except Exception as e:
        print(f"获取商户详情失败: {str(e)}")


def example_collect_reviews():
    """示例：收集评论"""
    print("\n" + "=" * 50)
    print("示例3: 收集商户评论")
    print("=" * 50)
    
    try:
        Config.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        return
    
    api = DianpingAPI()
    collector = DataCollector(api)
    
    # 假设有一个商户ID
    shop_id = "12345678"  # 替换为实际的商户ID
    
    reviews = collector.collect_shop_reviews(
        shop_id=shop_id,
        max_pages=3,
        page_size=20
    )
    
    print(f"\n共收集到 {len(reviews)} 条评论")
    
    # 保存数据
    if reviews:
        collector.save_data(reviews, filename="example_reviews", data_type='reviews')


if __name__ == '__main__':
    print("大众点评数据收集工具 - 使用示例\n")
    
    # 运行示例
    # example_search_shops()
    # example_get_shop_detail()
    # example_collect_reviews()
    
    print("\n提示: 取消注释上面的示例函数来运行它们")
    print("注意: 需要先配置 .env 文件中的 API 密钥")

