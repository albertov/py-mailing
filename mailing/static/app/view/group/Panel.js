Ext.define('Mailing.view.group.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Mailing.LoadMask',
        'Ext.layout.container.Fit',
        'Mailing.view.group.Grid'
    ],
    alias: 'widget.groups',
    layout: 'fit',
    items: [
        {
            xtype: 'group_grid'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    }
});
