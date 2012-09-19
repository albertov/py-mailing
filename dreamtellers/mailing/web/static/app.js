Ext.application({
    name: 'WebMailing',
    appFolder: window.appFolder,
    models: ['Category', 'Item', 'Mailing'],
    stores: ['Mailings'],
    controllers: ['Mailings'],
    requires: [
        'Ext.tab.Panel',
        'Ext.container.Viewport',
        'WebMailing.view.Home',
    ],

    launch: function() {
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
    }
});
