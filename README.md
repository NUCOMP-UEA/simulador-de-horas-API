<h1 align="center"> Descrição do Projeto </h1>

<p align="center">Simulador de horas complementares para o site do curso de Engenharia de Computação, Sistemas de Informação e Licenciatura em Computação.</p>

<h2 align="center"> Tecnologias Utilizadas </h2>

<p align="center">
	<a href="https://fastapi.tiangolo.com"><img alt="Static Badge" src="https://img.shields.io/badge/fastapi-white?style=for-the-badge&logo=FastAPI"></a>
	<a href="https://www.mongodb.com/pt-br"><img alt="Static Badge" src="https://img.shields.io/badge/mongodb-white?style=for-the-badge&logo=MongoDB"></a>
	<a href="https://www.docker.com"><img alt="Static Badge" src="https://img.shields.io/badge/Docker-white?style=for-the-badge&logo=docker&logoColor=%232496ED"></a>
	<a href="https://python-poetry.org"><img alt="Static Badge" src="https://img.shields.io/badge/poetry-white?style=for-the-badge&logo=Poetry"></a>
</p>

### Instalação do pré-requisito

Será necessário instalar o Docker:

```zsh
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
```

### Execução do comando no terminal

```zsh
docker build -t sound-sensor-api .
```