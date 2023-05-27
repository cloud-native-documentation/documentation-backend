FROM python:3.11-alpine
WORKDIR /app

RUN addgroup -S backend && adduser -S backend -G backend

COPY requirements.txt .

USER backend
RUN pip install --no-cache-dir --user -r requirements.txt

USER root
COPY . .

RUN chown -R backend:backend /app/DocManageSystem/store

USER backend

VOLUME /app/DocManageSystem/store

EXPOSE 8000

# Start the application
CMD ["/app/deploy.sh"]