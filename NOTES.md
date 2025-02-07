# Bitnami MLFlow

Если не отключить аутентификацию (`--set tracking.auth.enabled=false`), mlflow будет просить логопас, который выковыривается так:

```bash
# Логин для mlflow tracking server
kubectl get secrets mlflow-tracking --namespace mlflow --template '{{index .data "admin-user"}}' | base64 -d

# Пароль для mlflow tracking server
 kubectl get secrets mlflow-tracking --namespace mlflow --template '{{index .data "admin-password"}}' | base64 -d
```
