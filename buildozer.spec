[app]
# Informações do aplicativo
title = Gestor de Tarefas
package.name = gestor_tarefas
package.domain = org.carlitopj

# Diretório e arquivos incluídos
source.dir = .
source.include_exts = py,kv,txt,png,jpg

# Versão do app
version = 0.1

# Dependências Python necessárias
requirements = python3,kivy==2.2.1,pillow

# Configurações visuais
orientation = portrait
fullscreen = 0

[buildozer]
# Configurações gerais do Buildozer
log_level = 2
warn_on_root = 1

[android]
# API alvo e mínima
android.api = 33
android.minapi = 21
android.sdk = 33
android.build_tools = 33.0.2

# Versão do NDK
android.ndk = 25b

# Permissões (adicione conforme necessário)
android.accept_sdk_license = True
# Pular a atualização automática do SDK (evita que ele busque a v37)
android.skip_update = False

# Arquitetura alvo
android.archs = armeabi-v7a, arm64-v8a

# Garante que o Gradle use o Java 17 (padrão do GitHub Actions atual)
android.gradle_dependencies =

[buildozer]
# Pasta de build para cache
build_dir = ./.buildozer

# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
