FROM node:20-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with architecture detection
RUN npm install && \
    if [ "$(uname -m)" = "aarch64" ]; then \
    npm install @rollup/rollup-linux-arm64-musl; \
    else \
    npm install @rollup/rollup-linux-x64-musl; \
    fi

# Copy source files
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]