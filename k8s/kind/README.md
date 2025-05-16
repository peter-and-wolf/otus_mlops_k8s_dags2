# Кластер kind (K8s in Docker)

## Установка kind и создание кластера

[Установка kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

[Создание кластера](https://kind.sigs.k8s.io/docs/user/quick-start/#creating-a-cluster)

## LoadBalancer service

[Установка дополнительного модуля](https://kind.sigs.k8s.io/docs/user/loadbalancer/)

Потом запустить бинарник (на маке от sudo)

```bash
sudo cloud-provider-kind
```

## Ingress

Устанавливаем контроллер

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Ждем, пока все очухается

```
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```


