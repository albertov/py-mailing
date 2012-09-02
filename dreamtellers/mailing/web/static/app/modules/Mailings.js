Ext.define('WebMailing.modules.Mailings', {
    extend: 'Ext.ux.desktop.Module',
    requires: [
        'WebMailing.view.mailing.MailingGrid'
    ],
    id: 'mailings',
    launcher: {
        text: 'Envíos'
    },

    // TODO: factor this out into a base class
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
            var controller = this.app.getController('Mailings');
            win.mon(win, 'afterrender', function() {
                controller.init();
            }, this, {single:true});
            win.mon(win, 'destroy', function() {
                this.app.destroyController(controller);
            }, this, {single:true});
        }
        return win;
    }
});
