<div align="center">

![Logo SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/SADCHAT_LOGO.png)

Chat com verificação de integridade e autenticidade através de HMAC
</div>

## Índice
 * [O que é o SadChat](https://github.com/nickolascarlos/sadchat#o-que-é-o-sadchat)
 * [Como usá-lo](https://github.com/nickolascarlos/sadchat#como-usar-o-sadchat)
  * [Verificação HMAC](https://github.com/nickolascarlos/sadchat#verifica%C3%A7%C3%A3o-de-integridade-e-autenticidade-com-hmac)
  * [Orientações para os testes da aplicação](https://github.com/nickolascarlos/sadchat#como-usar-o-sadchat)

---
### O que é o SadChat?

SadChat é um chat que visa à segurança de seus usuários (mas não sua privacidade).

Ele conecta, diretamente, dois usuários e para cada mensagem trocada faz uma verificação HMAC (do lado de quem recebe a mensagem), averiguando, assim, não só a integridade da mensagem mas também sua autenticidade, o que evita que alguma das partes seja ludibriada por um agente malicioso.

Caso a verificação HMAC revele alguma inconsistência na mensagem, é mostrado um ❌ e uma mensagem mais técnica mostrando a hash HMAC recebida (e que é a esperada) e a hash calculada pelo SadChat.

---
### Como usar o SadChat?

1. Primeiramente, execute o script:
  
  ```bash
  python3 pasta_do_sadchat
  ```

 &nbsp;
2. Essa é a tela do SadChat:

![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_01.png)

&nbsp;
3. Antes de se conectar com alguém, você deve configurar seu username e sua chave secreta.
  
  Para isso, use os seguintes comandos:

  ```bash
  !su seu_usuario
  ```

  ```bash
  !ss sua_chave_secreta
  ```
&nbsp;

4. Pronto, agora está tudo configurado para iniciar a conexão.

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_02.png)

  Se você quiser esperar por uma conexão, use o comando `!start`  
  Se quiser se conectar a alguém, use o comando `!conn IP PORTA`

  **Obviamente**, para que você se conecte com o comando `!conn` a pessoa do outro lado deve estar esperando uma conexão.
  
&nbsp;

5. Após feita a conexão, é só conversar:

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_03.png)

  * Para se desconectar, basta enviar a mensagem `bye` que a conexão será cortada.

#### Verificação de integridade e autenticidade com HMAC

  Para cada mensagem recebida, é feita uma verificação HMAC usando a chave especificada.  
  O feedback é dado pelo emoji ✅ (se a verificação de integridade e autenticidade tiver sucesso) ou ❌ (se a verificação falhar).

  Quando a verificação HMAC falhar, aparecerá uma mensagem detalhando qual a hash recebida (EXPECTED HASH) e qual a hash calculada pelo script, usando a mensagem e a chave configurada:

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_04.png)

##### Testes:

  Para testar um ataque de autenticidade, basta configurar chaves diferentes para os usuários conectados.

  Para testar o corrompimento não malicioso de mensagens, basta ligar o simulador de corrompimento em algum dos dois clientes através do comando `!simulatecorruption` (para desligá-lo, execute mesmo comando novamente).

  Quando o simulador de corrompimento estiver ligado, será alterado algum bit do primeiro byte da mensagem, que será enviada juntamente com o HMAC da mensagem íntegra.

  Exemplo do funcionamento do simulador de corrompimento:

  ###### Cliente 1:
  
  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_05.png)

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_06.png)
  
  ###### Cliente 2:

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_07.png)

