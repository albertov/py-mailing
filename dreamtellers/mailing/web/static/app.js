Ext.application({
    name: 'WebMailing',
    appFolder: window.appFolder,
    controllers: [
        'Mailings', 'Items', 'Categories', 'Recipients', 'Groups', 'Images',
        'SentMailings', 'Templates'
    ],
    requires: [
        'Ext.app.Application',
        'Ext.tab.Panel',
        'Ext.container.Viewport',
        'WebMailing.view.Home'
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
                        title: 'Boletines' // i18n
                    }, {
                        id: 'categories',
                        xtype: 'categories',
                        title: 'Categorías' // i18n
                    }, {
                        id: 'images',
                        xtype: 'images',
                        title: 'Imágenes' // i18n
                    }, {
                        id: 'recipients',
                        xtype: 'recipients',
                        title: 'Suscriptores' // i18n
                    }, {
                        id: 'groups',
                        xtype: 'groups',
                        title: 'Grupos' // i18n
                    }, {
                        id: 'templates',
                        xtype: 'templates',
                        title: 'Plantillas' // i18n
                    }
                ]
            }
        });
    }
});
