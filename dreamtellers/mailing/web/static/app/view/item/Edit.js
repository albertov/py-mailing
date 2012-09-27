Ext.define('WebMailing.view.item.Edit', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.store.ItemTreeStore',
        'WebMailing.view.item.Form',
        'WebMailing.view.item.Tree'
    ],
    alias: 'widget.item_edit',
    layout: 'border',
    items: [
       { 
            xtype: 'container',
            layout: 'fit',
            itemId: 'tree_container',
            region: 'west',
            width: 400,
            collapsible: true
        }, {
            xtype: 'item_form',
            itemId: 'item_form',
            region: 'center'
        }
    ],
    setMailing: function(record) {
        this._createAndSwapTree(record);
    },
    _createAndSwapTree: function(record) {
        var container = this.items.get('tree_container'),
            old = container.items.get(0),
            tree = Ext.create('WebMailing.view.item.Tree', {
                store: Ext.create('WebMailing.store.ItemTreeStore', {
                    mailing: record,
                    categories: Ext.getStore('Categories')
                })
            });
        if (old)
            Ext.destroy(container.items.remove(old))
        container.items.add(tree);
    }
});

