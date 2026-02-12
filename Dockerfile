FROM pytorch/torchserve:latest-cpu

# Switch to root to make changes
USER root

# Create config directory and file
RUN mkdir -p /home/model-server && \
    echo "disable_token_authorization=true" > /home/model-server/config.properties && \
    chown -R model-server:model-server /home/model-server

# Copy model archive
COPY model-store /home/model-server/model-store

# Switch back to non-root user (FIX: Don't run as root!)
USER model-server

# Expose ports
EXPOSE 8080 8081 8082

# Start TorchServe
CMD ["torchserve", \
     "--start", \
     "--ncs", \
     "--model-store", "/home/model-server/model-store", \
     "--models", "mnist=mnist-digit-classifier.mar", \
     "--disable-token-auth"]