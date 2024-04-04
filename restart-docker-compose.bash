docker-compose down && \
docker image rm pingshian0131/pingshian-personal-website_biscuit-website
docker image rm pingshian0131/pingshian-personal-website_web
docker-compose pull && \
docker-compose up -d