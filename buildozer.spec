[app]
title = Gestor de Tarefas
package.name = gestor_tarefas
package.domain = org.carlitopj
source.dir = .
source.include_exts = py,kv,txt,png,jpg
version = 0.1

requirements = python3,kivy==2.2.1,pillow

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer

[android]
android.api = 31
android.minapi = 21
android.sdk = 31
android.build_tools = 31.0.0
android.ndk = 25.1.8937393

android.accept_sdk_license = True
android.skip_update = False

android.archs = arm64-v8a

android.gradle_dependencies = 
android.enable_androidx = True
android.allow_backup = True
android.skip_lint = True
android.logcat_filters = *:S python:D