Ext.define('WebMailing.controller.Mailings', {
    extend: 'Ext.app.Controller',
    views: ['mailing.MailingPanel'],

    init: function() {
        this.control({
            "mailinggrid": {
                'select': this.onRowSelect
            }
        });
    },

    onRowSelect: function(selectionmodel, record) {
        var winId = record.id,
            desktop = this.application.getDesktop(),
            win = desktop.getWindow(winId);
        if (!win) {
            win = desktop.createWindow({
                id: winId,
                width: 800,
                height: 600,
                title: "Mailing #"+record.get('number'),
                layout: 'fit',
                constrainHeader: true,
                items: {xtype: 'mailingpanel', record: record}
            });
        }
        win.show();
    }
});

