# escalonador-multi-level-queue
Simulação de escalonador de múltiplas filas.<br>

<h1>O que é um escalonador?</h1>
Escalonador é o programa de um sistema operacional multiprogramável responsável pela alocação e retirada de processos na CPU seguindo uma estratégia específica.
É importante que um escalonador aloque os processos na CPU de forma justa, sem causar starvation (situação em que um processo nunca é alocado). 

<h1>Multi-level-queue (MLQ)</h1>
É uma estratégia de escalonamento na qual os processos prontos são colocados em diferentes filas baseadas em seu tipo.  Cada fila de processos prontos tem uma prioridade, sendo a fila de processos de sistema com a maior prioridade, processos interativos de média prioridade e processos batch de menor prioridade.

![image](https://github.com/user-attachments/assets/825611bd-4cf9-4c51-b837-41e161b31485)
 
<h1>Simulação</h1>
Este projeto simula um escalonador de múltiplas filas, é possível utilizar a interface gráfica para escolher parâmetros de execução.

![image](https://github.com/user-attachments/assets/094d1110-543b-40bf-b004-a0fea03b623c)

<ul>
  <li>
    <strong>Processos de sistema, processos interativos e processos batch:</strong> Número de processos de cada tipo.
  </li>
  <li>
    <strong>Processos permanentes:</strong> Número de processos que nunca acabam.
    <ul>
      <li>
        Os processos permanentes são escolhidos de maneira aleatória.
      </li>
      <li>
        Neste caso, a execução se torna inifinita, para finalizar, basta clicar o botão de parar.
      </li>
    </ul>
  </li>
  <li>
    <strong>Clock:</strong> Tempo de espera entre uma execução e outra.
  </li>
  <li>
    <strong>Cores:</strong> Número de cores (núcleos) que serão utilizados na simulação.
  </li>
</ul>

<h1>Execução</h1>
Para executar, é só buscar o arquivo <strong>main.exe</strong>, dentro da pasta <strong>/src/dist/main</strong>.

<h1>Participantes</h1>
Antônio José Brogni (https://github.com/abrogni), Lucas Bauchspiess (https://github.com/lbauch) e Mateus Albano Santos (https://github.com/mateusalbano).

