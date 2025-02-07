# otus_mlops_k8s_dags2

## Установка Ingress

Ставим [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)-контроллер:

```bash
# Активируем манифест из интернетов;
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Опционально: ждем, пока придет в себя;
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

## Установка Mlflow

Ставим чарт [bitnami/mlflow](https://artifacthub.io/packages/helm/bitnami/mlflow) и включаем [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/#the-ingress-resource)-ресурсы для самого mlflow и для его зависимого чарта (сабчарта) [bitnami/minio](https://artifacthub.io/packages/helm/bitnami/minio).

```bash
helm upgrade --install mlflow bitnami/mlflow --create-namespace --namespace=mlflow --set tracking.auth.enabled=false --set tracking.service.type=ClusterIP --set tracking.ingress.enabled=true --set minio.ingress.enabled=true
```

Добавляем в `/etc/hosts` строчки:

```bash
127.0.0.1       minio.local
127.0.0.1       mlflow.local
```

Шагайте браузером на http://mlflow.local. 

## Загрузка референсного датасета в Minio

Идите на http://minio.local. Креденциалы берите тут:

```bash
# Логин для minio
kubectl get secrets mlflow-minio --namespace mlflow --template '{{index .data "root-user"}}' | base64 -d

# Пароль для minio
kubectl get secrets mlflow-minio --namespace mlflow --template '{{index .data "root-password"}}' | base64 -d
```

Создайте новый бакет с именем `datasets` и загрузите внутрь файл [drifter/data/reference.csv](drifter/data/reference.csv) – это будет референсный датасет, с которым нужно сравнивать вновь прибывшие данные.

Кроме того, создайте идентификатор секретного ключа и сам секретный ключ для доступа в хранилище. Графический интерфейс интуитивно понятен, поэтому сложностей быть не должно. 

Скопируйте созданные секреты и скопируйте их в манифест:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ya-s3-secret
type: Opaque
stringData:
  AWS_ACCESS_KEY_ID: '<идентификатор вашего секретного ключа>'
  AWS_SECRET_ACCESS_KEY: '<ваш секретный ключ>'
```

Активируйте этот манифест в кластере. 

## Использование MLFlow

Использовать MLFlow, который запущен в кластере, будет приложение, которое исполняется в том же кластере. Чтобы достучаться до MLFlow и его [Artifact Storage](https://mlflow.org/docs/latest/tracking/artifacts-stores.html), в качестве которого выступает (minio)[https://min.io/], нужно:

* Установить переменную окружения `MLFLOW_S3_ENDPOINT_URL=mlflow-minio.mlflow.svc`
* Установить переменную окружения `MLFLOW_TRACKING_URI=http://mlflow-tracking.mlflow.svc` или вызвать в коде метод `mlflow.set_tracking_uri('http://mlflow-tracking.mlflow.svc')`.

> Доменные имена `mlflow-minio.mlflow.svc` и `mlflow-tracking.mlflow.svc` – это имена служб k8s типа [ClusterIP](https://kubernetes.io/docs/concepts/services-networking/service/#type-clusterip), которые создает Helm при установке чарта с mlflow. Эти службы "тащат" трафик в соответствующие поды. 

## Установка Airflow

Ставим кластер:

```bash
helm install airflow bitnami/airflow --create-namespace --namespace=airflow
```

Реконфигурируем кластер:

```bash
helm upgrade --install airflow bitnami/airflow --create-namespace --namespace=airflow -f values.yaml
```

Проброс портов:

```bash
kubectl port-forward -n airflow svc/airflow 8080:8080
```

Логин: `user`. Узнать пароль:

```bash
kubectl get secret airflow --namespace airflow  --template='{{index .data "airflow-password"}}' | base64 -d
```