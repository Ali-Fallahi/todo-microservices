# ---- Build Stage ----
# Use a Node.js image to build the project
FROM node:20-alpine as builder
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the static files for production
RUN npm run build

# ---- Production Stage ----
# Use a lightweight Nginx image to serve the static files
FROM nginx:stable-alpine

# Copy the built static files from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx listens on port 80 by default
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]