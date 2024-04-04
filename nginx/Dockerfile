FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

#RUN mkdir -p /etc/nginx/ssl/
#COPY *.pem /etc/nginx/ssl/

#certonly --agree-tos --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory -d "tarot-fastapi.simplesocool.cc"
