Ext.application({
    name: 'WebMailing',
    appFolder: url('static/app'),
    controllers: [
        'Mailings', 'Items', 'Categories', 'Recipients', 'Groups', 'Images',
        'SentMailings', 'Templates', 'Config'
    ],
    requires: [
        'Ext.app.Application',
        'Ext.tab.Panel',
        'Ext.container.Viewport',
        'WebMailing.view.Home'
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
                    }, {
                        id: 'config',
                        xtype: 'config',
                        title: 'Configuración' // i18n
                    }
                ]
            }
        });
    }
});
