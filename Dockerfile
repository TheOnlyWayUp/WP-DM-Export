FROM node:20

WORKDIR /build
COPY src/Frontend/package*.json .
RUN rm -rf node_modules
RUN rm -rf build
RUN npm install
COPY src/Frontend/. .
RUN npm run build
# Thanks https://stackoverflow.com/q/76988450

FROM python:3.10-slim

WORKDIR /app
COPY src/API/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY --from=0 /build/build /app/build
# COPY src/API/src/.env .env
COPY src/API/src .

EXPOSE 80
# ENV PORT=80

CMD [ "python3", "main.py"]

