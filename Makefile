docker-push-flask:
	cd flask-static; make docker-push; 

swarm-up-ngrok:
	cd docker-ngrok; make swarm-up

swarm-up: docker-push-flask swarm-up-ngrok 
	cd docker-ngrok; swarm status
