Ext.define('WebMailing.view.sent_mailing.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.LoadMask',
        'Ext.layout.container.Fit',
        'Ext.layout.container.Border',
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
            border: false,
            disabled: true
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
    },
    getRecord: function() {
        return this.record;
    },
    setRecord: function(record) {
        this.record = record;
        if (record) {
            this._createAndSwapGrid(record);
        } else {
            this.items.get('group_chooser').disable();
            this.items.get('grid_container').disable();
        }
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
