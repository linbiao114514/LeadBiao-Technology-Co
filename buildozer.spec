[app]
title = 领飚渗透助手
package.name = lingbiaomobile
package.domain = org.lingbiao
source.dir = .
version = 0.1.0
requirements = python3,kivy==2.2.1,requests,urllib3
orientation = portrait
fullscreen = 0
android.api = 34
android.minapi = 24
android.sdk = 34
android.archs = arm64-v8a
android.permissions = INTERNET,ACCESS_NETWORK_STATE,SYSTEM_ALERT_WINDOW
android.enable_androidx = True
android.use_legacy_gradle_env = True

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True
android.log_level = debug
