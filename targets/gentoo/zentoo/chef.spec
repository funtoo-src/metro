[collect ../stage/stage4-generator.spec]

[section stage4]

name: zentoo-chef

[section zentoo/chef]

packages: [
	app-admin/chef-server
	dev-db/couchdb
	dev-java/sun-jdk
	dev-python/sphinx
	net-misc/rabbitmq-server
	www-servers/nginx
]

[section steps/stage4]

run: [
emerge $eopts $[zentoo/chef/packages] || exit 1
]
