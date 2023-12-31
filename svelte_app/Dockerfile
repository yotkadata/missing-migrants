# Step 1: Build the Svelte app with Vite

# Use the official Node.js image as the builder
FROM node:16 AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and vite.config.js
COPY package.json vite.config.js ./

# Install dependencies
RUN npm install

# Copy the rest of the app files
COPY src src/
COPY public/favicon.ico public/
COPY public/*.png public/
COPY index.html ./
COPY jsconfig.json ./

# Run Vite build
RUN npm run build

# Step 2: Serve the app using Nginx

# Use the official Nginx image
FROM nginx:alpine

# Set permissions for Nginx
RUN chown -R nginx:nginx /usr/share/nginx/html/

# Copy the built app from the builder stage and Nginx configuration (if any)
COPY --from=builder /app/dist /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Nginx will start automatically and serve the app at port 80
