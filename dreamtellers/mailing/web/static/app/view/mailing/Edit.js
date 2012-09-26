Ext.define('WebMailing.view.mailing.Edit', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.store.ItemTreeStore'
    ],
    alias: 'widget.mailing_edit',
    layout: 'fit',
    border: false,
    items: [
        {
            xtype: 'panel',
        }
    ],
    setRecord: function(record) {
        this.record = record;
        var old = this.items.get(0);
        Ext.destroy(old);
        this.items.remove(old);
        var tree = Ext.create('WebMailing.view.item.Tree', {
            store: Ext.create('WebMailing.store.ItemTreeStore', {
                mailing: record,
                categories: Ext.getStore('Categories')
            })
        });
        this.items.insert(0, tree);
        this.doLayout();
    }
});

