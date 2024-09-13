<div align="center" >
  <img src="docs/assets/images/Baguette Bread.png" width="180">
  <h1>
    FasAPI-Bread v1.0.0 <img src="docs/assets/images/Waving Hand Medium-Light Skin Tone.png" width="45px">
  </h1>
</div>


<p align="center" >
  <a href="">
      <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" height="25">
  </a>
  <a href="https://fastapi.tiangolo.com">
      <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" height="25">
  </a>
  <a href="https://docs.pydantic.dev/2.4/">
      <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=for-the-badge" alt="Pydantic" height="25">
  </a>
  <a href="https://www.mysql.org">
      <img src="https://img.shields.io/badge/MySQL-316192?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" height="25">
  </a>
  <a href="https://redis.io">
      <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=fff&style=for-the-badge" alt="Redis" height="25">
  </a>
  <a href="https://docs.docker.com/compose/">
      <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge" alt="Docker" height="25">
  </a>
  <a href="https://nginx.org/en/">
      <img src="https://img.shields.io/badge/NGINX-009639?logo=nginx&logoColor=fff&style=for-the-badge" alt=NGINX height="25">
  </a>
</p>


> 由于微服务个人来做能力实在有限，缓慢开发功能...

<img align='right' src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="280">

#### <img src="docs/assets/images/Party Popper.png" width="30"> 技术栈

- <img src="docs/assets/images/Fire.png" width="17">&nbsp;&nbsp;**Fully Async**
- <img src="docs/assets/images/Cyclone.png" width="16">&nbsp;&nbsp;**SQLAlchemy 2.0**
- <img src="docs/assets/images/School.png" width="17">&nbsp;&nbsp;**Pydantic V2**
- <img src="docs/assets/images/Flexed Biceps Light Skin Tone.png" width="17">&nbsp;&nbsp;**Powerful CRUD Functionality**
- <img src="docs/assets/images/Locked with Key.png" width="18">&nbsp;&nbsp;**User authentication with JWT**
- <img src="docs/assets/images/Police Car.png" width="19">&nbsp;&nbsp;**Easy running with docker compose**

#### <img src="docs/assets/images/Hot Beverage.png" width="25"> 说明

> `-` 表示没有，端口代表占用本机端口，请自行保证端口未被占用

| 软件    | 版本                           | 端口         | 默认用户  | 默认密码     | 类型     | 作用                           |
|-------|------------------------------|------------|-------|----------|--------|------------------------------|
| MySQL | 8.0.27                       | 3306       | root  | mysql123 | 关系型数据库 | 用于存储和管理结构化数据的数据库管理系统。        |
| Redis | 6.2.6                        | 6379       | -     | -        | 键值存储   | 内存数据结构存储，用作数据库、缓存和消息代理。      |
| Minio | RELEASE.2023-02-09T05-16-53Z | 9000, 9001 | minio | minio123 | 对象存储   | 高性能对象存储服务器，兼容 Amazon S3 API。 |

#### <img src="docs/assets/images/Spouting Whale.png" width="25"> Docker部署

1. 安装Docker
2. 打开终端并进入根目录
3. 执行以下命令，安静等待启动即可（docker-compose 一键部署）

```shell
docker-compose -f docker-compose.yml up -d
```

#### <img src="docs/assets/images/Eyes.png" width="25"> 提交规范

```shell
# black 格式化代码
black . 
isort . --profile black 

# 或使用 ruff pre-commit
pip install ruff
pre-commit install
# 手动运行全部检查
pre-commit run --all-files

git add .
git commit -m "✨ feat: 添加新功能"
git push origin main
```

#### <img src="docs/assets/images/Bookmark Tabs.png" width="24"> 许可证

[`MIT`](LICENSE)

#### <img src="docs/assets/images/Robot.png" width="25"> 作者介绍

    大家好，我是 wieszheng，一个乐于分享，喜欢钻研技术的测试开发工程师。

    一个打游戏不拿首胜不睡觉的酒0后。

#### <img src="docs/assets/images/Heart on Fire.png" width="25"> 喜欢我？

<p align="center">
<a href="https://star-history.com/#wieszheng/bread">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=wieszheng/bread&type=Date&title=50&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=wieszheng/bread&type=Date&title=50" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=wieszheng/bread&type=Date" />
  </picture>
</a>
</p>

<div align="center">
  <img src="docs/assets/images/Glowing Star.png" width="25"> 
  <img src="docs/assets/images/Birthday Cake.png" width="23"> 
  <img src="docs/assets/images/Glowing Star.png" width="25">
</div>
