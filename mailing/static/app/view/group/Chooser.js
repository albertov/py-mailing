Ext.define('Mailing.view.group.Chooser', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Border',
        'Ext.grid.plugin.DragDrop',
        'Ext.tip.ToolTip',
        'Mailing.view.group.Grid'
    ],
    layout: 'border',
    alias: 'widget.group_chooser',
    items: [
        {
            itemId: 'available',
            title: 'Grupos disponibles', // i18n
            xtype: 'group_grid',
            region: 'north',
            height: 300,
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
                    item_names: ['grupo selecionado', 'grupos seleccionados'],
                    actions: 'delete',
                    enable_row_edit: false
                }
            ],
            store: Ext.create('Ext.data.Store', {
                model: 'Mailing.model.Group',
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
        var view = this.getSelectedGrid().getView();
        view.on('beforedrop', this.onBeforeDrop, this);
        this.getSelectedGrid().relayEvents(view, ["drop"]);
        this.getAvailableGrid().getView().on('render', this._createTooltip,
                                             this);
    },
    getSelectedGrid: function() {
        return this.items.get('selected');
    },
    getAvailableGrid: function() {
        return this.items.get('available');
    },
    onBeforeDrop: function(_, data) {
        var store = this.getSelectedGrid().getStore();
        for (var i=0; i<data.records.length; i++) {
            var record = data.records[i];
            if (store.getById(record.getId())) {
                return false;
            }
        }
    },
    _createTooltip: function(view) {
        view.tip = Ext.widget('tooltip', {
            target: view.el,
            // Each grid row causes its own seperate show and hide.
            delegate: view.itemSelector,
            // Moving within the row should not hide the tip.
            trackMouse: true,
            renderTo: Ext.getBody(),
            html: 'Haga doble click sobre los grupos o arrastrélos sobre la '+
                  'rejilla de abajo para seleccionarlos'

        });
    }
    
});
