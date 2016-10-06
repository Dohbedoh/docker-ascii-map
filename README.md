# docker-ascii-map
A set of python scripts displaying the local docker containers structure and status on an ascii map.

## Requirements

* python 3.2
* docker-py

## Usage

```
alcibiade@mobydick:~/docker-ascii-map$ python3 src/docker-ascii-map.py 
+- chesscorp_default -------+
| [✓] /chesscorp_web_1      |
|     chesscorp/chess-club  |
| [✓] /chesscorp_database_1 |
|     postgres:9.5          |
| [✓] /chesscorp_mail_1     |
|     namshi/smtp           |
| [✓] /frontend_httpd_1     |
|     httpd:2.4             |
+---------------------------+
+- mail_default ---------------------+
| [✓] /mail_mailserver_1             |
|     tvial/docker-mailserver:latest |
+------------------------------------+
+- wordpress_default ---+
| [✓] /wordpress_web_1  |
|     wordpress_web     |
| [✓] /wordpress_db_1   |
|     mysql:5.7         |
| [✓] /wordpress_mail_1 |
|     namshi/smtp       |
| [✓] /frontend_httpd_1 |
|     httpd:2.4         |
+-----------------------+

```
