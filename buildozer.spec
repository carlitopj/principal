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
android.api = 33
android.minapi = 21
android.sdk = 33
android.build_tools = 33.0.2
android.ndk = 25c

android.accept_sdk_license = True
android.skip_update = False
android.archs = arm64-v8a

android.gradle_dependencies = 
android.enable_androidx = True
android.allow_backup = True