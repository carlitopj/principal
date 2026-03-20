name: Gerar Executável Windows (Nuitka)

on:
  push:
    branches: [ main ]  # Roda toda vez que você envia código para a main
  workflow_dispatch:      # Permite rodar manualmente na aba "Actions"

jobs:
  build:
    runs-on: windows-latest

    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip' # Acelera as próximas compilações

      - name: Instalar Dependências
        run: |
          pip install nuitka
          if (Test-Path requirements.txt) { pip install -r requirements.txt }

      - name: Compilar com Nuitka (Windows)
        run: |
          python -m nuitka --standalone --onefile --mingw64 --plugin-enable=tk-inter --disable-console App.py
          # Nota: Remova '--disable-console' se o seu app for apenas de texto (terminal)
          # Nota: Remova '--plugin-enable=tk-inter' se não usar interface gráfica Tkinter

      - name: Disponibilizar o arquivo .exe
        uses: actions/upload-artifact@v4
        with:
          name: App-Windows-Executavel
          path: App.exe
