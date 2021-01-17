 #!/bin/bash

 git pull
 docker stop dyndns
 docker build -t dyndns .
 docker run -it -d --restart unless-stopped --name dyndns dyndns
