# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Координаты сервера для проверяющего

- [перейти на сайт](https://nopath.ru)
- ip address: `45.142.122.145`.
- Скрипт для деплоя находится в домашней директории пользователя `ilya` ~/star-burger-deployment .
- Имя пользователя `ilya`.
- Проект находится в директории ~/projects/star-burger/ .
- Пароль находится в файле help.txt
## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Как собрать бэкенд

<details>
<summary>
Как собрать бэкенд
</summary>
Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:
- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран. Переходите к следующему разделу README.

</details>

### Собрать фронтенд

<details>
<summary>
Как собрать фронтенд
</summary>

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v12.18.2
# Если ошибка, попробуйте node:
node --version
# v12.18.2

npm --version
# 6.14.5
```

Версия `nodejs` должна быть не младше 10.0. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Установите необходимые пакеты. В каталоге проекта запустите:

```sh
npm install --dev
```

Установите [Parcel](https://parceljs.org/). Это упаковщик веб-приложений. Он похож на [Webpack](https://webpack.js.org/), но совсем не требует настроек:

```sh
npm install -g parcel@2.0.0-beta.2  # понадобятся права администратора `sudo`
```

Вам нужна вторая версия Parcel. Проверьте, что `parcel` установлен и его версию в командной строке:

```sh
$ parcel --version
2.0.0-beta.2
```

Почти всё готово. Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточно и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/), то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта, когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию. В норме Parcel решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и предупреждает JS-код в браузере о необходимости подтянуть свежий код. Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша, жмите <kbd>Ctrl-F5</kbd>.
</details>

## Как запустить prod-версию сайта

<details>
<summary>
Как запустить prod-версию сайта
</summary>

Собрать фронтенд:

```sh
parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```

Настроить бэкенд: создать файл `.env` в каталоге `star_burger/` со следующими настройками:

- `DEBUG` - дебаг-режим. Поставьте `False`.
- `SECRET_KEY` - секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте. Не стоит использовать значение по-умолчанию, **замените на своё**.
- `ALLOWED_HOSTS` - [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `YANDEX_GEO_API` - [получить здесь](https://developer.tech.yandex.ru/services/) API яндекса для работы с картами
- `ROLLBAR_TOKEN` - токен [rollbar.com](https://rollbar.com)
- `ROLLBAR_ENV` - `development` или `production`

[Инструкция по подключению rollbar](https://docs.rollbar.com/docs/django)
</details>

## Как запустить dev-версию сайта с использованием docker-compose

<details>
<summary>
Как запустить dev-версию сайта с использованием docker-compose
</summary>

Создайте в директории star-burger две переменных окружения:
1) `.env` - обязательная.

- `DEBUG`= настройка Django для включения отладочного режима. Принимает значения `TRUE` или `FALSE`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DEBUG).
- `SECRET_KEY`= обязательная секретная настройка Django. Это - соль для генерации хэшей. Значение может быть любым, важно лишь, чтобы оно никому не было известно. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key).
- `ALLOWED_HOSTS`= настройка Django со списком разрешённых адресов. Если запрос прилетит на другой адрес, то сайт ответит ошибкой 400. Можно перечислить несколько адресов через запятую, например `127.0.0.1,192.168.0.1,site.test`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts).
- `DATABASE_URL`= адрес для подключения к базе данных PostgreSQL. Другие СУБД сайт не поддерживает. [Формат записи](https://github.com/jacobian/dj-database-url#url-schema).
- `CSRF_COOKIE_DOMAIN`= `http://127.0.0.1:1337`, `http://mydomain.ru`, `https://mydomain.ru` [Документация](https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-cookie-domain).
- `CSRF_TRUSTED_ORIGINS`= `http://127.0.0.1:1337`, `http://mydomain.ru`, `https://mydomain.ru` [Документация](https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins).
- `VIRTUAL_HOST`= `http://mydomain.ru` - настройка для prod версии.
- `VIRTUAL_PORT`= `8000` - настройка для prod версии. `expose`'d порт, см файл
- `LETSENCRYPT_HOST`= `http://mydomain.ru` - настройка для prod версии. Хост, для которого необходимо будет получить сертификат.
- `YANDEX_GEO_API` - [получить здесь](https://developer.tech.yandex.ru/services/) API яндекса для работы с картами
- `ROLLBAR_TOKEN` - токен [rollbar.com](https://rollbar.com)
- `ROLLBAR_ENV` - `development` или `production`

[Инструкция по подключению rollbar](https://docs.rollbar.com/docs/django)

#### ВАЖНО! В переменной `DATABASE_URL` вместо localhost используйте `host.docker.internal`, если необходимо подключиться к postgres на локальном сервере.

2) `.env.staging.proxy-companion` - тоже обязательная, но для prod-версии.

- `DEFAULT_EMAIL`= `your_email@mail.com` - настройка для prod версии. На этот адрес будут приходить уведомления от [letsencrypt.org](https://letsencrypt.org).
- `ACME_CA_URI`= `https://acme-staging-v02.api.letsencrypt.org/directory` - настройка для prod версии. Необходимо будет удалить данную опцию после первого получения сертификата.
- `NGINX_PROXY_CONTAINER`= `nginx-proxy-starburger` - настройка для prod версии. Название вашего nginx-proxy контейнер из docker-compose.prod.yaml.

Разрешите докеру подключаться к Postgres:
```shell
cd /etc/postgresql/<psql_version>/main

```
1) Отредактируйте файл `postgresql.conf`:
Добавьте прослушивание всех адресов.
```shell
#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------

# - Connection Settings -

listen_addresses = '*'          # what IP address(es) to listen on;
# comma-separated list of addresses;
# defaults to 'localhost'; use '*' for all
# (change requires restart)
port = 5432                             # (change requires restart)
max_connections = 100                   # (change requires restart)
```
2) Отредактируйте файл `pg_hba.conf`:
Добавьте в список "допустимых" для прослушивания адресов `172.17.0.1/0` - стандартный ip-адрес для Docker контейнера.
```
host    replication     all             ::1/128                md5
host    all             all             172.17.0.1/0           md5
host    all             all             ::ffff:ac11:1/0        md5
```

Выполните команду:

```sh
docker-compose -f docker-compose.dev.yaml up --build -d
```

Сайт будет доступен по адресу http://ip.ip.ip.ip:1337

</details>

## Как запустить prod-версию сайта с использованием docker-compose

<details>
<summary>
Как запустить prod-версию сайта с использованием docker-compose
</summary>

Выполните инструкции из предыдущего пункта, а затем запустите скрипт:
```sh
docker-compose -f docker-compose.prod.yaml up --build -d
```

Сайт будет доступен по адресу https://yourdomain.ru

</details>

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

## Список возможных (и невозможных) проблем:

```shell
ERROR: for nginx-proxy-starburger Cannot start service nginx-proxy-starburger: driver failed programming external connectivity on endpoint nginx-proxy-starburger (long_hash): Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
```

[Возможное решение](https://stackoverflow.com/questions/37971961/docker-error-bind-address-already-in-use)
