Ext.define('WebMailing.view.mailing.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.mailing.Grid',
        'WebMailing.view.mailing.Detail'
    ],
    alias: 'widget.mailings',
    layout: 'border',
    items: [
        {
            xtype: 'mailing_grid',
            region: 'west',
            width: 200,
            collapsible: true,
            split: true
        }, {
            xtype: 'mailing_detail',
            region: 'center'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
    }
});
