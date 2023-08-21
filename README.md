# AnyLattes
<h3>Projeto de TCC com finalidade de auxiliar a avaliação contínua de currículo Lattes dos professores do PPGCC da UFPA.</h3>

<h2 align="center">Ferramentas</h2>

<div align="center" class="col-md-6"> 
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="30" width="40"/></td>
    <td>Python </td>
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" height="30" width="40"/></td>
    <td>Flask </td>
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" height="30" width="40"/></td>
    <td>Bootstrap 5.1 </td>
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" height="30" width="40"/></td>
    <td>SQLite </td>
    <td><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" height="30" width="40"/></td>
    <td>Docker (Opcional)</td>
</div>

<hr/>
<h2 align="center"> Instalação Windows </h2>
<ol>
<li>Instale o Python, disponibilizado em:
<pre><a href="https://www.python.org/downloads/">https://www.python.org/downloads</a></pre></li>
<li>Após baixar o projeto, executar o arquivo <strong>dependencias_windows.bat</strong> para preparar o ambiente e instalar as dependências utilizadas pela aplicação. </li>
<li>Para rodar a aplicação, execute o arquivo <strong>start.bat*</strong>
</ol>

<hr/>
<h2 align="center"> Instalação Linux (Debian / Ubuntu)</h2>
<ol>
<li> Baixe o projeto. Dentro do diretório, abra o terminal e execute o seguinte comando:
<pre>./dependencias_linux.sh</pre>
Ele irá instalar todas as dependências necessárias para a aplicação, desde a atualização da distro, instalação do Python, até as bibliotecas. O script utiliza do <strong>sudo</strong> para executar os comandos com as permissões, então, exgirá a senha com permissão root (admin) para prosseguir.</li>

<li>Para rodar a aplicação, execute o comando:
<pre>python app.py</pre>

</li>

</ol>

<hr/>
<h2 align="center"> Instalação Container Docker </h2>
<hr />
<h3 align="center">Docker Compose </h3>
<hr/>
<ol>
<li>Baixe o projeto. A Aplicação fará todo o deploy em container docker. Então execute, dentro do projeto o comando via docker-compose</li>
<pre>docker-compose up -d --build anylattes</pre>

Isso irá carregar a aplicação no IP: 172.21.0.3. Após finalizar, o container ficará rodando em 2° plano. Acesse a aplicação no navegador via URL:
<pre>http://172.21.0.3:5000</pre>

<hr />
<h3 align="center">Docker Run </h3>
<hr/>

<li>Ou se não utilizar o docker-compose, dentro do projeto, execute o comando abaixo para criar o network do container: </li>
<pre>docker network create -d bridge --subnet=172.21.0.0/24 --gateway=172.21.0.1 anylattes-network </pre>

E o build da aplicação:
<pre> docker build -t anylattes . </pre>

E depois o comando para rodar a aplicação:
<pre>docker run -d --name anylattes --network=anylattes-network --ip 172.21.0.3 anylattes</pre>

Após finalizar, o container ficará rodando em 2° plano. Acesse a aplicação no navegador via URL:
<pre>http://172.21.0.3:5000</pre>
</ol>

