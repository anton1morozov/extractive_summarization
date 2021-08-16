
build:
	docker build -t summarizer_service .

run:
	docker run -it --name summarizer_container -p 5000:5000 summarizer_service

request:
	curl -iX POST -H "Content-Type: application/json" -d @example.json "localhost:5000/process"

clear:
	docker container stop summarizer_container
	docker container rm summarizer_container
	docker rmi summarizer_service
