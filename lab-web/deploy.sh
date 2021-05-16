 #!/bin/bash

 git pull
 docker stop labweb
 docker build -t lab-web .
 docker run -it -d -p 8080:80 --rm --restart unless-stopped --name labweb lab-web
