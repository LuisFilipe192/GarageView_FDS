# Como Contribuir para o GarageView 🚗
para uma melhor organização e garantir a qualidade do software, siga as diretrizes abaixo.

---

## 1. Configurando o Ambiente Local

Para rodar e testar o projeto na sua máquina, siga estes passos:

### Pré-requisitos
- Ter o Python 3.10+ instalado.
- Ter o Git configurado.

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/LuisFilipe192/GarageView_FDS.git


2.  Crie e ative um ambiente virtual (venv):

No Windows:
Bash
python -m venv venv
.\venv\Scripts\activate

No Linux/Mac:
Bash
python3 -m venv venv
source venv/bin/activate

3.  instalar dependênciass:
Bash
pip install -r requirements.txt

4. Rode as migrações do banco de dados (SQLite):
bash
python manage.py migrate

5. Inicie o servidor local:
Bash
python manage.py runserver


--- Fluxo de Desenvolvimento (Git) ---

1. Sempre puxe as atualizações da Main antes de começar:

Bash
git checkout main
git pull origin main

2. Crie uma branch separada para a sua tarefa:

Use nomes claros: feature/nome-da-historia 

Bash
git checkout -b feature/nova-funcionalidade

3. Faça Commits Atômicos:

Faça commits pequenos e focados. Cada commit deve resolver apenas uma coisa.

Exemplo: git commit -m "Cria a lógica de login na view"

4. Suba sua branch e abra um Pull Request (PR):

Bash
git push origin feature/nova-funcionalidade

--- Regras Importantes do Projeto (Diretrizes de FDS) ---

Sem Generic Views ou Django Forms: Todo o processamento de requisições (POST/GET) e formulários deve ser feito de forma manual nas views.py para fins de aprendizado da disciplina.

Coesão e Acoplamento: Mantenha as classes e funções focadas. Se uma View está fazendo coisas demais, quebre a lógica.

Testes: Se você criar uma nova funcionalidade, lembre-se de atualizar ou criar os testes automatizados correspondentes para garantir que o fluxo ponta a ponta (E2E) continue funcionando.