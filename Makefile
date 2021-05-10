deploy:
	rsync -r dist/ root@allyfocus.com:/var/www/allyfocus.com/html/v11
	rsync nginx.conf root@allyfocus.com:/etc/nginx/sites-available/allyfocus.conf