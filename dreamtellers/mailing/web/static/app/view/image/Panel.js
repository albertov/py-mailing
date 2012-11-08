Ext.define('WebMailing.view.image.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.image.Grid'
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
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
    }
});
