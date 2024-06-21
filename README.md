# How to run
```
    cd {{root_dir}}
    make run
```

# build docker
```
docker build -t ms .
```

# run docker
```
docker run --rm -d -p 8080:8080 ms:latest
```

# done
加分项：（均为可选项，可酌情跳过）
- [x] 使得代码可以正确运行 （推荐 FastAPI）
- [x] 添加 test cases （推荐 pytest ）
- [x] 添加 type hint （推荐使用 mypy 之类的工具做静态类型分析）
- [x] 添加 logger
- [x] 添加 typed error 和 更可读的 error message
- [x] 按照 Clean Architecture 的形式拆分层次，并且加以适当的测试
- [x] 添加项目依赖和配置 （requirements.txt or pyproject.toml)
- [x] 使用 docker 打包项目，构建可运行镜像
- [x] 接入 Sqlite or Postgresql （ 纯SQL 或 ORM 都可以）
- [x] 改写为 Async
- [x] 添加 Authentication （ 推荐 JWT ）
- [ ] 添加 Authorization
- [ ] 添加 GraphQL 接口 （推荐 Strawberry-GraphQL ）
- [ ] 改写为 Event Driven Architecture
- [ ] 实现 CQRS 模式
