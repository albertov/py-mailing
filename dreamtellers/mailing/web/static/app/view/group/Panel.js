Ext.define('WebMailing.view.group.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.LoadMask',
        'Ext.layout.container.Fit',
        'WebMailing.view.group.Grid'
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
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
    }
});
