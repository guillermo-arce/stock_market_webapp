
Welcome to the README, please find below some indications.

Directory structure explained:

- stock_api: Contains the Python implementation of StockAPI, as well as the required Dockerfile.

- webapp: Contains the Python implementation of WebApp, as well as the required Dockerfile.

- docker-compose.yml: It is the YAML file to configure our web application deployment.

You can access prediction models repository right here: https://github.com/guillermoarce07/stock_market_models

HOW-TO:

In order to access the web application, you can do the following:

- Deploy the web application locally. For that purpose, it is just needed to execute the following command from the current directory (as well as having "docker" and "docker-compose" installed):

	$ docker-compose up -d --build

	Please, feel free to remove/edit the extra flags:
	
	"-d" is for detached mode-
	"--build" is for forcing image building before starting containers.


	After that, accessing http://localhost:7000 should show the web application.



