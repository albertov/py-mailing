Ext.application({
    name: 'WebMailing',
    appFolder: window.appFolder,
    models: ['Mailing', 'Category', 'Item'],
    stores: ['Mailings'],
    requires: [
        'WebMailing.Application',
    ],

    launch: function() {
        this.app = new WebMailing.Application();
    }
});
