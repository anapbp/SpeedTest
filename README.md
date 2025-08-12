# Speedtest – Primeiro trabalho de Redes

Este script realiza testes de velocidade em redes utilizando os protocolos TCP e UDP, simulando o envio e recebimento de pacotes durante um período fixo de tempo. 
Ele foi desenvolvido na disciplina de Redes, com o objetivo de medir desempenho em termos de taxa de transferência e quantidade de pacotes transmitidos/recebidos.

A execução é feita no modo remetente (sender) ou receptor (receiver). O remetente conecta-se ao receptor utilizando o protocolo especificado e envia pacotes contendo uma mensagem de teste, completada até 500 bytes. 
O envio ocorre continuamente por 20 segundos, registrando a quantidade de pacotes e bytes enviados. 
O receptor, por sua vez, fica aguardando conexões ou pacotes, também por 20 segundos, contabilizando a quantidade de dados recebidos.

Durante a execução, o tempo decorrido é exibido em segundos, permitindo acompanhar o progresso do teste. Ao final, são calculadas e exibidas as seguintes métricas:

* Total de pacotes enviados/recebidos;
* Total de bytes enviados/recebidos;
* Velocidade média em bits por segundo;
* Velocidade média em pacotes por segundo.

O código utiliza **sockets** para implementar a comunicação. Além disso, a biblioteca **argparse** é usada para configurar parâmetros via linha de comando, permitindo especificar o protocolo, o papel (remetente ou receptor), o endereço IP do destino (no caso do remetente) e a porta utilizada.

## Como usar:

(Receptor TCP na porta 5000)

```
python speedtest.py --protocol tcp --role receiver --port 5000
```

(Remetente TCP enviando para 192.168.0.10 na porta 5000)

```
python speedtest.py --protocol tcp --role sender --host 192.168.0.10 --port 5000
```

(Receptor UDP na porta 5000)

```
python speedtest.py --protocol udp --role receiver --port 5000
```

(Remetente UDP enviando para 192.168.0.10 na porta 5000)

```
python speedtest.py --protocol udp --role sender --host 192.168.0.10 --port 5000
```
