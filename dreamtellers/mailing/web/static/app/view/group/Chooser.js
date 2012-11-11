Ext.define('WebMailing.view.group.Chooser', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Border',
        'Ext.grid.plugin.DragDrop',
        'WebMailing.view.group.Grid'
    ],
    layout: 'border',
    alias: 'widget.group_chooser',
    items: [
        {
            itemId: 'available',
            title: 'Grupos disponibles', // i18n
            xtype: 'group_grid',
            region: 'north',
            height: 400,
            plugins: null,
            store: 'Groups',
            multiSelect: true,
            viewConfig: {
                plugins: {
                    ptype: 'gridviewdragdrop',
                    ddGroup: 'groupgriddrag',
                    enableDrop: false
                },
                copy: true
            }
        }, {
            itemId: 'selected',
            title: 'Grupos seleccionados', // i18n
            xtype: 'group_grid',
            region: 'center',
            plugins: [
                {
                    ptype: 'crud',
                    actions: 'delete',
                    enable_row_edit: false
                }
            ],
            store: Ext.create('Ext.data.Store', {
                model: 'WebMailing.model.Group',
                proxy: {type:'memory'}
            }),
            viewConfig: {
                plugins: {
                    ptype: 'gridviewdragdrop',
                    ddGroup: 'groupgriddrag',
                    enableDrop: true,
                    enableDrag: false
                }
            }
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.items.get('selected').getView().on('beforedrop', this.onBeforeDrop,
                                                this);
    },
    onBeforeDrop: function(_, data) {
        var store = this.items.get('selected').getStore();
        for (var i=0; i<data.records.length; i++) {
            var record = data.records[i];
            if (store.getById(record.getId())) {
                return false;
            }
        }
    }
});
