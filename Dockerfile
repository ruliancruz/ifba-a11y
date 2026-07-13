FROM mcr.microsoft.com/playwright:v1.61.1-noble AS collect

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "collect"]

FROM python:3.14-slim AS analysis

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest"]
