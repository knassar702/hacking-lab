# Hacking-Lab

<h4>Hack this site using :  [xss , ssrf ,sql injection , command injection , open redirect , Server Side Template Injection (SSTI) , upload file]</h4>

Coded By khaled Nassar @knassar702

# Requirements :
- python2
- flask module
- jinja2 Template

# install requirements (Linux) :

````
$ apt install python2
````
````
$ pip2 install flask
````
````
$ pip2 install jinja2
````
# Run It :
````
$ git clone https://github.com/knassar702/hacking-lab && cd hacking-lab
````
````
$ python2 hackme.py
`````
# Login Page :

UserName : admin <br>
Password : p@ssword

* path traversal & XSS Stored : http://localhost/upload
* SQLI : http://localhost/posts/{ID}
* SSTI & XSS : http://localhost/search
* CSRF : http://localhost/login/edite/42
* SSRF & RCE : http://localhost/website?u=http://127.0.0.1
* open redirect : http://localhost/redirect?url=http://127.0.0.1/contact


<h4> Good Luck :)</h4>
