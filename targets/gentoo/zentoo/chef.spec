[collect ./generator.spec]

[section zentoo]

name: chef

[section zentoo/chef]

packages: [
	app-admin/chef-server
	dev-db/couchdb
	dev-java/sun-jdk
	dev-python/sphinx
	net-misc/rabbitmq-server
	www-servers/nginx
]

[section steps/zentoo]

run: [
emerge $eopts $[zentoo/chef/packages] || exit 1
]
