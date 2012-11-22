Ext.define('WebMailing.view.recipient.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Fit',
        'WebMailing.view.recipient.Grid',
        'WebMailing.LoadMask'
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
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
    }
});
