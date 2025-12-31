FROM node:20-alpine

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend .

ENV NEXT_PUBLIC_API_BASE_URL=http://backend:8000
ENV NODE_ENV=production

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
