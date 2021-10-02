# HomePortal
## MQTT Broker
### Description
This is a [MQTT mosquitto](https://mosquitto.org/) broker hosted on server. 
### Develop
- run
```sh
$ docker-compose -f docker-compose.dev.yaml up
```
### Production
- Check path at docker-compose and service files.
- Copy service to systemd and run.
```sh
$ sudo cp mosquitto.service /etc/systemd/system
$ sudo systemctl daemon-reload
$ sudo systemctl enable mosquitto.service
$ sudo systemctl start mosquitto.service
```
### Password
- After change password file you should restart the container.
- Tips: [http://www.steves-internet-guide.com/mqtt-username-password-example/](http://www.steves-internet-guide.com/mqtt-username-password-example/)
- You can use `mosquitto_passwd` command at the docker like:
    ```sh
    docker exec -it mosquitto mosquitto_passwd
    ```
#### Clear file and create new user
```sh
mosquitto_passwd -c /mosquitto/config/passwords username
```
#### Delete user from file
```sh
mosquitto_passwd -D /mosquitto/config/passwords username
```
#### Add user to file
```sh
mosquitto_passwd /mosquitto/config/passwords username
```

