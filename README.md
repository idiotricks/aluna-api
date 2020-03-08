# Aluna API
Aluna adalah sistem informasi stock management yang
dirancang khusus untuk aplikasi kelola stok untuk
distro-distro pakaian.

![](./aluna.png)

## Instalasi Aluna API
Clone project ini ke direktori local Anda, lalu
masuk ke direktori project dan ketik:

```
$ pip install -r requirements.txt
$ python manage.py migrate
```

Selanjutnya buat superuser dengan perintah:

```
$ python manage.py createsuperuser
```

Lalu jalankan development server dengan perintah:

```
$ python manage.py runserver
```

Buka browser dan akses `http://localhost:8000/`.

### Aluna App
Unduh aplikasi `Aluna App` sebagai aplikasi berbasis web (User Interface)
untuk mengelola stok:

https://github.com/idiotricks/aluna-apps.





