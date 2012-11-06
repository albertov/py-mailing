Ext.define('WebMailing.view.recipient.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.recipient.Grid'
    ],
    alias: 'widget.recipients',
    layout: 'fit',
    items: [
        {
            xtype: 'recipient_grid'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('Ext.LoadMask', this, {
            msg: 'Por favor, espere....' //i18n
        });
    }
});