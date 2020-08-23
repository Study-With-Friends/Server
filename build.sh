aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 272604832244.dkr.ecr.us-east-1.amazonaws.com
docker build -t study-with-friends .
docker tag study-with-friends:latest 272604832244.dkr.ecr.us-east-1.amazonaws.com/study-with-friends:latest
docker push 272604832244.dkr.ecr.us-east-1.amazonaws.com/study-with-friends:latest

