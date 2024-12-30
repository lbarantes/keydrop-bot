# Automação Web para Participação em Sorteios  

Este projeto realiza a automação de interações com o site **KeyDrop**, permitindo que o usuário participe de sorteios com base em critérios definidos, como tipo de sorteio e valor mínimo. O sistema também implementa controle de acesso por chave e notifica o usuário sobre a conclusão ou a necessidade de ações adicionais, como resolver captchas.  

## ⚒️ Funcionalidades  

1. **Controle de Acesso**  
   - Ao iniciar o programa, é exibida uma tela solicitando uma **chave de acesso**.  
   - Se a chave for válida e vinculada ao endereço MAC do dispositivo, o usuário avança para a próxima etapa.  
   - Chaves inválidas retornam uma mensagem de erro, impedindo o acesso.  

2. **Definição de Preferências**  
   - Após validar a chave, o usuário acessa uma segunda tela onde pode configurar:  
     - **Tipo de Sorteio**  
     - **Valor Mínimo do Sorteio**  

3. **Automação do Sorteio**  
   - O programa acessa o site **KeyDrop** e navega até a página de sorteios.  
   - Localiza o sorteio com base nos critérios definidos (tipo e valor mínimo).  
   - Verifica se o valor do sorteio atende aos requisitos configurados.  
   - Caso positivo:  
     - Clica no botão do sorteio e tenta entrar.  
     - Se um captcha (anti-bot) for solicitado:  
       - Envia uma notificação no Windows para que o usuário resolva o captcha manualmente.  
     - Caso contrário, conclui a participação no sorteio automaticamente e notifica o usuário.  

## 💻 Tecnologias Utilizadas  

- **Selenium**: Automação de navegação na web.  
- **Tkinter**: Interface gráfica para interação com o usuário.  
- **Notificações do Windows (win10toast)**: Informar o usuário sobre captchas ou conclusão de ações.  
- **Validação por Endereço MAC (getmac)**: Garantia de uso único da chave por dispositivo.  

## 📋 Requisitos  

1. **Google Chrome instalado**  
   - O bot utiliza o navegador Google Chrome para executar a automação.  

2. **Login prévio no KeyDrop**  
   - O usuário deve ter realizado login manualmente no site KeyDrop pelo menos uma vez no computador.  
   - Isso permite que o bot acesse o diretório de **User Data** e se autentique automaticamente como o usuário.
   - Observação: Não se pode realizar login pelo navegador do BOT, ele deve ser feito pelo navegador original.
    
