[app]
title = Gestor de Tarefas
package.name = gestor_tarefas
package.domain = org.carlitopj
source.dir = .
source.include_exts = py,kv,txt
requirements = python3,kivy
orientation = portrait
fullscreen = 0
version = 0.1

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer

[android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = armeabi-v7a
android.build_tools = 33.0.2
# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
