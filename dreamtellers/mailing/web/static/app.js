Ext.application({
    name: 'WebMailing',
    appFolder: window.appFolder,
    models: ['Mailing'],
    stores: ['Mailings'],
    views: ['mailing.MailingGrid'],
    requires: [
        'WebMailing.Application',
    ],

    launch: function() {
        this.app = new WebMailing.Application();
    }
});
