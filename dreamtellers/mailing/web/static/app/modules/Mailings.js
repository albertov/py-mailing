Ext.define('WebMailing.modules.Mailings', {
    extend: 'Ext.ux.desktop.Module',
    requires: [
        'WebMailing.view.mailing.MailingGrid'
    ],
    id: 'mailings',
    launcher: {
        text: 'Envíos'
    },

    createWindow: function() {
        var desktop = this.app.getDesktop();
        var win = desktop.getWindow(this.id);
        if (!win) {
            win = desktop.createWindow({
                id: this.id,
                title: this.launcher.text,
                layout: 'fit',
                width: 740,
                height: 480,
                constrainHeader: true,
                items: [
                    {xtype: 'mailinggrid'}
                ]
            });
        }
        return win;
    }
});
