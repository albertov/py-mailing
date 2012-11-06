Ext.define('WebMailing.CRUDGrid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Ext.grid.plugin.RowEditing'
    ],
    alias: 'widget.crud_grid',
    selModel: {
        pruneRemoved: false
    },
    initComponent: function() {
        this.actions = {
            'save': Ext.create('Ext.Action', {
                text: 'Guardar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEvent, this, ['save_items', this])
            }),
            'new': Ext.create('Ext.Action', {
                text: 'Nuevo', //18n
                handler: Ext.bind(this.fireEvent, this, ['new_item', this])
            }),
            'delete': Ext.create('Ext.Action', {
                text: 'Eliminar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['delete_item'])
            })
        };
        this.dockedItems = {
            xtype: 'toolbar',
            items: [
                this.actions['save'],
                this.actions['new'],
                this.actions['delete'],
            ]
        }
        this.contextMenu = Ext.create('Ext.menu.Menu', {
            items: [
                this.actions['delete'],
            ]
        });
        this.rowEditor = Ext.create('Ext.grid.plugin.RowEditing');
        this.plugins = [this.rowEditor];
        this.callParent(arguments);
        this.addEvents(['save_items', 'new_item', 'delete_item']);
        this.mon(this.store, 'write', this._setSaveActionState, this);
        this.mon(this.store, 'load', this._setSaveActionState, this);
        this.mon(this.store, 'update', this._setSaveActionState, this);
        this.mon(this.store, 'add', this._setSaveActionState, this);
        this.mon(this.store, 'remove', this._setSaveActionState, this);
        this.on('select', this.onRowSelect, this);
        this.on('deselect', this.onRowDeSelect, this);
        this.on('itemcontextmenu', this.onItemCtxMenu, this);
    },
    onRowSelect: function(grid, record) {
        this.selectedRecord = record;
        this._activateObjectActions();
    },
    _setSaveActionState: function() {
        if (this.store.getModifiedRecords().length>0 ||
            this.store.getRemovedRecords().length>0 ||
            this.store.getNewRecords().length>0) {
            this.actions.save.enable();
        } else {
            this.actions.save.disable();
        }
    },
    onRowDeSelect: function(grid, record) {
        this.selectedRecord = null;
        this._deactivateObjectActions();
    },

    onItemCtxMenu: function(grid, record, item, index, ev) {
        this.onRowSelect(grid, record);
        this.contextMenu.showAt(ev.getXY())
        ev.stopEvent();
        return false;
    },

    _activateObjectActions: function() {
        this.actions['delete'].enable();
    },

    _deactivateObjectActions: function() {
        this.actions['delete'].disable();
    },

    fireEventWithRecord: function(evname) {
        this.fireEvent(evname, this, this.selectedRecord);
    }
});
