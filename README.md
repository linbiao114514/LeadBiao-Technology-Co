# 领飚渗透助手 - Android移动版

## 项目简介
领飚渗透助手的Android移动版，保留核心查询功能，支持悬浮窗快捷操作。

## 技术栈
- **Kivy** - Python跨平台UI框架
- **Buildozer** - APK打包工具
- **GitHub Actions** - 云端自动编译

## 项目结构
```
lingbiao-mobile/
├── main.py                    # 应用入口
├── buildozer.spec             # 构建配置
├── requirements.txt           # Python依赖
├── .github/
│   └── workflows/
│       └── android.yml        # CI/CD配置
└── mobile_app/
    ├── main.py               # App主类
    ├── ui/                   # 界面组件
    ├── services/             # 服务模块
    └── widgets/              # 自定义组件
```

## 开发流程
1. 用Trae编辑代码
2. GitHub Desktop提交并推送
3. 等待GitHub Actions编译（5-10分钟）
4. 下载APK文件
5. QQ传到手机安装测试

## 注意事项
- Windows需要通过GitHub Actions云端编译APK
- 首次编译需要配置Buildozer账号（免费）
