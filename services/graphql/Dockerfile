FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --omit=dev

# Copy source
COPY . .

ENV NODE_ENV=development
ENV JWT_SECRET=secret123
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=vulnshop
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres123
ENV REDIS_URL=redis://redis:6379

EXPOSE 4000
EXPOSE 9229

CMD ["node", "src/index.js"]
