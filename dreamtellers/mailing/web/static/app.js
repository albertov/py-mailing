Ext.application({
    name: 'WebMailing',
    appFolder: window.appFolder,
    models: ['ItemNode', 'Category', 'Item', 'Mailing'],
    stores: ['Mailings', 'Categories'],
    controllers: ['Mailings', 'Items', 'Categories'],
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
                    }, {
                        id: 'categories',
                        xtype: 'categories',
                        title: 'Categorías' // i18n
                    }
                ]
            }
        });
    }
});
