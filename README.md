# Eco-Libras – Site do Curso de Libras Audiovisual

Aplicação web em Flask para um glossário de termos com foco em acessibilidade. Este README explica como rodar localmente (Windows), como usar Docker e como publicar o site para acesso público.

## 🚀 Início Rápido

### Opção 1: Docker (Recomendado para colaboração)

```powershell
# Clonar o repositório
git clone https://github.com/sergioxv2006/eco-libras.git
cd eco-libras

# Iniciar com Docker Compose
docker-compose up --build
```

Acesse: `http://localhost:5000`

📖 **[Ver documentação completa do Docker](DOCKER.md)**

### Opção 2: Instalação Local (Windows / PowerShell)

Pré-requisitos:

- Python 3.11+ instalado (recomendado)
- Git (opcional)

1. Clonar o repositório e entrar na pasta do projeto

```powershell
git clone https://github.com/sergioxv2006/eco-libras.git
cd eco-libras
```

2. Criar e ativar um ambiente virtual

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependências

```powershell
python -m pip install -U pip
pip install -r requirements.txt
```

4. Configurar variáveis de ambiente

```powershell
Copy-Item .env.example .env
# Edite o arquivo .env se quiser trocar SECRET_KEY, ADMIN_USER/PASSWORD ou o caminho do banco
```

Por padrão, o projeto usa SQLite em `instance/data_bank.db`. A pasta `instance/` já existe no repo.

5. Iniciar a aplicação

```powershell
python -m APP.run
```

Abra http://localhost:5000 no navegador. Área admin em http://localhost:5000/admin (credenciais no `.env`). Na primeira execução, as tabelas são criadas automaticamente.

## Características do Projeto

### Design

- **Paleta de cores**: Azul (#007bff) e branco (#ffffff)
- **Estilo**: Minimalista e limpo
- **Responsivo**: Adaptável a diferentes dispositivos
- **Tipografia**: Arial, fonte legível e escalável

### Acessibilidade

- **WCAG 2.1 Nível AA**: Conformidade com diretrizes internacionais
- **Navegação por teclado**: Totalmente navegável via teclado
- **Leitores de tela**: Compatível com NVDA, JAWS e VoiceOver
- **Alto contraste**: Modo de alto contraste disponível
- **Ajuste de fonte**: Aumento/diminuição do tamanho da fonte
- **Semântica HTML5**: Estrutura semântica adequada
- **Atributos ARIA**: Labels e roles apropriados

### Funcionalidades

- **Navegação suave**: Scroll suave entre seções
- **Formulário de contato**: Com validação acessível
- **Barra de ferramentas de acessibilidade**: Controles rápidos
- **Animações responsivas**: Respeitam preferências do usuário
- **Anúncios para leitores de tela**: Feedback auditivo

## Estrutura de Arquivos

```
libras_course_website/
├── index.html              # Página principal
├── accessibility.html      # Página de recursos de acessibilidade
├── css/
│   ├── style.css           # Estilos principais
│   └── accessibility.css   # Estilos específicos de acessibilidade
├── js/
│   ├── script.js           # JavaScript principal
│   └── accessibility.js    # JavaScript de acessibilidade
└── images/
    ├── accessibility_icon1.jpg
    ├── accessibility_icon2.jpg
    ├── accessibility_icon3.jpg
    ├── sign_language_icon1.jpg
    └── sign_language_icon2.jpg
```

## Recursos de Acessibilidade Implementados

### 1. Navegação por Teclado

- **Tab**: Navegar para o próximo elemento
- **Shift + Tab**: Navegar para o elemento anterior
- **Enter/Space**: Ativar links e botões
- **Esc**: Voltar ao topo da página
- **Alt + 1**: Ir para o conteúdo principal
- **Alt + 2**: Ir para o menu de navegação
- **Alt + 3**: Ir para o formulário de contato
- **Alt + 4**: Ir para o rodapé

### 2. Ferramentas de Acessibilidade

- **A+**: Aumentar tamanho da fonte
- **A-**: Diminuir tamanho da fonte
- **A**: Resetar tamanho da fonte
- **Contraste**: Alternar modo de alto contraste
- **🔊**: Ativar/desativar modo leitor de tela

### 3. Compatibilidade com Leitores de Tela

- Estrutura semântica HTML5
- Atributos ARIA apropriados
- Descrições alternativas para imagens
- Anúncios de mudanças de contexto
- Labels associados aos campos de formulário

### 4. Design Responsivo

- Layout flexível
- Suporte a zoom até 200%
- Compatível com dispositivos móveis
- Orientação portrait e landscape

## Conformidade com Padrões

### WCAG 2.1 Nível AA

- **Perceptível**: Contraste adequado, texto alternativo
- **Operável**: Navegação por teclado, sem convulsões
- **Compreensível**: Linguagem clara, comportamento previsível
- **Robusto**: Compatível com tecnologias assistivas

### Lei Brasileira de Inclusão

- Conformidade com a Lei nº 13.146/2015
- Acessibilidade digital garantida

### eMAG

- Seguimento do Modelo de Acessibilidade em Governo Eletrônico

## Como Usar

1. Abra o arquivo `index.html` em um navegador web
2. Use a barra de ferramentas de acessibilidade no topo direito para ajustar preferências
3. Navegue pelo site usando o teclado ou mouse
4. Acesse a página de acessibilidade para mais informações sobre recursos disponíveis

## Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **CSS3**: Estilos e responsividade
- **JavaScript**: Interatividade e acessibilidade
- **Imagens**: Ícones relacionados a Libras e acessibilidade

## Suporte

Para questões de acessibilidade ou suporte técnico:

- Email: acessibilidade@cursodlibras.com.br
- Telefone: (91) 98977-4760
- WhatsApp: Disponível através do link no site

## Licença

© 2026 Curso de Libras. Todos os direitos reservados.
Comprometidos com a acessibilidade e inclusão digital.
