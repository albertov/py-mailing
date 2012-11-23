Ext.define('Mailing.view.mailing.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Border',
        'Mailing.view.mailing.Grid',
        'Mailing.view.mailing.Detail'
    ],
    tabConfig: {
        tooltip: 'Gestión y envío de boletines' // i18n
    },
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
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    }
});
