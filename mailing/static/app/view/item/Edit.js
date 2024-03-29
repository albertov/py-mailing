Ext.define('Mailing.view.item.Edit', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Border',
        'Ext.layout.container.Fit',
        'Mailing.view.item.Form',
        'Mailing.view.item.Tree',
        'Mailing.LoadMask'
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
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    },
    setMailing: function(record) {
        if (record!==this.record) {
            console.debug('setMailing');
            this.record = record;
            this._createAndSwapTree(record);
            this.loadMask.bindStore(record.items());
        }
    },
    _createAndSwapTree: function(record) {
        var container = this.items.get('tree_container'),
            old = container.items.get(0),
            tree = Ext.create('Mailing.view.item.Tree', {
                mailing: record,
                categories: Ext.getStore('Categories'),
            });
        if (old)
            Ext.destroy(container.items.remove(old))
        container.items.add(tree);
    }
});

