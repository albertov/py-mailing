Ext.define('WebMailing.view.category.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.category.Tree'
    ],
    alias: 'widget.categories',
    layout: 'fit',
    items: [
        {
            xtype: 'category_tree'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
    }
});
