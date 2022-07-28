# Rede P2P

> Projeto realizado para a disciplina de Redes de Computadores, este é um projeto com objetivos de estudos, não utilize em um sistema real.
O sistema se baseia em uma rede P2P, onde cada cliente ao se conectar com um servidor, também possui caracteristicas do servidor. O objetivo desse trabalho é criar uma rede Peer to Peer, onde é possível compartilhar arquivos através de computadores diferentes na mesma rede utilizando sockets.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!---Estes são apenas requisitos de exemplo. Adicionar, duplicar ou remover conforme necessário--->
* Você possui instalado `Python 3.7`
* Você tem uma máquina `Windows / Linux / Mac`.
* Você leu `o objetivo do projeto`.

## 🚀 Instalando as Dependências

Para instalar a Rede P2P, siga estas etapas:

Abra o terminal e realize o Git Clone com o seguinte comando
```
git clone https://github.com/Grasiella/rede-p2p.git
```
Esse comando criará um diretório chamado `rede-p2p`

Ainda no terminal, acesse o diretório e execute o comando
```
pip install rich
```

## ☕ Usando a Rede P2P

Para usar o projeto, siga estas etapas:

Acesse o diretório `rede-p2p` que criamos em `Instalando as Dependências`

Para facilitar o uso do projeto, dentro desse diretório haverá uma pasta chamada `arquivos_compartilhaveis`,
dentro dela ficarão todos os arquivos que você estará disposto a compartilhar com outros Peers.

No diretório `rede-p2p` há um arquivo chamado `meus_arquivos.txt`, dentro dele terá as seguintes informações:

```
a.txt ./arquivos_compartilhaveis/a.txt
b.txt ./arquivos_compartilhaveis/a.txt
int.png ./arquivos_compartilhaveis/int.png
```

Essas informações precisarão ficar neste formato, onde cada linha possui um arquivo que você gostaria de compartilhar e o `caminho` desse arquivo. No caso desse projeto, todos estão no diretório `arquivos_compartilhaveis`


Agora, abra um terminal e execute o comando `python3 Servidor.py <PORTA>`, mandando no parâmetro porta o número da porta que você gostaria de utilizar, de preferência portas altas. **Exemplo:** `python3 Servidor.py 9450`

Desse modo, o programa iniciará e o servidor abrirá um **socket** com o endereço **IP:porta**, sendo o endereço IP da máquina que executou o `Servidor.py`

Ao iniciar o **Servidor**, ele estará disposto a receber um **Peer**, para adicionar um **Peer** à rede, execute em outro terminal da mesma máquina, ou no terminal de outro computador na mesma rede o seguinte comando `python3 Peers.py <IP>`, sendo IP o endereço da máquina que está executando o **Servidor**, pois é nele que queremos conectar. **Obs:** este outro computador precisa fazer o git clone também!

Dentro do Peer, há uma série de comandos disponíveis, sendo eles:

`peers` o servidor retorna uma tabela com todos os Peers conectados na rede, com o seguinte formato:

| Endereço IP         |     Porta     |
| ------------------- |  ------------ |
|  127.0.0.1          |     5455      |
|  127.0.0.2          |     5456      |
|    ...              |      X        |
|   Última Peer       |  Última porta |



`ls <IP> <PORTA>` sendo IP e Porta, o endereço do vizinho que você gostaria de fazer buscar arquivos, informações podem ser enconstradas na tabela do comando `peers`, retorna uma tabela no seguinte formato:

| Arquivos compartilhados |
| -------------------     |
|  a.txt                  | 
|  ab.txt                 | 
|    ...                  | 
|   Último arquivo        | 


`get <IP> <NOME_ARQUIVO.EXTENSAO>` sendo IP E nome do arquivo, dados que podem ser encontrados nas tabelas dos comandos `peers` e `ls`, o comando `get` irá baixar o arquivo informado do **Peer** cujo IP foi passado como parâmetro.

`quit` encerra a conexão.

Todos estes comandos podem ser executados através de todas as máquinas cujos terminais estão rodando `Peers.py` conectados ao mesmo **Servidor**.



## 📖 Como o Algoritmo Funciona

Ao iniciar o **Servidor**, ele criará um socket com uma conexão TCP e manterá uma porta aberta pública para conexões de terceiros enquanto o programa estiver rodando. Após esse momento ele estará em loop na função `start()`esperando algum **Peer** se conectar a ele.

Quando um **Peer** se conecta ao **Servidor**, o Servidor inicia uma thread para a conexão estabelecida, e se mantém em loop na função `start()`esperando algum outro Peer se conectar a ele. Então o novo Peer é adicionado à lista de Peers conectados e a conexão segue aberta, com a thread realizando a função de "ouvir" os comandos emitidos por este peer (peers ou quit).

A cada Peer conectado, uma thread é iniciada para ficar em função dele.

Executando o Peer pela primeira vez, ele estabelecerá uma conexão via socket com o servidor enviado como parâmetro, essa conexão será realizada no endereço criado pelo socket do Servidor que está aguardando conexões. Após estabelecer a conexão, o estado do programa Peer estará dentro da função `menu()`, ele receberá uma porta pública informada pelo Servidor e criará uma thread para ouvir caso alguém queira se conectar a ele, visto que o sistema é P2P.

A thread criada será enviada para a função `listening()`, onde o peer criará um socket para conexões de terceiros (utilizando seu IP e a porta pública informada pelo servidor) e ficará aguardando até que algum outro peer queira se conectar a ele.

Ao aceitar uma conexão, é inicializada outra thread que irá para a função `peer_connected()`, cuja função é ficar a mercê dessa conexão e poder receber os comandos dos Peers terceiros conectados a ele.

Quando o Peer principal quiser se conectar a outro Peer da rede para receber ou ver arquivos, haverá a função `connect_to_peer()` que realizará esta funcionalidade.

<h3>Tenha um bom uso!<h3>
