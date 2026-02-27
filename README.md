# escalonador-multi-level-queue
Simulação de escalonador de múltiplas filas.<br>

<h1>O que é um escalonador?</h1>
Escalonador é o programa de um sistema operacional multiprogramável responsável pela alocação e retirada de processos na CPU seguindo uma estratégia específica.
É importante que um escalonador aloque os processos na CPU de forma justa, sem causar starvation (situação em que um processo nunca é alocado). 

<h1>Multi-level-queue (MLQ)</h1>
É uma estratégia de escalonamento na qual os processos prontos são colocados em diferentes filas baseadas em seu tipo.  Cada fila de processos prontos tem uma prioridade, sendo a fila de processos de sistema com a maior prioridade, processos interativos de média prioridade e processos batch de menor prioridade.<br>

<img width="886" height="812" alt="image" src="https://github.com/user-attachments/assets/d00921b9-6e0c-4a1c-b187-d81e9de95e93" />
 
<h1>Simulação</h1>
Este projeto simula um escalonador de múltiplas filas, é possível utilizar a interface gráfica para escolher parâmetros de execução.<br>

<img width="993" height="772" alt="image" src="https://github.com/user-attachments/assets/fa3ac104-738a-4ed5-864d-bb5b048b4046" />

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
    <strong>cpus:</strong> Número de cpus que serão utilizados na simulação.
  </li>
</ul>

<h1>Execução</h1>
Para executar, basta fazer o download do projeto e escolher um ambiente Python.

<h1>Participantes</h1>
Antônio José Brogni https://github.com/abrogni, Lucas Bauchspiess https://github.com/lbauch e Mateus Albano Santos https://github.com/mateusalbano.
