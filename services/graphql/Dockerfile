FROM node:20-alpine

# VULN: Running as root (no USER directive)
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --omit=dev

# Copy source
COPY . .

# VULN: Secrets hardcoded in image via build args / ENV
ENV NODE_ENV=development
ENV JWT_SECRET=secret123
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=vulnshop
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres123
ENV REDIS_URL=redis://redis:6379

# VULN: Expose unnecessary port metadata
EXPOSE 4000
EXPOSE 9229

# VULN: Debug mode enabled (exposes inspector)
# CMD ["node", "--inspect=0.0.0.0:9229", "src/index.js"]
CMD ["node", "src/index.js"]
