[app]
title = Gestor de Tarefas
package.name = gestor_tarefas
package.domain = org.carlitopj
source.dir = .
source.include_exts = py,kv,txt,png,jpg
version = 0.1

# Requirements atualizados
requirements = python3,kivy==2.2.1,pillow,hostpython3

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer

[android]
# Configurações de API para máxima compatibilidade no GitHub Actions
android.api = 31
android.minapi = 21
android.sdk = 31
android.build_tools = 31.0.0
android.ndk = 25b

# Permissões e Licenças
android.accept_sdk_license = True
android.skip_update = False

# Arquiteturas para rodar na maioria dos celulares modernos
android.archs = arm64-v8a, armeabi-v7a

# Limpeza de dependências para evitar conflitos de Gradle
android.gradle_dependencies = 
android.enable_androidx = True

# Isso ajuda a evitar o erro de memória/pipe no ambiente virtual
android.allow_backup = True
