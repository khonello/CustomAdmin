# Custom Django Administration

### Production Environment Setup
- Open `WSL`
- Create virtual environment
- Install `gunicorn` using `pip3 install gunicorn`
- Bind the application to `gunicorn` using `gunicorn --bind 0.0.0.0:8000 project.wsgi:application`
- Create a service for `gunicorn` using `sudo nano /etc/systemd/system/gunicorn.service`
- Update the `gunicorn.service` with this code:
```
Bash

[Unit]
Description=Gunicorn instance to serve Django Project
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/gunicorn --workers 4 --bind unix:/path/to/your/project/gunicorn/gunicorn.sock project.wsgi:application

RuntimeDirectory=gunicorn
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
```
- Start and enable `gunicorn` using this:
```
Bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
- Create an `Nginx` configuration file with this `sudo nano /etc/nginx/sites-available/<project>
`
- Update the `Nginx` configuration file `<project>` with this code:
```
Bash
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://unix:/path/to/your/project/gunicorn/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }
}
```
- Enable the `Nginx` configuration using these commands:
```
Bash
sudo ln -s /etc/nginx/sites-available/<project> /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx

```
- Reload and check if everything is operational:
```
Bash
sudo systemctl daemon-reload
sudo systemctl status gunicorn
sudo systemctl status nginx
```
- Set appropriate permissions using these commands:
```
Bash
sudo chown -R khonello:www-data /run/gunicorn/
sudo chmod -R 775 /run/gunicorn/
```
