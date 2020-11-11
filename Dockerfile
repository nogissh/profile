# Building
FROM python:3.8-alpine as build-stage
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
RUN python compile.py

# Production
FROM nginx:stable-alpine as production-stage
ENV SOURCE_ROOT /usr/share/nginx/html
COPY ./configs/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./configs/robots.txt ${SOURCE_ROOT}
COPY --from=build-stage /app/public ${SOURCE_ROOT}
RUN find ${SOURCE_ROOT}/image | grep .jpg | xargs chmod 644
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
