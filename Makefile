DIR=$(CURDIR)/dreamtellers/mailing/web/static
SENCHA=/Applications/SenchaSDKTools-2.0.0-beta3/sencha
URL=http://localhost:8080

all:
	cd $(DIR); $(SENCHA) create jsb -a $(URL) -p app.jsb3
	cd $(DIR); sed -i .bak 's:static/::g' app.jsb3 
	cd $(DIR); $(SENCHA) build -p app.jsb3 -d .
