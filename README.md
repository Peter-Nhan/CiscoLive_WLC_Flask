# CiscoLive_WLC_Flask
See the Blog for more details - https://peter-nhan.github.io/posts/CiscoLive-WLC-Web-Monitoring-App/

Dockerise into two containers Nginx and Gunicorn/Flask/Python to monitor WLC for Cisco Live.
Flask WSGI App - SSH to the Wireless LAN controller to parse a show command output then takes the output and makes it easily consumable via a web page.

Please be aware the current code lacks error handling ability.
Modify the Username/password/enable secret and IP address of your WLC in app.py file.

Kick off the docker containers with:
> docker-compose up -d --build

To shutdown and clean up:
> docker-compose down --rmi all
