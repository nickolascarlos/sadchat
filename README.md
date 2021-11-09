<div align="center">

![Logo SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/SADCHAT_LOGO.png)

Chat com verificação de integridade e autenticidade através de HMAC
</div>

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

