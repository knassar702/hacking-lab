git clone https://github.com/tomnomnom/httprobe
#apt install golang
cd httprobe
echo 'google.com' > domains
cat domains | go run main.go | tee lol
#rm install.sh
# By : knassar702
