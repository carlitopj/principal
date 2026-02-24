[app]
# Informações do aplicativo
title = Gestor de Tarefas
package.name = gestor_tarefas
package.domain = org.carlitopj

# Diretório e arquivos incluídos
source.dir = .
source.include_exts = py,kv,txt

# Versão do app
version = 0.1

# Dependências Python necessárias
requirements = python3,kivy

# Configurações visuais
orientation = portrait
fullscreen = 0

# Ícone e tela de abertura (opcional)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

[buildozer]
# Configurações gerais do Buildozer
log_level = 2
warn_on_root = 1
build_dir = .buildozer

[android]
# API alvo e mínima
android.api = 33
android.minapi = 21

# Versão do NDK
android.ndk = 25b

# Arquitetura alvo
android.arch = armeabi-v7a

# Fixando versão estável de build-tools
android.build_tools = 33.0.2

# Permissões (adicione conforme necessário)
# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
