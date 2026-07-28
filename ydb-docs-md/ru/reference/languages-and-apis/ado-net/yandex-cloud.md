---
title: "Подключение ADO.NET к Yandex Cloud"
url: "https://ydb.tech/docs/ru/reference/languages-and-apis/ado-net/yandex-cloud?version=v26.1"
doc_path: "ru/reference/languages-and-apis/ado-net/yandex-cloud"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/languages-and-apis/ado-net/yandex-cloud.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/languages-and-apis/ado-net/yandex-cloud.md"
description: "Установка. Чтобы использовать аутентификацию Yandex Cloud в вашем.NET-приложении, установите Ydb.Sdk.Yc.Auth NuGet-пакет: dotnet add package Ydb.Sdk.Yc.Auth."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Подключение ADO.NET к Yandex Cloud

## Установка {#ustanovka}

Чтобы использовать аутентификацию [Yandex Cloud](https://yandex.cloud/ru) в вашем .NET-приложении, установите `Ydb.Sdk.Yc.Auth` [NuGet-пакет](https://www.nuget.org/packages/Ydb.Sdk.Yc.Auth/):

```bash
dotnet add package Ydb.Sdk.Yc.Auth
```

Этот пакет предоставляет необходимые инструменты для аутентификации в сервисах Yandex Cloud.

## Аутентификация {#autentifikaciya}

Поддерживаемые Yandex Cloud методы аутентификации:

- `Ydb.Sdk.Yc.ServiceAccountProvider` — аутентификация через [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts). Пример использования:

  ```c#
  var saProvider = new ServiceAccountProvider(
      saFilePath: file, // Path to file with service account JSON info
      loggerFactory: loggerFactory
  );
  ```

- `Ydb.Sdk.Yc.MetadataProvider` — аутентификация через [сервис метаданных](https://yandex.cloud/ru/docs/compute/operations/vm-connect/auth-inside-vm); используется внутри облачных виртуальных машин Яндекса и облачных функций. Пример использования:

  ```c#
  var metadataProvider = new MetadataProvider(loggerFactory: loggerFactory);
  ```

## Сертификаты {#sertifikaty}

Библиотека включает в себя сертификаты Yandex Cloud, которые необходимы для подключения к Dedicated YDB:

```c#
var certs = Ydb.Sdk.Yc.YcCerts.GetYcServerCertificates();
```

## Как подключиться с ADO.NET {#kak-podklyuchitsya-s-adonet}

Чтобы установить безопасное соединение с YDB с помощью ADO.NET с требуемыми параметрами аутентификации и TLS, используйте следующий пример:

```c#
var builder = new YdbConnectionStringBuilder
{
    // More settings ...
    UseTls = true,
    Port = 2135,
    CredentialsProvider = saProvider, // For service account
    ServerCertificates = YcCerts.GetYcServerCertificates() // custom certificates Yandex Cloud
};
```

## Пример {#primer}

[ADO.NET подключение к Yandex Cloud](https://github.com/ydb-platform/ydb-dotnet-sdk/tree/main/examples/Ydb.Sdk.AdoNet.Yandex.Cloud)
