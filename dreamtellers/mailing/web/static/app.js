Ext.application({
    name: 'WebMailing',
    appFolder: window.appFolder,
    models: ['ItemNode', 'Category', 'Item', 'Mailing'],
    stores: ['Mailings', 'Categories'],
    controllers: ['Mailings'],
    requires: [
        'Ext.tab.Panel',
        'Ext.container.Viewport',
        'WebMailing.view.Home',
    ],

    launch: function() {
        window.application = this;
        Ext.create('Ext.container.Viewport', {
            layout: 'fit',
            items: {
                xtype: 'tabpanel',
                items: [
                    {
                        id: 'home',
                        xtype: 'home',
                        title: 'Inicio' // i18n
                    }, {
                        id: 'mailings',
                        xtype: 'mailings',
                        title: 'Envíos' // i18n
                    }
                ]
            }
        });
    },
    getFreshController: function(name) {
        this.destroyController(name);
        return this.getController(name);
    },
    destroyController: function(name) {
        var old = this.controllers.get(name);
        if (old) {
            Ext.destroy(this.controllers.remove(old));
        }
    }
});
