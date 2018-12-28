# Background
After having some performance issues with my cable modem, I wanted to start monitoring it so that Comcast could figure out what was going on.

Unfortunately, I found out from a Comcast employee that SMNP access to the cable modems is blocked from outside of their internal network, so my only option was to just constantly check the status page/event log that the modem provides. Or was it?


# About

The goal of this project was to create a better monitoring experience for Arris Surfboard cable modems.

With this code, you can log status information to [Grafana](https://grafana.com/) and event logs into [Elasticsearch](https://www.elastic.co/).

Once you get it all setup, the final output looks something like this:

![Image](https://i.imgur.com/OnJKgKP.png)

![Image](https://i.imgur.com/58G21Q6.png)


# Compatability

The only modem this is tested to work with is the **Arris Surfboard SB6183**. I would hazard a guess that most routers from the Arris Surfboard line would work fine -- if you are not sure, check that your modem's status/event pages look like mine (see the `html` folder).

This was developed on Ubuntu 18.10 and Windows compatability is unknown.


# Setup instructions

The code dependencies for this project are available in the `setup.py` file.

In addition, you will need:

* The ELK stack installed and running: https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-elk-stack-on-ubuntu-14-04

* The TIG stack installed and running: https://www.howtoforge.com/tutorial/how-to-install-tig-stack-telegraf-influxdb-and-grafana-on-ubuntu-1804/

This code uses the default ports for Logstash (5044, at the time of this writing) so no setup should be required there.

Once everything is setup, to run, simply do:

```bash
$ python3 main.py
```

# Bugs/TODO

This project is a very early work in progress. Here is my feature wishlist:

* [ ] Fix duplication issue with event log
* [ ] Add support for other cable modems
* [ ] Create a better CLI and/or GUI
