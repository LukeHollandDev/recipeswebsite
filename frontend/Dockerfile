# Use the official Node.js runtime as the base image
FROM node:20 as build

# Set environment variables
ARG VITE_API_URL
ENV VITE_API_URL ${VITE_API_URL}

# Set the working directory in the container
WORKDIR /app

# Copy the entire application code to the container
COPY . .

# Install dependencies
RUN npm install

# Build the React app for production
RUN npm run build

# Use Nginx as the production server
FROM nginx:alpine

# Set environment variables
ARG VIRTUAL_HOST
ENV VIRTUAL_HOST ${VIRTUAL_HOST}
ARG LETSENCRYPT_HOST
ENV LETSENCRYPT_HOST ${LETSENCRYPT_HOST}

# Copy the built React app to Nginx's web server directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for the Nginx server
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]