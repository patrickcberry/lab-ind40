# lab-web
Static documentation website for Industry 4.0 Test Lab.

## Build and Test Local
Building and testing locally requires that the Docker engine be installed.

Build image:
```
docker build -t lab-web .
```
Run:
```
docker run -it --rm -d -p 8080:80 --name labweb lab-web
```
Stop:
```
docker stop labweb
```
_The container is automatically removed through the use of the `--rm` tag._

Single batch file build and run:
```
run.bat
```

## Push to GitHub
Using Visual Code, Powershell terminal run the `update.bat` file:
```
.\\update.bat
```
## Deploy
On the remote machine, initally, `clone` the Github repository:
```
git clone https://github.com/patrickcberry/lab-web.git
```

After the repository has been cloned, for any furure updates issue the, `git pull` command.

Change directory to `lab-web`
```
cd lab-web
```

Run the docker build and run commands as per the development environment,
```
sudo docker build -t lab-web .
sudo docker run -it --rm -d -p 8080:80 --name labweb lab-web
```
Using the bash script:
```
sudo sh ./deploy.sh
```
Note: the bash script above will:
+ Pull the latest version from GitHub
+ Build the container
+ Deploy the new container
