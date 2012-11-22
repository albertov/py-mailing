Ext.define('Mailing.view.mailing_delivery.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Mailing.LoadMask',
        'Ext.layout.container.Fit',
        'Ext.layout.container.Border',
        'Mailing.view.mailing_delivery.Grid',
        'Mailing.view.group.Chooser'
    ],
    alias: 'widget.mailing_deliveries',
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
            border: false,
            disabled: true
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    },
    getRecord: function() {
        return this.record;
    },
    setRecord: function(record) {
        if (record!==this.record) {
            this.record = record;
            if (record) {
                this._createAndSwapGrid(record);
            } else {
                this.items.get('group_chooser').disable();
                this.items.get('grid_container').disable();
            }
        }
    },
    _createAndSwapGrid: function(record) {
        var container = this.items.get('grid_container'),
            old = container.items.get(0),
            grid = Ext.create('Mailing.view.mailing_delivery.Grid', {
                store: record.mailing_deliveries()
            });
        if (old)
            Ext.destroy(container.items.remove(old))
        container.items.add(grid);
        grid.getStore().load();
    }
});
