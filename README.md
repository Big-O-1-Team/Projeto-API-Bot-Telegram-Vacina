# API 1° SEMESTRE ADS

<p align="center">
  <img src="docs/img/LogoGrupo.jpeg" alt="logoGrupo" width="200">
  <h2 align="center"> Equipe Big O</h2>

<p align="center">
  | <a href ="#equipe"> Equipe</a>  |
  <a href ="#tec"> Tecnologias utilizadas</a>  |   
  <a href ="#backlog"> Product Backlog</a>  |
  <a href ="#desafio"> Desafio</a>  |
  <a href ="#solução"> Solução</a>  |
  <a href ="#dor">DoR</a>  |
  <a href ="#dod">DoD</a>  |
  <a href ="#sprint"> Cronograma de Sprints</a>  |
</p>
<ul>
  <li>
    <a href='https://www.youtube.com/watch?v=Q80purAx_8c'>Video do funcionamento🎥</a>
  </li>  
</ul>



## Desafio🏅 <a id="desafio"></a>
Desenvolver um assistente virtual capaz de utilizar dados de portais públicos oficiais de saúde sobre vacinação, com o objetivo de informar o cidadão sobre:
Calendário de vacinação para diferentes faixas etárias (crianças, adolescentes/jovens, adultos e idosos).
Coberturas vacinais em diferentes regiões brasileiras.
Informações gerais sobre vacinas disponíveis.
O assistente deverá interagir com o usuário utilizando o Telegram.

## Solução🏅 <a id="solução"></a>
A solução consiste no desenvolvimento de um assistente virtual (Bot) integrado ao Telegram, capaz de coletar, processar e fornecer informações sobre vacinação no Brasil a partir de dados públicos oficiais. O sistema será desenvolvido em Python e funcionará por meio de web scraping em portais oficiais de saúde, como o site do Ministério da Saúde e plataformas de dados públicos. Os dados coletados serão organizados e armazenados em arquivos CSV permitindo consultas rápidas e organizadas.
  
  # Oswaldo Health

<p align="center">
  <img src="docs/img/FotoPerfilOswaldoHealth.png" alt="Logo Oswaldo" width="200">

<p align="center"
  >Oi eu sou o Oswaldo! Sou seu assistente pessoal de saúde, como posso te ajudar?</p>


O bot funcionará da seguinte forma:
<ul>
<li>O usuário envia uma mensagem pelo Telegram.</li>
<li>O sistema identifica a pergunta utilizando comandos.</li>
<li>O usuário informa dados como idade e localização.</li>
<li>O sistema consulta a base de dados criada a partir do web scraping.</li>
<li>O assistente retorna as informações, como:</li>
<ul>
<li>Vacinas recomendadas para a idade</li>
<li>Calendário de vacinação</li>
<li>Cobertura vacinal na região informada</li>
<li>Informações sobre campanhas e vacinas disponíveis.</li>
</ul>

## Manual de instalação
### 🛠 Pré-requisitos

<ul>
  <li>Git (<a href="https://git-scm.com/downloads">Download</a>)</li>
  <li>Python 3.9+ (<a href="https://www.python.org/downloads/">Download</a>)</li>
<ul>
  
- Telebot
- Pandas
- CSV
- IPython
- DateTime
- dotenv
- os
- bs4
- requests

---
### 1. Clonar o repositório principal
```bash
git clone https://github.com/Big-O-1-Team/Projeto-API-Bot-Telegram-Vacina
```

### 1.1 Entre na pasta
```bash
cd Projeto-API-Bot-Telegram-Vacina
```

### 2. Criação dotenv
```bash
# Para criar o arquivo vazio:
touch .env

# Para criar o arquivo já com o conteúdo:
echo "BOT_TOKEN='seu_token_aqui'" > .env
```

### 3. Instale as dependências necessárias
```bash
pip install pyTelegramBotAPI
pip install pandas
pip install python-dotenv
pip install beautifulsoup4
pip install requests
pip install ipython
```

### 4. Execute o bot
```bash
python main.py
```

## 💻 Tecnologias utilizadas <a id="tec"></a>
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jira](https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white)
![GitHub Badge](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
---

<div align="center">

# Product Backlog📋 <a id="backlog"></a>
| Rank  | Prioridade |                                                        User Story                                                            | Estimativa | Sprint
|:-----:|:----------:|:----------------------------------------------------------------------------------------------------------------------------:|:----------:|:-----------:
|**1**| **Alta**|**Como cidadão desejo um canal de comunicação de uso diário e simples para saber informações sobre meu calendário de vacinação (MVP)**|✅|**Sprint 1**
|2|Alta|Como usuário desejo saber informações das vacinas e para que elas servem                          |✅|Sprint 1
|3|Alta|Como cidadão quais vacinas estão disponíveis gratuitamente hoje nos postos de saúde               |✅|Sprint 1
|4|Alta|Como usuário desejo saber qual será a minha próxima vacina a ser tomada                           |🔄|Sprint 1
|5|Média|Como usuário desejo saber a cobertura de vacinação para o local em que eu resido                 |🔄|Sprint 2
|6|Média|Como usuário gostaria de ser alertado sobre a minha próxima vacina                               |🔄|Sprint 2
|7|Baixa|Como deficiente visual desejo ter ferramentas para o acesso as informações do assistente virtual |🔄|Sprint 3
|8|Baixa|Como estrangeiro gostaria de saber quais vacinas são necessárias pra adentrar no país            |🔄|Sprint 3
</div>

## DoR - Definition of Ready <a id="dor"></a>

* O objetivo da tarefa está definido
* A fonte de dados está definida
* A entrada e a saída da tarefa estão definidas
* Não há impedimentos para começar

## DoD - Definition of Done <a id="dod"></a>

* O código foi implementado
* O código foi testado
* Os dados foram coletados corretamente
* A funcionalidade está funcionando
* O código foi enviado para o GitHub
* A documentação foi atualizada

## Cronograma de Sprints <a id="sprint"></a>

| Sprint          |    Período    | Documentação                                     |
| --------------- | :-----------: | ------------------------------------------------ |
|  **SPRINT 1** | 11/03 - 10/04 | [Sprint 1 Docs](docs/processo/sprints/sprint-1) |
|  **SPRINT 2** | 13/04 - 03/05 | [Sprint 2 Docs](docs/processo/sprints/sprint-2) |
|  **SPRINT 3** | 11/05 - 31/05 | [Sprint 3 Docs](docs/processo/sprints/sprint-3) |


<div align = "center">

# Equipe🎓 <a id="equipe"></a>
| Função | Nome | LinkedIn | GitHub |
|:--------:|:------:|:----------:|:--------:|
| Scrum Master | Lennon Vinicius de Moraes Soares | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lennon-vinicius-de-moraes-soares-0544a0276/) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/LennonVinicius) |
| Product Owner | Enzo Ramos de Almeida | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/enzo-ramos-de-almeida-90085a364/) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/ExKN1) |
| Desenvolvedor | Erik Dias Santana | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/erik-dias-936bb0292?utm_source=share_via&utm_content=profile&utm_medium=member_ios) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/erikbtw) |
| Desenvolvedor | Felipe Dobri Camargo | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/felipe-dobri-camargo-b71a83256) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/felipedobri) |
| Desenvolvedor | Gustavo Akira Leite Minami | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gustavo-akira-leite-minami-0766571ba/) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/MinamiAkira)|
| Desenvolvedor | João Paulo Monteiro Ribas da Silva | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jo%C3%A3o-monteiro-70a698400/utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/monteirojdev-bit) |
| Desenvolvedor | Lucas Eduardo Rodrigues de Almeida | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lucas-almeida-6ba3a7254?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/Luckode554) |
| Desenvolvedor | Lucas Uchôas Morais Belarmino | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lucas-uchôas-bb2694400?utm_source=share_via&utm_content=profile&utm_medium=member_android) | [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/lucasuchoasb-hash) |

---
</div>
