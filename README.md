# docker-ascii-map
A set of python scripts displaying the local docker containers structure and status on an ascii map.

## Requirements

* python 3.5
* docker-py

## Usage

Below is a sample of a host running several applications on multiple networks. 
A container is routing traffic to these networks from the host.

```
alcibiade@mobydick:~/docker-ascii-map$ python3 src/docker-ascii-map.py
 
                                                   +- chesscorp_default ----------------+
                                                   | [✓] chesscorp_web_1                |
80 ]------------  [✓] frontend_httpd_1 ------+     |     chesscorp/chess-club           |
                      httpd:2.4              +-----| [✓] chesscorp_database_1           |
                                             |     |     postgres:9.5                   |
                                             |     | [✓] chesscorp_mail_1               |
                                             |     |     namshi/smtp                    |
                                             |     +------------------------------------+
                                             |     +- wordpress_default ----------------+
                                             |     | [✓] wordpress_web_1                |
                                             |     |     wordpress_web                  |
                                             +-----| [✓] wordpress_db_1                 |
                                                   |     mysql:5.7                      |
                                                   | [✓] wordpress_mail_1               |
                                                   |     namshi/smtp                    |
                                                   +------------------------------------+
                                                   +- mail_default ---------------------+
25 ]-----------------------------------------------+ [✓] mail_mailserver_1              |
                                                   |     tvial/docker-mailserver:latest |
                                                   +------------------------------------+
                                                   +- proxy_default --------------------+
                                                   | [❌] proxy_squid_1                  |
                                                   |     sameersbn/squid                |
                                                   +------------------------------------+

```
