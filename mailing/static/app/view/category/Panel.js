Ext.define('Mailing.view.category.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Fit',
        'Mailing.view.category.Tree'
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
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    }
});
