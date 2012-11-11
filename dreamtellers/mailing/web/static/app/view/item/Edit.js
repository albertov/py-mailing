Ext.define('WebMailing.view.item.Edit', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Border',
        'Ext.layout.container.Fit',
        'WebMailing.store.ItemTreeStore',
        'WebMailing.view.item.Form',
        'WebMailing.view.item.Tree',
        'WebMailing.LoadMask'
    ],
    alias: 'widget.item_edit',
    layout: 'border',
    items: [
       { 
            xtype: 'panel',
            layout: 'fit',
            title: 'Items', // i18n
            itemId: 'tree_container',
            region: 'west',
            border: false,
            width: 400,
            collapsible: true
        }, {
            xtype: 'item_form',
            itemId: 'item_form',
            region: 'center'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
    },
    setMailing: function(record) {
        this._createAndSwapTree(record);
        this.loadMask.bindStore(record.items());
    },
    _createAndSwapTree: function(record) {
        var container = this.items.get('tree_container'),
            old = container.items.get(0),
            tree = Ext.create('WebMailing.view.item.Tree', {
                store: Ext.create('WebMailing.store.ItemTreeStore', {
                    mailing: record,
                    categories: Ext.getStore('Categories'),
                    border: false
                })
            });
        if (old)
            Ext.destroy(container.items.remove(old))
        container.items.add(tree);
    }
});

