Ext.define('Mailing.view.recipient.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Fit',
        'Mailing.view.recipient.Grid',
        'Mailing.LoadMask'
    ],
    alias: 'widget.recipients',
    tabConfig: {
        tooltip: 'Gestión e información de suscriptores'
    },
    layout: 'fit',
    items: [
        {
            xtype: 'recipient_grid'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    }
});
