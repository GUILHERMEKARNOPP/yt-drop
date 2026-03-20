# YT Drop 
> Frontend no Vercel + Backend no Render — 100% gratuito para sempre

---

## Arquivos do projeto

```
yt-drop/
├── index.html       ← Frontend (deploy no Vercel)
├── server.py        ← Backend Python Flask
├── requirements.txt ← Dependências Python
├── render.yaml      ← Config automática do Render
└── README.md
```

---

## PASSO 1 — Instalar o Git (se não tiver)

Baixe em: https://git-scm.com/download/win  
Instale com as opções padrão.

---

## PASSO 2 — Criar o repositório no GitHub

1. Acesse https://github.com/new
2. Repository name: `yt-drop`
3. Deixe como **Public**
4. **NÃO** marque "Add a README file"
5. Clique em **Create repository**

---

## PASSO 3 — Subir os arquivos para o GitHub

Abra o terminal (PowerShell ou CMD) na pasta onde estão os arquivos e rode:

```bash
git init
git add .
git commit -m "feat: yt-drop inicial"
git branch -M main
git remote add origin https://github.com/GUILHERMEKARNOPP/yt-drop.git
git push -u origin main
```

> Se pedir login, entre com seu usuário e senha/token do GitHub.

---

## PASSO 4 — Deploy do backend no Render (grátis)

1. Acesse https://render.com
2. Clique em **Get Started for Free**
3. Faça login com **GitHub**
4. Clique em **New +** → **Web Service**
5. Conecte o repositório `yt-drop`
6. Preencha:
   - **Name:** `yt-drop`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn server:app --bind 0.0.0.0:$PORT --workers 2 --timeout 300`
7. Plano: **Free**
8. Clique em **Create Web Service**
9. Aguarde o build (3-5 minutos)
10. Copie a URL gerada (ex: `https://yt-drop.onrender.com`)

> ⚠ O Render instala ffmpeg automaticamente no ambiente Python gratuito.

---

## PASSO 5 — Conectar o frontend ao backend

1. Abra o arquivo `index.html`
2. Localize a linha:
   ```js
   const API = 'https://yt-drop.onrender.com';
   ```
3. Substitua pela URL real que o Render gerou
4. Salve o arquivo

Depois faça push:
```bash
git add index.html
git commit -m "fix: url do backend"
git push
```

---

## PASSO 6 — Deploy do frontend no Vercel (grátis)

1. Acesse https://vercel.com
2. Clique em **Sign Up** → **Continue with GitHub**
3. Clique em **Add New...** → **Project**
4. Importe o repositório `yt-drop`
5. Clique em **Deploy** (sem alterar nada)
6. Aguarde ~1 minuto

Sua URL será algo como: `yt-drop.vercel.app`

Para personalizar o nome:
- Settings → Domains → adicione um nome como `ytdrop.vercel.app`

---

## PRONTO! 

- **Frontend:** `https://yt-drop.vercel.app` (qualquer pessoa do mundo acessa)
- **Backend:** `https://yt-drop.onrender.com` (processa os downloads)

### Observações importantes

- O Render no plano gratuito **dorme após 15min sem uso** e leva ~30 segundos para acordar. O site mostra um aviso automático quando isso acontece.
- O Vercel atualiza automaticamente sempre que você fizer `git push`.
- Limite gratuito do Render: **750 horas/mês** (suficiente para uso pessoal o mês todo).

### Para atualizar o site no futuro

Edite os arquivos e rode:
```bash
git add .
git commit -m "sua mensagem"
git push
```
Vercel e Render atualizam automaticamente.
