"""
命令行界面
"""
import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from config import Config
from dianping_api import DianpingAPI
from data_collector import DataCollector

console = Console()


def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔═══════════════════════════════════════╗
    ║   大众点评数据收集工具                ║
    ║   Dianping Data Collector            ║
    ╚═══════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan"))


def search_shops(args):
    """搜索商户"""
    try:
        Config.validate()
    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        console.print("[yellow]请先配置 .env 文件中的 API 密钥[/yellow]")
        return
    
    api = DianpingAPI()
    collector = DataCollector(api)
    
    console.print(f"[cyan]开始搜索商户...[/cyan]")
    console.print(f"关键词: {args.keyword or '无'}")
    console.print(f"城市: {args.city or '无'}")
    console.print(f"分类: {args.category or '无'}")
    console.print(f"区域: {args.region or '无'}")
    console.print()
    
    shops = collector.collect_shops(
        keyword=args.keyword,
        city=args.city,
        category=args.category,
        region=args.region,
        max_pages=args.max_pages,
        page_size=args.page_size
    )
    
    if shops:
        # 显示结果表格
        table = Table(title="搜索结果", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("名称")
        table.add_column("地址", style="cyan")
        table.add_column("评分", justify="right")
        table.add_column("评论数", justify="right")
        
        for shop in shops[:10]:  # 只显示前10个
            table.add_row(
                str(shop.get('shop_id', '')),
                shop.get('name', '')[:30],
                shop.get('address', '')[:30],
                str(shop.get('rating', '')),
                str(shop.get('review_count', 0))
            )
        
        console.print(table)
        
        if len(shops) > 10:
            console.print(f"[dim]... 还有 {len(shops) - 10} 个结果未显示[/dim]")
        
        # 保存数据
        if args.save:
            flattened = collector.flatten_shop_data(shops)
            collector.save_data(flattened, filename=args.output, data_type='shops')
    else:
        console.print("[yellow]未找到相关商户[/yellow]")


def get_shop_detail(args):
    """获取商户详情"""
    try:
        Config.validate()
    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        return
    
    api = DianpingAPI()
    collector = DataCollector(api)
    
    console.print(f"[cyan]正在获取商户 {args.shop_id} 的详情...[/cyan]")
    
    try:
        result = api.get_shop_detail(args.shop_id)
        detail = result.get('data', {})
        
        if detail:
            # 显示详情
            info = f"""
商户名称: {detail.get('name', '')}
地址: {detail.get('address', '')}
电话: {detail.get('phone', '')}
评分: {detail.get('rating', '')}
评论数: {detail.get('review_count', 0)}
价格: {detail.get('price', '')}
分类: {detail.get('category', '')}
营业时间: {detail.get('open_time', '')}
            """
            console.print(Panel(info, title="商户详情", border_style="green"))
            
            # 保存数据
            if args.save:
                collector.save_data([detail], filename=args.output, data_type='shop_detail')
        else:
            console.print("[yellow]未找到商户详情[/yellow]")
            
    except Exception as e:
        console.print(f"[red]获取商户详情失败: {str(e)}[/red]")


def get_reviews(args):
    """获取商户评论"""
    try:
        Config.validate()
    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        return
    
    api = DianpingAPI()
    collector = DataCollector(api)
    
    console.print(f"[cyan]正在收集商户 {args.shop_id} 的评论...[/cyan]")
    
    reviews = collector.collect_shop_reviews(
        shop_id=args.shop_id,
        max_pages=args.max_pages,
        page_size=args.page_size
    )
    
    if reviews:
        # 显示评论表格
        table = Table(title="评论列表", show_header=True, header_style="bold magenta")
        table.add_column("用户", style="cyan")
        table.add_column("评分", justify="right")
        table.add_column("评论内容", style="dim")
        table.add_column("时间", style="dim")
        
        for review in reviews[:10]:  # 只显示前10条
            content = review.get('content', '')
            if len(content) > 50:
                content = content[:50] + '...'
            table.add_row(
                review.get('user_name', ''),
                str(review.get('rating', '')),
                content,
                review.get('date', '')
            )
        
        console.print(table)
        
        if len(reviews) > 10:
            console.print(f"[dim]... 还有 {len(reviews) - 10} 条评论未显示[/dim]")
        
        # 保存数据
        if args.save:
            collector.save_data(reviews, filename=args.output, data_type='reviews')
    else:
        console.print("[yellow]未找到评论[/yellow]")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='大众点评数据收集工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 搜索商户命令
    search_parser = subparsers.add_parser('search', help='搜索商户')
    search_parser.add_argument('-k', '--keyword', help='搜索关键词')
    search_parser.add_argument('-c', '--city', help='城市名称')
    search_parser.add_argument('--category', help='分类')
    search_parser.add_argument('-r', '--region', help='区域')
    search_parser.add_argument('--max-pages', type=int, default=10, help='最大页数 (默认: 10)')
    search_parser.add_argument('--page-size', type=int, default=20, help='每页数量 (默认: 20)')
    search_parser.add_argument('-s', '--save', action='store_true', help='保存结果到文件')
    search_parser.add_argument('-o', '--output', help='输出文件名（不含扩展名）')
    search_parser.set_defaults(func=search_shops)
    
    # 获取商户详情命令
    detail_parser = subparsers.add_parser('detail', help='获取商户详情')
    detail_parser.add_argument('shop_id', help='商户ID')
    detail_parser.add_argument('-s', '--save', action='store_true', help='保存结果到文件')
    detail_parser.add_argument('-o', '--output', help='输出文件名（不含扩展名）')
    detail_parser.set_defaults(func=get_shop_detail)
    
    # 获取评论命令
    review_parser = subparsers.add_parser('reviews', help='获取商户评论')
    review_parser.add_argument('shop_id', help='商户ID')
    review_parser.add_argument('--max-pages', type=int, default=5, help='最大页数 (默认: 5)')
    review_parser.add_argument('--page-size', type=int, default=20, help='每页数量 (默认: 20)')
    review_parser.add_argument('-s', '--save', action='store_true', help='保存结果到文件')
    review_parser.add_argument('-o', '--output', help='输出文件名（不含扩展名）')
    review_parser.set_defaults(func=get_reviews)
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return
    
    print_banner()
    args.func(args)


if __name__ == '__main__':
    main()

