Ext.application({
    name: 'WebMailing',
    appFolder: window.appFolder,
    models: ['Category', 'Item', 'Mailing'],
    stores: ['Mailings'],
    requires: [
        'WebMailing.Application',
    ],

    launch: function() {
        this.app = new WebMailing.Application(this);
    },

    getDesktop: function() {
        return this.app.getDesktop();
    }
});
