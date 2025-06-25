# DHL 发货自动生成系统 v5

一个智能的 DHL 发货 CSV 文件生成器，采用精确匹配逻辑，能够自动记忆和填充海关编码、重量和产地信息，支持 UK Tariff API 查询。

## 🚀 主要功能

### 智能匹配系统
- **精确匹配 (Exact Match)**: 只有当 Item Description 完全相同时才从数据库调取数据
- **海关编码 (Commodity Code)**: 自动匹配和填充 HS 编码，支持 UK Tariff API 查询
- **重量 (Weight)**: 从数据库调取或手动填写
- **产地 (Origin Country)**: 从数据库调取或手动填写

### 匹配逻辑
1. **精确匹配** - 只有当 Item Description 完全相同时才算匹配
2. **API 查询** - 本地找不到 Commodity Code 时自动调用 UK Tariff API
3. **手动补全** - 未匹配的商品留空，等待用户手动填写

## 📋 使用方法

### 1. 上传订单文件
- 支持 CSV、Excel (.xlsx, .xls) 格式
- 必须包含两列：`Item Description` 和 `Selling Price`

### 2. 匹配检查
- 系统自动检查本地 SKU 数据库
- 显示匹配统计：找到 X 条 exact match，Y 条未找到
- 未匹配的商品字段留空，等待用户填写

### 3. 手动补全
- 在可编辑表格中补全未匹配商品的 Weight、Origin Country、Commodity Code
- 勾选需要写入 SKU 数据库的行

### 4. 提交并导出
- 点击"提交并导出 DHL 文件"
- 自动写入 SKU 数据库
- 导出新添加的商品数据（new_sku_records.csv）
- 生成 DHL_ready_file.csv

## 🗄️ SKU 数据库

### 文件位置
`sku_reference_data.csv`

### 数据格式
```csv
Item Description,Commodity Code,Weight,Origin Country
LV SPEEDY BAG,42022100,0.9,CN
GUCCI BELT,4203301000,0.3,IT
```

### 数据库更新
- **自动更新**: 勾选"写入 SKU 数据库"后自动追加
- **手动下载**: 侧边栏可随时下载当前数据库
- **新数据导出**: 每次提交后导出新添加的商品数据

## 🔧 技术特性

### 精确匹配算法
- 使用 Item Description 的完全匹配
- 区分大小写，去除首尾空格
- 只有完全匹配才调取数据库数据

### UK Tariff API 集成
- 自动调用 UK Tariff API 查询 Commodity Code
- API 地址：https://www.trade-tariff.service.gov.uk/api/v2
- 本地找不到时自动查询

### 数据格式化
- Commodity Code 自动格式化为 xxxx.xx.xx
- Unique Item Number 固定为 1
- 严格按 DHL 官方要求生成 CSV

## 📦 安装和运行

### 依赖安装
```bash
pip install streamlit pandas openpyxl requests
```

### 运行应用
```bash
streamlit run app.py
```

## 🎯 使用场景

### 适合的用户
- 经常处理 DHL 发货的电商卖家
- 需要精确匹配商品信息的用户
- 希望提高工作效率的物流人员

### 工作流程
1. 上传包含 Item Description 和 Selling Price 的订单文件
2. 系统检查精确匹配，显示匹配统计
3. 手动补全未匹配商品的信息
4. 勾选需要记忆的商品，提交并导出
5. 系统自动记忆，下次遇到相同商品时自动填充

## 🔄 数据管理

### 自动保存
- 每次提交时自动保存到 SKU 数据库
- 支持增量更新，不会覆盖现有数据
- 导出新添加的商品数据便于备份

### 数据安全
- 支持随时下载 SKU 数据库备份
- 数据格式简单，易于理解和维护
- 云端部署时建议定期备份

## 📈 性能优化

### 匹配效率
- 使用精确匹配，避免误匹配
- 优先本地查找，减少 API 调用
- 按需加载数据，提高响应速度

### 用户体验
- 实时显示匹配统计
- 清晰的未匹配项提示
- 一键下载新添加数据

## 🛠️ 自定义配置

### 修改 API 查询
编辑 `utils.py` 中的 `query_uk_tariff_api` 函数

### 调整匹配逻辑
修改 `app.py` 中的 `exact_match_lookup` 函数

### 添加国家代码
修改表格中的 Origin Country 选项

## 📞 支持

如有问题或建议，请检查：
1. 文件格式是否正确（必须包含 Item Description 和 Selling Price）
2. SKU 数据库是否正常
3. 网络连接是否正常（API 查询需要）

---

**版本**: 5.0  
**更新日期**: 2024  
**功能**: 精确匹配系统 + UK Tariff API + DHL CSV 生成# DHL-CSV-Generator-v5
