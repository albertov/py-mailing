Ext.define('Mailing.view.image.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Fit',
        'Mailing.view.image.Grid'
    ],
    alias: 'widget.images',
    layout: 'fit',
    items: [
        {
            xtype: 'image_grid'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    }
});
