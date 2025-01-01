# fire-city

适合躺平fire的城市信息管理系统

## 项目简介
本项目旨在帮助用户了解和管理各个城市的宜居信息，包括城市基本信息、生活配套、房价等数据，帮助用户选择适合自己的城市。

## 功能特性
- 用户管理
  - 用户注册
  - 用户登录
  - 用户退出
  - 密码修改
- 城市信息管理
  - 录入城市信息
  - 修改城市信息
  - 删除城市信息
  - 查询城市信息
- 城市数据展示
  - 首页热门城市展示
  - 城市列表页
  - 城市详情页

## 技术栈
- 后端：Python 3.11 + Flask
- 数据库：MySQL 5.7.44
- 前端：HTML + CSS + JavaScript

## 项目结构
```
fire-city/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用初始化
│   ├── models/            # 数据模型
│   ├── routes/            # 路由控制器
│   ├── services/          # 业务逻辑
│   ├── static/            # 静态文件
│   └── templates/         # 模板文件
├── config/                # 配置文件
├── tests/                 # 单元测试
├── docs/                  # 文档
└── requirements.txt       # 项目依赖
```

## 安装部署
1. 克隆项目
```bash
git clone https://github.com/wuleying/fire-city.git
cd fire-city
```

2. 创建虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Windows使用: venv\Scripts\activate
pip install -r requirements.txt
```

3. 配置数据库
- 创建MySQL数据库
- 修改config/config.py中的数据库配置

4. 运行项目
```bash
python run.py
```

## 开发团队
- [@wuleying](https://github.com/wuleying)

## 开源协议
本项目采用 MIT 协议开源，详见 [LICENSE](./LICENSE)
