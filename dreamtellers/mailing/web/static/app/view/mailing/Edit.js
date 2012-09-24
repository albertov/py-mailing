Ext.define('WebMailing.view.mailing.Edit', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.mailing_edit',
    layout: 'fit',
    border: false,
    items: [
        {
            xtype: 'panel',
        }
    ],

    setRecord: function(record) {
        if (record!==this.record) {
            this.record = record;
            var old = this.items.get(0);
            Ext.destroy(old);
            this.items.remove(old);
            var tree = Ext.create('WebMailing.view.item.Tree', {
                store: record.item_tree(),
                root: {
                    expanded: true,
                    title: this.record.getTitle()
                }
            });
            this.items.insert(0, tree);
            this.doLayout();
        }
    }
});

