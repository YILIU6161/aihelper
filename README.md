# 大众点评数据收集工具

一个用于快速收集大众点评相关信息的命令行工具，支持搜索商户、获取商户详情、收集评论等功能。

## 功能特性

- 🔍 **商户搜索**: 支持按关键词、城市、分类、区域搜索商户
- 📋 **商户详情**: 获取商户的详细信息
- 💬 **评论收集**: 批量收集商户评论数据
- 💾 **数据导出**: 支持导出为 Excel、CSV、JSON 格式
- 🎨 **美观界面**: 使用 Rich 库提供美观的命令行界面

## 安装

### 1. 克隆或下载项目

```bash
cd /Users/liuyi/Code/aihelper
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

复制 `.env.example` 文件为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的大众点评API密钥：

```env
DIANPING_API_KEY=your_api_key_here
DIANPING_API_SECRET=your_api_secret_here
DIANPING_BASE_URL=https://api.dianping.com
```

## 使用方法

### 搜索商户

```bash
# 基本搜索
python main.py search -k "火锅" -c "北京"

# 带更多参数
python main.py search -k "川菜" -c "上海" --category "美食" --region "黄浦区" --max-pages 5

# 搜索并保存结果
python main.py search -k "咖啡" -c "深圳" -s -o "coffee_shops"
```

参数说明：
- `-k, --keyword`: 搜索关键词
- `-c, --city`: 城市名称
- `--category`: 分类
- `-r, --region`: 区域
- `--max-pages`: 最大收集页数（默认：10）
- `--page-size`: 每页数量（默认：20）
- `-s, --save`: 保存结果到文件
- `-o, --output`: 输出文件名（不含扩展名）

### 获取商户详情

```bash
# 获取商户详情
python main.py detail <shop_id>

# 获取并保存
python main.py detail <shop_id> -s -o "shop_detail"
```

### 获取商户评论

```bash
# 获取评论
python main.py reviews <shop_id>

# 获取更多评论并保存
python main.py reviews <shop_id> --max-pages 10 --page-size 50 -s
```

## 输出格式

数据默认保存在 `data/` 目录下，支持以下格式：

- **Excel** (.xlsx): 默认格式，适合数据分析
- **CSV** (.csv): 通用格式，易于导入其他工具
- **JSON** (.json): 结构化数据，适合程序处理

可以通过修改 `.env` 文件中的 `OUTPUT_FORMAT` 来更改默认格式。

## 项目结构

```
aihelper/
├── main.py              # 主入口文件
├── cli.py               # 命令行界面
├── dianping_api.py      # 大众点评API调用模块
├── data_collector.py    # 数据收集和存储模块
├── config.py            # 配置管理
├── requirements.txt     # 依赖包列表
├── .env.example         # 环境变量示例
├── .gitignore          # Git忽略文件
├── README.md           # 项目说明
└── data/               # 数据输出目录（自动创建）
```

## 注意事项

1. **API密钥**: 请确保你有有效的大众点评API密钥和密钥
2. **API限制**: 注意API的调用频率限制，避免过于频繁的请求
3. **数据格式**: API返回的数据格式可能与示例不同，需要根据实际API文档调整
4. **错误处理**: 如果遇到API错误，请检查网络连接和API密钥配置

## 开发说明

### API签名算法

本工具实现了大众点评API的标准签名算法：
1. 将参数按key排序
2. 构建查询字符串
3. 添加密钥
4. 生成MD5签名

### 扩展功能

你可以通过以下方式扩展功能：

1. **添加新的API方法**: 在 `dianping_api.py` 中添加新的方法
2. **自定义数据收集**: 在 `data_collector.py` 中添加新的收集函数
3. **添加新的命令**: 在 `cli.py` 中添加新的子命令

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

# aihelper
