Ext.define('WebMailing.view.sent_mailing.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.view.sent_mailing.Grid',
        'WebMailing.view.group.Chooser'
    ],
    alias: 'widget.sent_mailings',
    layout: 'border',
    border: false,
    items: [
        {
            xtype: 'panel',
            layout: 'fit',
            border: false,
            itemId: 'grid_container',
            region: 'west',
            width: 350
        }, {
            xtype: 'group_chooser',
            itemId: 'group_chooser',
            region: 'center',
            border: false
        }
    ],
    setRecord: function(record) {
        this.record = record;
        this._createAndSwapGrid(record);
    },
    _createAndSwapGrid: function(record) {
        var container = this.items.get('grid_container'),
            old = container.items.get(0),
            grid = Ext.create('WebMailing.view.sent_mailing.Grid', {
                store: record.sent_mailings()
            });
        if (old)
            Ext.destroy(container.items.remove(old))
        container.items.add(grid);
        grid.getStore().load();
    }
});
