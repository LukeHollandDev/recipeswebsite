# Use the official Node.js runtime as the base image
FROM node:18 as build

# Set environment variables
ARG VITE_API_URL
ENV VITE_API_URL ${VITE_API_URL}
ARG VIRTUAL_HOST
ENV VIRTUAL_HOST ${VIRTUAL_HOST}
ARG LETSENCRYPT_HOST
ENV LETSENCRYPT_HOST ${LETSENCRYPT_HOST}

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire application code to the container
COPY . .

# Build the React app for production
RUN npm run build

# Use Nginx as the production server
FROM nginx:alpine

# Copy the built React app to Nginx's web server directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the Nginx server
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]