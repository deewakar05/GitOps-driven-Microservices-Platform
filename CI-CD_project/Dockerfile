FROM node:18-alpine

WORKDIR /app

# Install only production dependencies to keep image small.
COPY package*.json ./
RUN npm install --production

# Copy application code.
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
