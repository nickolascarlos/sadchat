<div align="center">

![Logo SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/SADCHAT_LOGO.png)

Chat com verificação de integridade e autenticidade através de HMAC
</div>

---
### Como usar o SadChat?

* Primeiramente, execute o script:
  
  ```bash
  python3 pasta_do_sadchat
  ```

 &nbsp;
* Essa é a tela do SadChat:

![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_01.png)

&nbsp;
* Antes de se conectar com alguém, você deve configurar seu username e sua chave secreta.
  
  Para isso, use os seguintes comandos:

  ```bash
  !su seu_usuario
  ```

  ```bash
  !ss sua_chave_secreta
  ```
&nbsp;

* Pronto, agora está tudo configurado para iniciar a conexão.

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_02.png)

  Se você quiser esperar por uma conexão, use o comando `!start`  
  Se quiser se conectar a alguém, use o comando `!conn IP PORTA`

  **Obviamente**, para que você se conecte com o comando `!conn` a pessoa do outro lado deve estar esperando uma conexão.
  
&nbsp;

* Após feita a conexão, é só conversar:

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_03.png)

  Para cada mensagem recebida, é feita uma verificação HMAC usando a chave especificada.  
  O feedback é dado pelo emoji ✅ (se a mensagem tiver sido autenticada com sucesso) ou ❌ (se a autenticação falhar).

  Quando a autenticação HMAC falhar, aparecerá uma mensagem detalhando qual a hash recebida (EXPECTED HASH) e qual a hash calculada pelo script, usando a mensagem e a chave configurada:

  ![Tela SadChat](https://raw.githubusercontent.com/nickolascarlos/sadchat/main/images/tela_04.png)

&nbsp;

* Para se desconectar, basta enviar a mensagem `bye` que a conexão será cortada.